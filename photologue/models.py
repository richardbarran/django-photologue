import os
import shutil
import zipfile

from datetime import datetime
import Image
import ImageFile
import ImageFilter
from inspect import isclass

from django.db import models
from django.db.models import signals
from django.conf import settings
from django.utils.functional import curry
from django.core.validators import ValidationError
from django.core.urlresolvers import reverse
from django.dispatch import dispatcher
from django.template.defaultfilters import slugify

from util import EXIF

# Photologue image path relative to media root
PHOTOLOGUE_DIR = getattr(settings, 'PHOTOLOGUE_DIR', 'photologue')

# Modify image file buffer size if set, otherwise keep PIL default (64k)
ImageFile.MAXBLOCK = getattr(settings, 'PHOTOLOGUE_MAXBLOCK', 256*1024)

# Prepare a list of image filters
IMAGE_FILTER_CHOICES = []
for n in dir(ImageFilter):
    klass = getattr(ImageFilter, n)
    if isclass(klass) and issubclass(klass, ImageFilter.BuiltinFilter) and \
       hasattr(klass, 'name'):
        IMAGE_FILTER_CHOICES.append((klass.__name__, klass.name))

# Quality options for JPEG images
JPEG_QUALITY_CHOICES = (
    (20, 'Very Low'),
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
)


class FilterSet(models.Model):
    name = models.CharField(max_length=20, unique=True)
    filters = models.ManyToManyField('PhotoFilter', related_name='filter_sets',
                                     help_text="Selected filters will be applied to all resized images")

    class Admin:
        pass

    def __unicode__(self):
        return self.name


class Gallery(models.Model):
    pub_date = models.DateTimeField("Date published", default=datetime.now)
    title = models.CharField(max_length=200)
    slug = models.SlugField(prepopulate_from=('title',),
                            help_text='A "Slug" is a unique URL-friendly title for an object.')
    description = models.TextField()
    is_public = models.BooleanField(default=True,
                                    help_text="Public galleries will be displayed in the default views.")
    photos = models.ManyToManyField('Photo', related_name='galleries')

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
    zip_file = models.FileField('Images file (.zip)',
                                upload_to=PHOTOLOGUE_DIR+"/temp",
                                help_text="Select a .zip file of images to upload into a new Gallery.")
    title_prefix = models.CharField(max_length=75,
                                    help_text="Photos will be titled using this prefix.")
    caption = models.TextField(help_text="Caption will be added to all photos.")
    description = models.TextField(blank=True,
                                   help_text="A description of this Gallery.")
    photographer = models.CharField(max_length=100, blank=True)
    info = models.TextField(blank=True,
                            help_text="Additional information about the photograph such as date taken, equipment used etc..")
    is_public = models.BooleanField(default=True,
                                    help_text="Uncheck this to make the uploaded gallery and included photographs private.")

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
            count = 0
            gallery = Gallery.objects.create(title=self.title_prefix,
                                             slug=slugify(self.title_prefix),
                                             description=self.description,
                                             is_public=self.is_public)
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
                                  is_public=self.is_public)
                    photo.save_image_file(filename, data)
                    gallery.photos.add(photo)
                    count = count + 1
            zip.close()


class Photo(models.Model):
    image = models.ImageField("Photograph", upload_to=PHOTOLOGUE_DIR+"/photos/%Y/%b/%d")
    pub_date = models.DateTimeField("Date published", default=datetime.now)
    title = models.CharField(max_length=80)
    slug = models.SlugField(prepopulate_from=('title',),
                            help_text='A "Slug" is a unique URL-friendly title for an object.')
    caption = models.TextField(blank=True)
    photographer = models.CharField(max_length=100, blank=True)
    date_taken = models.DateTimeField(null=True, blank=True)
    info = models.TextField(blank=True,
                            help_text="Additional information about the photograph such location, equipment used etc..")
    crop_from = models.CharField(blank=True, max_length=10,
                                 choices=CROP_ANCHOR_CHOICES)
    is_public = models.BooleanField(default=True,
                                    help_text="Public photographs will be displayed in the default views.")
    filter_set = models.ForeignKey('FilterSet', null=True, blank=True,
                                   help_text="This setting will override the photo size filter set for this photo.")

    class Meta:
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'

    class Admin:
        list_display = ('title', 'date_taken', 'pub_date', 'photographer',
                        'admin_thumbnail')
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
        func = getattr(self, 'get_thumbnail_url', None)
        if func is None:
            return 'A "thumbnail" photo size has not been defined.'
        else:
            return u'<a href="%s"><img src="%s"></a>' % \
                (self.get_absolute_url(), func())
    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True

    def __unicode__(self):
        return self.title

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
                    box = (int(x_diff), 0, int(x-x_diff), new_height)
            elif self.crop_from == 'left':
                    box = (0, int(y_diff), new_width, int(y-y_diff))
            elif self.crop_from == 'bottom':
                    box = (int(x_diff), int(yd), int(x-x_diff), int(y)) # y - yd = new_height
            elif self.crop_from == 'right':
                    box = (int(xd), int(y_diff), int(x), int(y-y_diff)) # x - xd = new_width
            else:
                    box = (int(x_diff), int(y_diff), int(x-x_diff), int(y-y_diff))
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
        if self.filter_set is not None:
            filter_set = self.filter_set.filters.all()
        elif photosize.filter_set is not None:
            filter_set = list(photosize.filter_set.filters.all())
        else:
            filter_set = None
        if filter_set is not None:
            for f in filter_set:
                filter = getattr(ImageFilter, f.name, None)
                if filter is not None:
                    try:
                        resized = resized.filter(filter)
                    except ValueError:
                        pass
        resized_filename = getattr(self, "get_%s_path" % photosize.name)()
        try:
            if im.format == 'JPEG':
                resized.save(resized_filename, 'JPEG', quality=photosize.quality,
                             optimize=True)
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
            try:
                os.removedirs(self.cache_path())
            except:
                pass

    def remove_set(self):
        cache = PhotoSizeCache()
        for photosize in cache.sizes.values():
            self.remove_size(photosize, False)
            try:
                os.removedirs(self.cache_path())
            except:
                pass

    def save(self):
        exif_date = self.EXIF.get('EXIF DateTimeOriginal', None)
        if exif_date is not None:
            d, t = str.split(exif_date.values)
            year, month, day = d.split(':')
            hour, minute, second = t.split(':')
            self.date_taken = datetime(int(year), int(month), int(day),
                                       int(hour), int(minute), int(second))
        else:
            self.date_taken = datetime.now()
        self.remove_set()
        super(Photo, self).save()

    def delete(self):
        super(Photo, self).delete()
        self.remove_set()

    def public_galleries(self):
        """Return the public galleries to which this photo belongs."""
        return self.galleries.filter(is_public=True)


class PhotoFilter(models.Model):
    name = models.CharField(max_length=25, unique=True,
                            choices=IMAGE_FILTER_CHOICES,
                            help_text="Select effect from the available image filters.")

    class Admin:
        pass

    def __unicode__(self):
        return self.get_name_display()


class PhotoSize(models.Model):
    name = models.CharField(max_length=20, unique=True, help_text='Examples: "thumbnail", "display", "small"')
    width = models.PositiveIntegerField(default=0,
                                        help_text='Leave to size the image to the set height')
    height = models.PositiveIntegerField(default=0,
                                         help_text='Leave to size the image to the set width')
    quality = models.PositiveIntegerField(choices=JPEG_QUALITY_CHOICES,
                                          default=70,
                                          help_text="JPEG image quality.")
    crop = models.BooleanField("Crop photo to fit?", default=False,
                               help_text="If selected the image will be scaled \
                                         and cropped to fit the supplied dimensions.")
    filter_set = models.ForeignKey('FilterSet', null=True, blank=True,
                                   help_text="Selected filters will be applied to all resized images")

    class Meta:
        ordering = ['width', 'height']

    class Admin:
        list_display = ('name', 'width', 'height', 'crop')

    def __unicode__(self):
        return self.name

    def _clear_caches(self):
        for photo in Photo.objects.all():
            photo.remove_size(self)
        PhotoSizeCache().reset()

    def save(self):
        if self.width + self.height == 0:
            raise ValueError("A PhotoSize must have a positive height or width.")
        self._clear_caches()
        super(PhotoSize, self).save()

    def delete(self):
        self._clear_caches()
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
