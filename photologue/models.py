import os
import shutil
import zipfile

from datetime import datetime
from inspect import isclass

# Required PIL classes may or may not be available from the root namespace
# depending on the installation method used.
try:
    import Image
    import ImageFile
    import ImageFilter
    import ImageEnhance
except ImportError:
    try:
        from PIL import Image
        from PIL import ImageFile
        from PIL import ImageFilter
        from PIL import ImageEnhance
    except ImportError:
        raise ImportError("Photologue was unable to import the Python " \
                          "Imaging Library. Please confirm it's installed " \
                          "and available on your current Python path.")

from django.db import models
from django.db.models import signals
from django.conf import settings
from django.utils.functional import curry
from django.core.validators import ValidationError
from django.core.urlresolvers import reverse
from django.dispatch import dispatcher
from django.template.defaultfilters import slugify

# attempt to load the django-tagging TagField from default location,
# otherwise we substitude a dummy TagField.
try:
    from tagging.fields import TagField
    tagfield_help_text = 'Separate tags with spaces, put quotes around multiple-word tags.'
except ImportError:
    class TagField(models.CharField):
        def __init__(self, **kwargs):
            default_kwargs = {'max_length': 255, 'blank': True}
            default_kwargs.update(kwargs)
            super(TagField, self).__init__(**default_kwargs)
        def get_internal_type(self):
            return 'CharField'
    tagfield_help_text = 'Django-tagging was not found, tags will be treated as plain text.'

from util import EXIF

# Path to sample image
SAMPLE_IMAGE_PATH = getattr(settings, 'SAMPLE_IMAGE_PATH', os.path.join(os.path.dirname(__file__), 'res', 'sample.jpg')) # os.path.join(settings.PROJECT_PATH, 'photologue', 'res', 'sample.jpg'

# Photologue image path relative to media root
PHOTOLOGUE_DIR = getattr(settings, 'PHOTOLOGUE_DIR', 'photologue')

# Modify image file buffer size.
ImageFile.MAXBLOCK = getattr(settings, 'PHOTOLOGUE_MAXBLOCK', 256*1024)

# Prepare a list of image filters
filter_names = []
for n in dir(ImageFilter):
    klass = getattr(ImageFilter, n)
    if isclass(klass) and issubclass(klass, ImageFilter.BuiltinFilter) and \
        hasattr(klass, 'name'):
            filter_names.append(klass.__name__)
image_filters_help_text = 'Chain multiple filters using the following pattern "FILTER_ONE->FILTER_TWO->FILTER_THREE". ' \
                          'Image filters will be applied in order. The following filter are available: %s' % \
                          ', '.join(filter_names)

# Quality options for JPEG images
JPEG_QUALITY_CHOICES = (
    (30, 'Very Low'),
    (40, 'Low'),
    (50, 'Medium-Low'),
    (60, 'Medium'),
    (70, 'Medium-High'),
    (80, 'High'),
    (90, 'Very High'),
)

# choices for new crop_anchor field in Photo
CROP_ANCHOR_CHOICES = (
    ('top', 'Top'),
    ('right', 'Right'),
    ('bottom', 'Bottom'),
    ('left', 'Left'),
    ('center', 'Center (Default)'),
)


class Gallery(models.Model):
    pub_date = models.DateTimeField("Date published", default=datetime.now)
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(prepopulate_from=('title',), unique=True,
                            help_text='A "Slug" is a unique URL-friendly title for an object.')
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=True,
                                    help_text="Public galleries will be displayed in the default views.")
    photos = models.ManyToManyField('Photo', related_name='galleries', filter_interface=models.HORIZONTAL)
    tags = TagField(help_text=tagfield_help_text)

    class Meta:
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'
        verbose_name_plural = "galleries"

    class Admin:
        list_display = ('title', 'pub_date', 'photo_count', 'is_public')
        list_filter = ['pub_date', 'is_public']
        date_hierarchy = 'pub_date'

    def __unicode__(self):
        return self.title
        
    def __str__(self):
        return self.__unicode__()

    def get_absolute_url(self):
        args = self.pub_date.strftime("%Y/%b/%d").lower().split("/") + [self.slug]
        return reverse('pl-gallery-detail', args=args)

    def latest(self, limit=5):
        return self.photos.all()[:limit]

    def photo_count(self):
        return self.photos.all().count()
    photo_count.short_description = 'Count'

    def public_photos(self):
        return self.photos.filter(is_public=True)


class GalleryUpload(models.Model):
    id = models.IntegerField(default=1, editable=False, primary_key=True)
    zip_file = models.FileField('Images file (.zip)', upload_to=PHOTOLOGUE_DIR+"/temp",
                                help_text="Select a .zip file of images to upload into a new Gallery.")
    title_prefix = models.CharField(max_length=75, help_text="All photos in the gallery will be given a title made up of this prefix + a sequential number.")
    caption = models.TextField(blank=True, help_text="Caption will be added to all photos.")
    description = models.TextField(blank=True, help_text="A description of this Gallery.")
    photographer = models.CharField(max_length=100, blank=True)
    info = models.TextField(blank=True, help_text="Additional information about the photograph such as date taken, equipment used etc..")
    is_public = models.BooleanField(default=True, help_text="Uncheck this to make the uploaded gallery and included photographs private.")
    tags = models.CharField(max_length=255, blank=True, help_text=tagfield_help_text)

    class Admin:
        pass

    def save(self):
        super(GalleryUpload, self).save()
        self.process_zipfile()
        super(GalleryUpload, self).delete()

    def process_zipfile(self):
        if os.path.isfile(self.get_zip_file_filename()):
            # TODO: implement try-except here
            zip = zipfile.ZipFile(self.get_zip_file_filename())
            bad_file = zip.testzip()
            if bad_file:
                raise Exception('"%s" in the .zip archive is corrupt.' % bad_file)
            count = 1
            gallery = Gallery.objects.create(title=self.title_prefix,
                                             slug=slugify(self.title_prefix),
                                             description=self.description,
                                             is_public=self.is_public,
                                             tags=self.tags)
            from cStringIO import StringIO
            for filename in zip.namelist():
                if filename.startswith('__'): # do not process meta files
                    continue
                data = zip.read(filename)
                if len(data):
                    try:
                        # the following is taken from django.newforms.fields.ImageField:
                        #  load() is the only method that can spot a truncated JPEG,
                        #  but it cannot be called sanely after verify()
                        trial_image = Image.open(StringIO(data))
                        trial_image.load()
                        # verify() is the only method that can spot a corrupt PNG,
                        #  but it must be called immediately after the constructor
                        trial_image = Image.open(StringIO(data))
                        trial_image.verify()
                    except Exception:
                        # if a "bad" file is found we just skip it.
                        continue
                    title = ' '.join([self.title_prefix, str(count)])
                    slug = slugify(title)
                    photo = Photo(title=title, slug=slug,
                                  caption=self.caption,
                                  photographer=self.photographer,
                                  info=self.info,
                                  is_public=self.is_public,
                                  tags=self.tags)
                    photo.save_image_file(filename, data)
                    gallery.photos.add(photo)
                    count = count + 1
            zip.close()
            try:
                os.remove(self.get_zip_file_filename())
            except:
                pass


class Photo(models.Model):
    image = models.ImageField("Photograph", upload_to=PHOTOLOGUE_DIR+"/photos/%Y/%b/%d")
    pub_date = models.DateTimeField("Date published", default=datetime.now)
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(prepopulate_from=('title',), unique=True,
                            help_text='A "Slug" is a unique URL-friendly title for an object.')
    caption = models.TextField(blank=True)
    photographer = models.CharField(max_length=100, blank=True)
    date_taken = models.DateTimeField(null=True, blank=True)
    info = models.TextField(blank=True, help_text="Additional information about the photograph such location, equipment used etc..")
    crop_from = models.CharField(blank=True, max_length=10, default='center', choices=CROP_ANCHOR_CHOICES)
    is_public = models.BooleanField(default=True, help_text="Public photographs will be displayed in the default views.")
    tags = TagField(help_text=tagfield_help_text)
    effect = models.ForeignKey('PhotoEffect', null=True, blank=True, related_name='photos')

    class Meta:
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'

    class Admin:
        list_display = ('title', 'date_taken', 'pub_date', 'photographer', 'is_public', 'tags', 'admin_thumbnail')
        list_filter = ['pub_date', 'is_public']
        list_per_page = 10

    @property
    def EXIF(self):
        try:
            return EXIF.process_file(open(self.get_image_filename(), 'rb'),
                                     details=False)
        except:
            return {}

    def admin_thumbnail(self):
        func = getattr(self, 'get_admin_thumbnail_url', None)
        if func is None:
            return 'An "admin_thumbnail" photo size has not been defined.'
        else:
            return u'<a href="%s"><img src="%s"></a>' % \
                (self.get_absolute_url(), func())
    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True

    def __unicode__(self):
        return self.title
        
    def __str__(self):
        return self.__unicode__()

    def get_absolute_url(self):
        args = self.pub_date.strftime("%Y/%b/%d").lower().split("/") + [self.slug]
        return reverse('pl-photo-detail', args=args)

    def cache_path(self):
        return os.path.join(os.path.dirname(self.get_image_filename()), "cache")

    def cache_url(self):
        return '/'.join([os.path.dirname(self.get_image_url()), "cache"])

    def image_filename(self):
        return os.path.basename(self.image)

    def _get_filename_for_size(self, size):
        base, ext = os.path.splitext(self.image_filename())
        return ''.join([base, '_', size, ext])

    def _get_SIZE_size(self, photosize):
        return photosize.size

    def _get_SIZE_url(self, photosize):
        if not self.size_exists(photosize):
            self.create_size(photosize)
        return '/'.join([self.cache_url(), self._get_filename_for_size(photosize.name)])

    def _get_SIZE_path(self, photosize):
        return os.path.join(self.cache_path(),
                            self._get_filename_for_size(photosize.name))

    def add_accessor_methods(self, *args, **kwargs):
        cache = PhotoSizeCache()
        if len(cache.sizes):
            sizes = cache.sizes.values()
        else:
            sizes = PhotoSize.objects.all()
            for size in sizes:
                cache.sizes[size.name] = size
        for photosize in sizes:
            setattr(self, 'get_%s_size' % photosize.name,
                    curry(self._get_SIZE_size, photosize=photosize))
            setattr(self, 'get_%s_url' % photosize.name,
                    curry(self._get_SIZE_url, photosize=photosize))
            setattr(self, 'get_%s_path' % photosize.name,
                    curry(self._get_SIZE_path, photosize=photosize))

    def size_exists(self, photosize):
        func = getattr(self, "get_%s_path" % photosize.name, None)
        if func is not None:
            if os.path.isfile(func()):
                return True
        return False

    def create_size(self, photosize):
        if self.size_exists(photosize):
            return
        if not os.path.isdir(self.cache_path()):
            os.makedirs(self.cache_path())
        try:
            im = Image.open(self.get_image_filename())
        except IOError:
            return
        if im.size == photosize.size():
            shutil.copy(self.get_image_filename(),
                        self._get_SIZE_path(photosize))
            return
        cur_width, cur_height = im.size
        new_width, new_height = photosize.size()
        if photosize.crop:
            ratio = max(float(new_width)/cur_width,float(new_height)/cur_height)
            x = (cur_width * ratio)
            y = (cur_height * ratio)
            xd = abs(new_width - x)
            yd = abs(new_height - y)
            x_diff = int(xd / 2)
            y_diff = int(yd / 2)
            if self.crop_from == 'top':
                box = (int(x_diff), 0, int(x_diff+new_width), new_height)
            elif self.crop_from == 'left':
                box = (0, int(y_diff), new_width, int(y_diff+new_height))
            elif self.crop_from == 'bottom':
                box = (int(x_diff), int(yd), int(x_diff+new_width), int(y)) # y - yd = new_height
            elif self.crop_from == 'right':
                box = (int(xd), int(y_diff), int(x), int(y_diff+new_height)) # x - xd = new_width
            else:
                box = (int(x_diff), int(y_diff), int(x_diff+new_width), int(y_diff+new_height))
            resized = im.resize((int(x), int(y)), Image.ANTIALIAS).crop(box)
        else:
            if not new_width == 0 and not new_height == 0:
                if cur_width > cur_height:
                    ratio = float(new_width)/cur_width
                else:
                    ratio = float(new_height)/cur_height
            else:
                if new_width == 0:
                    ratio = float(new_height)/cur_height
                else:
                    ratio = float(new_width)/cur_width
            resized = im.resize((int(cur_width*ratio), int(cur_height*ratio)), Image.ANTIALIAS)

        # Apply effect if found
        if self.effect is not None:
            resized = self.effect.process(resized)
        elif photosize.effect is not None:
            resized = photosize.effect.process(resized)

        # save resized file
        resized_filename = getattr(self, "get_%s_path" % photosize.name)()
        try:
            if im.format == 'JPEG':
                resized.save(resized_filename, 'JPEG', quality=int(photosize.quality), optimize=True)
            else:
                resized.save(resized_filename)
        except IOError, e:
            if os.path.isfile(resized_filename):
                os.unlink(resized_filename)
            raise e

    def remove_size(self, photosize, remove_dirs=True):
        if not self.size_exists(photosize):
            return
        filename = getattr(self, "get_%s_path" % photosize.name)()
        if os.path.isfile(filename):
            os.remove(filename)
        if remove_dirs:
            self.remove_cache_dirs()

    def clear_cache(self):
        cache = PhotoSizeCache()
        for photosize in cache.sizes.values():
            self.remove_size(photosize, False)
        self.remove_cache_dirs()

    def pre_cache(self):
        cache = PhotoSizeCache()
        for photosize in cache.sizes.values():
            if photosize.pre_cache:
                self.create_size(photosize)

    def remove_cache_dirs(self):
        try:
            os.removedirs(self.cache_path())
        except:
            pass

    def save(self):
        if self.date_taken is None:
            exif_date = self.EXIF.get('EXIF DateTimeOriginal', None)
            if exif_date is not None:
                d, t = str.split(exif_date.values)
                year, month, day = d.split(':')
                hour, minute, second = t.split(':')
                self.date_taken = datetime(int(year), int(month), int(day),
                                           int(hour), int(minute), int(second))
            else:
                self.date_taken = datetime.now()
        if self._get_pk_val():
            self.clear_cache()
        super(Photo, self).save()
        self.pre_cache()

    def delete(self):
        super(Photo, self).delete()
        self.clear_cache()

    def public_galleries(self):
        """Return the public galleries to which this photo belongs."""
        return self.galleries.filter(is_public=True)


class PhotoEffect(models.Model):
    """ A pre-defined effect to apply to photos """
    name = models.CharField(max_length=30, unique=True)
    color = models.FloatField(default=1.0, help_text="A factor of 0.0 gives a black and white image, a factor of 1.0 gives the original image.")
    brightness = models.FloatField(default=1.0, help_text="A factor of 0.0 gives a black image, a factor of 1.0 gives the original image.")
    contrast = models.FloatField(default=1.0, help_text="A factor of 0.0 gives a solid grey image, a factor of 1.0 gives the original image.")
    sharpness = models.FloatField(default=1.0, help_text="A factor of 0.0 gives a blurred image, a factor of 1.0 gives the original image.")
    filters = models.CharField(max_length=200, blank=True, help_text=image_filters_help_text)

    class Admin:
        list_display = ['name', 'color', 'brightness', 'contrast', 'sharpness', 'filters', 'admin_sample']

    def __unicode__(self):
        return self.name
        
    def __str__(self):
        return self.__unicode__()

    def sample_dir(self):
        return os.path.join(settings.MEDIA_ROOT, PHOTOLOGUE_DIR, 'samples')

    def sample_url(self):
        return settings.MEDIA_URL + '/'.join([PHOTOLOGUE_DIR, 'samples', '%s %s.jpg' % (self.name.lower(), 'sample')])

    def sample_filename(self):
        return os.path.join(self.sample_dir(), '%s %s.jpg' % (self.name.lower(), 'sample'))

    def create_sample(self):
        if not os.path.isdir(self.sample_dir()):
            os.makedirs(self.sample_dir())
        try:
            im = Image.open(SAMPLE_IMAGE_PATH)
        except IOError:
            raise IOError('Photologue was unable to open the sample image: %s.' % SAMPLE_IMAGE_PATH)
        im = self.process(im)
        im.save(self.sample_filename(), 'JPEG', quality=90, optimize=True)

    def admin_sample(self):
        return u'<img src="%s">' % self.sample_url()
    admin_sample.short_description = 'Sample'
    admin_sample.allow_tags = True

    def process(self, im):
        if im.mode != 'RGB':
            return im
        for name in ['Color', 'Brightness', 'Contrast', 'Sharpness']:
            factor = getattr(self, name.lower())
            if factor != 1.0:
                im = getattr(ImageEnhance, name)(im).enhance(factor)
        for name in self.filters.split('->'):
            image_filter = getattr(ImageFilter, name.upper(), None)
            if image_filter is not None:
                try:
                    im = im.filter(image_filter)
                except ValueError:
                    pass
        return im

    def save(self):
        try:
            os.remove(self.sample_filename())
        except:
            pass
        for photo in self.photos.all():
            photo.clear_cache()
            photo.pre_cache()
        for size in self.photo_sizes.all():
            size.clear_cache()
        super(PhotoEffect, self).save()
        self.create_sample()

    def delete(self):
        try:
            os.remove(self.sample_filename())
        except:
            pass
        super(PhotoEffect, self).delete()


class PhotoSize(models.Model):
    name = models.CharField(max_length=20, unique=True, help_text='Photo size name should contain only letters, numbers and underscores. Examples: "thumbnail", "display", "small", "main_page_widget".')
    width = models.PositiveIntegerField(default=0, help_text='Leave to size the image to the set height')
    height = models.PositiveIntegerField(default=0, help_text='Leave to size the image to the set width')
    quality = models.PositiveIntegerField(choices=JPEG_QUALITY_CHOICES, default=70,
                                          help_text="JPEG image quality.")
    crop = models.BooleanField("crop to fit?", default=False, help_text="If selected the image will be scaled and cropped to fit the supplied dimensions.")
    pre_cache = models.BooleanField('pre-cache?', default=False, help_text="If selected this photo size will be pre-cached as photos are added.")
    effect = models.ForeignKey('PhotoEffect', null=True, blank=True, related_name='photo_sizes')

    class Meta:
        ordering = ['width', 'height']

    class Admin:
        list_display = ('name', 'width', 'height', 'crop', 'pre_cache', 'effect')

    def __unicode__(self):
        return self.name
        
    def __str__(self):
        return self.__unicode__()

    def clear_cache(self):
        for photo in Photo.objects.all():
            photo.remove_size(self)
            if self.pre_cache:
                photo.create_size(self)
        PhotoSizeCache().reset()

    def save(self):
        if self.width + self.height == 0:
            raise ValueError("A PhotoSize must have a positive height or width.")
        super(PhotoSize, self).save()
        self.clear_cache()
        
    def delete(self):
        self.clear_cache()
        super(PhotoSize, self).delete()

    def size(self):
        return (self.width, self.height)


class PhotoSizeCache(object):
    __state = {"sizes": {}}

    def __init__(self):
        self.__dict__ = self.__state

    def reset(self):
        self.sizes = {}


# Set up the accessor methods
def add_methods(sender, instance, signal, *args, **kwargs):
    """ Adds methods to access sized images (urls, paths)

    after the photo models __init__ function completes,
    this method calls "add_accessor_methods" on each instance.
    """
    instance.add_accessor_methods()

# connect the add_accessor_methods function to the post_init signal
dispatcher.connect(add_methods, signal=signals.post_init, sender=Photo)
