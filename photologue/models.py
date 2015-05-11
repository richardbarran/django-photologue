import os
import random
from datetime import datetime
from inspect import isclass
import logging
from io import BytesIO
from importlib import import_module

from django.utils.timezone import now
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.utils.encoding import force_text, smart_str, filepath_to_uri
from django.utils.functional import curry
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import RegexValidator
from django.contrib.sites.models import Site

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
        raise ImportError(
            'Photologue was unable to import the Python Imaging Library. Please confirm it`s installed and available '
            'on your current Python path.')

from sortedm2m.fields import SortedManyToManyField

from .utils import EXIF
from .utils.reflection import add_reflection
from .utils.watermark import apply_watermark
from .managers import GalleryQuerySet, PhotoQuerySet

logger = logging.getLogger('photologue.models')

# Default limit for gallery.latest
LATEST_LIMIT = getattr(settings, 'PHOTOLOGUE_GALLERY_LATEST_LIMIT', None)

# Number of random images from the gallery to display.
SAMPLE_SIZE = getattr(settings, 'PHOTOLOGUE_GALLERY_SAMPLE_SIZE', 5)

# max_length setting for the ImageModel ImageField
IMAGE_FIELD_MAX_LENGTH = getattr(settings, 'PHOTOLOGUE_IMAGE_FIELD_MAX_LENGTH', 100)

# Path to sample image
SAMPLE_IMAGE_PATH = getattr(settings, 'PHOTOLOGUE_SAMPLE_IMAGE_PATH', os.path.join(
    os.path.dirname(__file__), 'res', 'sample.jpg'))

# Modify image file buffer size.
ImageFile.MAXBLOCK = getattr(settings, 'PHOTOLOGUE_MAXBLOCK', 256 * 2 ** 10)

# Photologue image path relative to media root
PHOTOLOGUE_DIR = getattr(settings, 'PHOTOLOGUE_DIR', 'photologue')

# Look for user function to define file paths
PHOTOLOGUE_PATH = getattr(settings, 'PHOTOLOGUE_PATH', None)
if PHOTOLOGUE_PATH is not None:
    if callable(PHOTOLOGUE_PATH):
        get_storage_path = PHOTOLOGUE_PATH
    else:
        parts = PHOTOLOGUE_PATH.split('.')
        module_name = '.'.join(parts[:-1])
        module = import_module(module_name)
        get_storage_path = getattr(module, parts[-1])
else:
    def get_storage_path(instance, filename):
        return os.path.join(PHOTOLOGUE_DIR, 'photos', filename)

# Support CACHEDIR.TAG spec for backups for ignoring cache dir.
# See http://www.brynosaurus.com/cachedir/spec.html
PHOTOLOGUE_CACHEDIRTAG = os.path.join(PHOTOLOGUE_DIR, "photos", "cache", "CACHEDIR.TAG")
if not default_storage.exists(PHOTOLOGUE_CACHEDIRTAG):
    default_storage.save(PHOTOLOGUE_CACHEDIRTAG, ContentFile(
        "Signature: 8a477f597d28d172789f06886806bc55"))

# Exif Orientation values
# Value 0thRow	0thColumn
#   1	top     left
#   2	top     right
#   3	bottom	right
#   4	bottom	left
#   5	left	top
#   6	right   top
#   7	right   bottom
#   8	left    bottom

# Image Orientations (according to EXIF informations) that needs to be
# transposed and appropriate action
IMAGE_EXIF_ORIENTATION_MAP = {
    2: Image.FLIP_LEFT_RIGHT,
    3: Image.ROTATE_180,
    6: Image.ROTATE_270,
    8: Image.ROTATE_90,
}

# Quality options for JPEG images
JPEG_QUALITY_CHOICES = (
    (30, _('Very Low')),
    (40, _('Low')),
    (50, _('Medium-Low')),
    (60, _('Medium')),
    (70, _('Medium-High')),
    (80, _('High')),
    (90, _('Very High')),
)

# choices for new crop_anchor field in Photo
CROP_ANCHOR_CHOICES = (
    ('top', _('Top')),
    ('right', _('Right')),
    ('bottom', _('Bottom')),
    ('left', _('Left')),
    ('center', _('Center (Default)')),
)

IMAGE_TRANSPOSE_CHOICES = (
    ('FLIP_LEFT_RIGHT', _('Flip left to right')),
    ('FLIP_TOP_BOTTOM', _('Flip top to bottom')),
    ('ROTATE_90', _('Rotate 90 degrees counter-clockwise')),
    ('ROTATE_270', _('Rotate 90 degrees clockwise')),
    ('ROTATE_180', _('Rotate 180 degrees')),
)

WATERMARK_STYLE_CHOICES = (
    ('tile', _('Tile')),
    ('scale', _('Scale')),
)

# Prepare a list of image filters
filter_names = []
for n in dir(ImageFilter):
    klass = getattr(ImageFilter, n)
    if isclass(klass) and issubclass(klass, ImageFilter.BuiltinFilter) and \
            hasattr(klass, 'name'):
        filter_names.append(klass.__name__)
IMAGE_FILTERS_HELP_TEXT = _('Chain multiple filters using the following pattern "FILTER_ONE->FILTER_TWO->FILTER_THREE"'
                            '. Image filters will be applied in order. The following filters are available: %s.'
                            % (', '.join(filter_names)))

size_method_map = {}


class TagField(models.CharField):

    """Tags have been removed from Photologue, but the migrations still refer to them so this
    Tagfield definition is left here.
    """

    def __init__(self, **kwargs):
        default_kwargs = {'max_length': 255, 'blank': True}
        default_kwargs.update(kwargs)
        super(TagField, self).__init__(**default_kwargs)

    def get_internal_type(self):
        return 'CharField'


@python_2_unicode_compatible
class Gallery(models.Model):
    date_added = models.DateTimeField(_('date published'),
                                      default=now)
    title = models.CharField(_('title'),
                             max_length=50,
                             unique=True)
    slug = models.SlugField(_('title slug'),
                            unique=True,
                            help_text=_('A "slug" is a unique URL-friendly title for an object.'))
    description = models.TextField(_('description'),
                                   blank=True)
    is_public = models.BooleanField(_('is public'),
                                    default=True,
                                    help_text=_('Public galleries will be displayed '
                                                'in the default views.'))
    photos = SortedManyToManyField('Photo',
                                   related_name='galleries',
                                   verbose_name=_('photos'),
                                   blank=True)
    sites = models.ManyToManyField(Site, verbose_name=_(u'sites'),
                                   blank=True)

    objects = GalleryQuerySet.as_manager()

    class Meta:
        ordering = ['-date_added']
        get_latest_by = 'date_added'
        verbose_name = _('gallery')
        verbose_name_plural = _('galleries')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('photologue:pl-gallery', args=[self.slug])

    def latest(self, limit=LATEST_LIMIT, public=True):
        if not limit:
            limit = self.photo_count()
        if public:
            return self.public()[:limit]
        else:
            return self.photos.filter(sites__id=settings.SITE_ID)[:limit]

    def sample(self, count=None, public=True):
        """Return a sample of photos, ordered at random.
        If the 'count' is not specified, it will return a number of photos
        limited by the GALLERY_SAMPLE_SIZE setting.
        """
        if not count:
            count = SAMPLE_SIZE
        if count > self.photo_count():
            count = self.photo_count()
        if public:
            photo_set = self.public()
        else:
            photo_set = self.photos.filter(sites__id=settings.SITE_ID)
        return random.sample(set(photo_set), count)

    def photo_count(self, public=True):
        """Return a count of all the photos in this gallery."""
        if public:
            return self.public().count()
        else:
            return self.photos.filter(sites__id=settings.SITE_ID).count()
    photo_count.short_description = _('count')

    def public(self):
        """Return a queryset of all the public photos in this gallery."""
        return self.photos.is_public().filter(sites__id=settings.SITE_ID)

    def orphaned_photos(self):
        """
        Return all photos that belong to this gallery but don't share the
        gallery's site.
        """
        return self.photos.filter(is_public=True)\
                          .exclude(sites__id__in=self.sites.all())


class ImageModel(models.Model):
    image = models.ImageField(_('image'),
                              max_length=IMAGE_FIELD_MAX_LENGTH,
                              upload_to=get_storage_path)
    date_taken = models.DateTimeField(_('date taken'),
                                      null=True,
                                      blank=True,
                                      editable=False)
    view_count = models.PositiveIntegerField(_('view count'),
                                             default=0,
                                             editable=False)
    crop_from = models.CharField(_('crop from'),
                                 blank=True,
                                 max_length=10,
                                 default='center',
                                 choices=CROP_ANCHOR_CHOICES)
    effect = models.ForeignKey('PhotoEffect',
                               null=True,
                               blank=True,
                               related_name="%(class)s_related",
                               verbose_name=_('effect'))

    class Meta:
        abstract = True

    @property
    def EXIF(self):
        try:
            f = self.image.storage.open(self.image.name, 'rb')
            tags = EXIF.process_file(f)
            f.close()
            return tags
        except:
            try:
                f = self.image.storage.open(self.image.name, 'rb')
                tags = EXIF.process_file(f, details=False)
                f.close()
                return tags
            except:
                return {}

    def admin_thumbnail(self):
        func = getattr(self, 'get_admin_thumbnail_url', None)
        if func is None:
            return _('An "admin_thumbnail" photo size has not been defined.')
        else:
            if hasattr(self, 'get_absolute_url'):
                return u'<a href="%s"><img src="%s"></a>' % \
                    (self.get_absolute_url(), func())
            else:
                return u'<a href="%s"><img src="%s"></a>' % \
                    (self.image.url, func())
    admin_thumbnail.short_description = _('Thumbnail')
    admin_thumbnail.allow_tags = True

    def cache_path(self):
        return os.path.join(os.path.dirname(self.image.name), "cache")

    def cache_url(self):
        return '/'.join([os.path.dirname(self.image.url), "cache"])

    def image_filename(self):
        return os.path.basename(force_text(self.image.name))

    def _get_filename_for_size(self, size):
        size = getattr(size, 'name', size)
        base, ext = os.path.splitext(self.image_filename())
        return ''.join([base, '_', size, ext])

    def _get_SIZE_photosize(self, size):
        return PhotoSizeCache().sizes.get(size)

    def _get_SIZE_size(self, size):
        photosize = PhotoSizeCache().sizes.get(size)
        if not self.size_exists(photosize):
            self.create_size(photosize)
        return Image.open(self.image.storage.open(
            self._get_SIZE_filename(size))).size

    def _get_SIZE_url(self, size):
        photosize = PhotoSizeCache().sizes.get(size)
        if not self.size_exists(photosize):
            self.create_size(photosize)
        if photosize.increment_count:
            self.increment_count()
        return '/'.join([
            self.cache_url(),
            filepath_to_uri(self._get_filename_for_size(photosize.name))])

    def _get_SIZE_filename(self, size):
        photosize = PhotoSizeCache().sizes.get(size)
        return smart_str(os.path.join(self.cache_path(),
                                      self._get_filename_for_size(photosize.name)))

    def increment_count(self):
        self.view_count += 1
        models.Model.save(self)

    def __getattr__(self, name):
        global size_method_map
        if not size_method_map:
            init_size_method_map()
        di = size_method_map.get(name, None)
        if di is not None:
            result = curry(getattr(self, di['base_name']), di['size'])
            setattr(self, name, result)
            return result
        else:
            raise AttributeError

    def size_exists(self, photosize):
        func = getattr(self, "get_%s_filename" % photosize.name, None)
        if func is not None:
            if self.image.storage.exists(func()):
                return True
        return False

    def resize_image(self, im, photosize):
        cur_width, cur_height = im.size
        new_width, new_height = photosize.size
        if photosize.crop:
            ratio = max(float(new_width) / cur_width, float(new_height) / cur_height)
            x = (cur_width * ratio)
            y = (cur_height * ratio)
            xd = abs(new_width - x)
            yd = abs(new_height - y)
            x_diff = int(xd / 2)
            y_diff = int(yd / 2)
            if self.crop_from == 'top':
                box = (int(x_diff), 0, int(x_diff + new_width), new_height)
            elif self.crop_from == 'left':
                box = (0, int(y_diff), new_width, int(y_diff + new_height))
            elif self.crop_from == 'bottom':
                # y - yd = new_height
                box = (int(x_diff), int(yd), int(x_diff + new_width), int(y))
            elif self.crop_from == 'right':
                # x - xd = new_width
                box = (int(xd), int(y_diff), int(x), int(y_diff + new_height))
            else:
                box = (int(x_diff), int(y_diff), int(x_diff + new_width), int(y_diff + new_height))
            im = im.resize((int(x), int(y)), Image.ANTIALIAS).crop(box)
        else:
            if not new_width == 0 and not new_height == 0:
                ratio = min(float(new_width) / cur_width,
                            float(new_height) / cur_height)
            else:
                if new_width == 0:
                    ratio = float(new_height) / cur_height
                else:
                    ratio = float(new_width) / cur_width
            new_dimensions = (int(round(cur_width * ratio)),
                              int(round(cur_height * ratio)))
            if new_dimensions[0] > cur_width or \
               new_dimensions[1] > cur_height:
                if not photosize.upscale:
                    return im
            im = im.resize(new_dimensions, Image.ANTIALIAS)
        return im

    def create_size(self, photosize):
        if self.size_exists(photosize):
            return
        try:
            im = Image.open(self.image.storage.open(self.image.name))
        except IOError:
            return
        # Save the original format
        im_format = im.format
        # Apply effect if found
        if self.effect is not None:
            im = self.effect.pre_process(im)
        elif photosize.effect is not None:
            im = photosize.effect.pre_process(im)
        # Resize/crop image
        if im.size != photosize.size and photosize.size != (0, 0):
            im = self.resize_image(im, photosize)
        # Rotate if found & necessary
        if 'Image Orientation' in self.EXIF and \
                self.EXIF.get('Image Orientation').values[0] in IMAGE_EXIF_ORIENTATION_MAP:
            im = im.transpose(
                IMAGE_EXIF_ORIENTATION_MAP[self.EXIF.get('Image Orientation').values[0]])
        # Apply watermark if found
        if photosize.watermark is not None:
            im = photosize.watermark.post_process(im)
        # Apply effect if found
        if self.effect is not None:
            im = self.effect.post_process(im)
        elif photosize.effect is not None:
            im = photosize.effect.post_process(im)
        # Save file
        im_filename = getattr(self, "get_%s_filename" % photosize.name)()
        try:
            buffer = BytesIO()
            if im_format != 'JPEG':
                im.save(buffer, im_format)
            else:
                im.save(buffer, 'JPEG', quality=int(photosize.quality),
                        optimize=True)
            buffer_contents = ContentFile(buffer.getvalue())
            self.image.storage.save(im_filename, buffer_contents)
        except IOError as e:
            if self.image.storage.exists(im_filename):
                self.image.storage.delete(im_filename)
            raise e

    def remove_size(self, photosize, remove_dirs=True):
        if not self.size_exists(photosize):
            return
        filename = getattr(self, "get_%s_filename" % photosize.name)()
        if self.image.storage.exists(filename):
            self.image.storage.delete(filename)

    def clear_cache(self):
        cache = PhotoSizeCache()
        for photosize in cache.sizes.values():
            self.remove_size(photosize, False)

    def pre_cache(self):
        cache = PhotoSizeCache()
        for photosize in cache.sizes.values():
            if photosize.pre_cache:
                self.create_size(photosize)

    def __init__(self, *args, **kwargs):
        super(ImageModel, self).__init__(*args, **kwargs)
        self._old_image = self.image

    def save(self, *args, **kwargs):
        if self.date_taken is None:
            try:
                exif_date = self.EXIF.get('EXIF DateTimeOriginal', None)
                if exif_date is not None:
                    d, t = str.split(exif_date.values)
                    year, month, day = d.split(':')
                    hour, minute, second = t.split(':')
                    self.date_taken = datetime(int(year), int(month), int(day),
                                               int(hour), int(minute), int(second))
            except:
                pass
        if self.date_taken is None:
            self.date_taken = now()
        if self._get_pk_val() and (self._old_image != self.image):
            self.clear_cache()
        super(ImageModel, self).save(*args, **kwargs)
        self.pre_cache()

    def delete(self):
        assert self._get_pk_val() is not None, \
            "%s object can't be deleted because its %s attribute is set to None." % \
            (self._meta.object_name, self._meta.pk.attname)
        self.clear_cache()
        # Files associated to a FileField have to be manually deleted:
        # https://docs.djangoproject.com/en/dev/releases/1.3/#deleting-a-model-doesn-t-delete-associated-files
        # http://haineault.com/blog/147/
        # The data loss scenarios mentioned in the docs hopefully do not apply
        # to Photologue!
        super(ImageModel, self).delete()
        self.image.storage.delete(self.image.name)


@python_2_unicode_compatible
class Photo(ImageModel):
    title = models.CharField(_('title'),
                             max_length=60,
                             unique=True)
    slug = models.SlugField(_('slug'),
                            unique=True,
                            help_text=_('A "slug" is a unique URL-friendly title for an object.'))
    caption = models.TextField(_('caption'),
                               blank=True)
    date_added = models.DateTimeField(_('date added'),
                                      default=now)
    is_public = models.BooleanField(_('is public'),
                                    default=True,
                                    help_text=_('Public photographs will be displayed in the default views.'))
    sites = models.ManyToManyField(Site, verbose_name=_(u'sites'),
                                   blank=True)

    objects = PhotoQuerySet.as_manager()

    class Meta:
        ordering = ['-date_added']
        get_latest_by = 'date_added'
        verbose_name = _("photo")
        verbose_name_plural = _("photos")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super(Photo, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('photologue:pl-photo', args=[self.slug])

    def public_galleries(self):
        """Return the public galleries to which this photo belongs."""
        return self.galleries.filter(is_public=True)

    def get_previous_in_gallery(self, gallery):
        """Find the neighbour of this photo in the supplied gallery.
        We assume that the gallery and all its photos are on the same site.
        """
        if not self.is_public:
            raise ValueError('Cannot determine neighbours of a non-public photo.')
        photos = gallery.photos.is_public()
        if self not in photos:
            raise ValueError('Photo does not belong to gallery.')
        previous = None
        for photo in photos:
            if photo == self:
                return previous
            previous = photo

    def get_next_in_gallery(self, gallery):
        """Find the neighbour of this photo in the supplied gallery.
        We assume that the gallery and all its photos are on the same site.
        """
        if not self.is_public:
            raise ValueError('Cannot determine neighbours of a non-public photo.')
        photos = gallery.photos.is_public()
        if self not in photos:
            raise ValueError('Photo does not belong to gallery.')
        matched = False
        for photo in photos:
            if matched:
                return photo
            if photo == self:
                matched = True
        return None


@python_2_unicode_compatible
class BaseEffect(models.Model):
    name = models.CharField(_('name'),
                            max_length=30,
                            unique=True)
    description = models.TextField(_('description'),
                                   blank=True)

    class Meta:
        abstract = True

    def sample_dir(self):
        return os.path.join(PHOTOLOGUE_DIR, 'samples')

    def sample_url(self):
        return settings.MEDIA_URL + '/'.join([PHOTOLOGUE_DIR, 'samples', '%s %s.jpg' % (self.name.lower(), 'sample')])

    def sample_filename(self):
        return os.path.join(self.sample_dir(), '%s %s.jpg' % (self.name.lower(), 'sample'))

    def create_sample(self):
        try:
            im = Image.open(SAMPLE_IMAGE_PATH)
        except IOError:
            raise IOError(
                'Photologue was unable to open the sample image: %s.' % SAMPLE_IMAGE_PATH)
        im = self.process(im)
        buffer = BytesIO()
        im.save(buffer, 'JPEG', quality=90, optimize=True)
        buffer_contents = ContentFile(buffer.getvalue())
        default_storage.save(self.sample_filename(), buffer_contents)

    def admin_sample(self):
        return u'<img src="%s">' % self.sample_url()
    admin_sample.short_description = 'Sample'
    admin_sample.allow_tags = True

    def pre_process(self, im):
        return im

    def post_process(self, im):
        return im

    def process(self, im):
        im = self.pre_process(im)
        im = self.post_process(im)
        return im

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            default_storage.delete(self.sample_filename())
        except:
            pass
        models.Model.save(self, *args, **kwargs)
        self.create_sample()
        for size in self.photo_sizes.all():
            size.clear_cache()
        # try to clear all related subclasses of ImageModel
        for prop in [prop for prop in dir(self) if prop[-8:] == '_related']:
            for obj in getattr(self, prop).all():
                obj.clear_cache()
                obj.pre_cache()

    def delete(self):
        try:
            default_storage.delete(self.sample_filename())
        except:
            pass
        models.Model.delete(self)


class PhotoEffect(BaseEffect):

    """ A pre-defined effect to apply to photos """
    transpose_method = models.CharField(_('rotate or flip'),
                                        max_length=15,
                                        blank=True,
                                        choices=IMAGE_TRANSPOSE_CHOICES)
    color = models.FloatField(_('color'),
                              default=1.0,
                              help_text=_('A factor of 0.0 gives a black and white image, a factor of 1.0 gives the '
                                          'original image.'))
    brightness = models.FloatField(_('brightness'),
                                   default=1.0,
                                   help_text=_('A factor of 0.0 gives a black image, a factor of 1.0 gives the '
                                               'original image.'))
    contrast = models.FloatField(_('contrast'),
                                 default=1.0,
                                 help_text=_('A factor of 0.0 gives a solid grey image, a factor of 1.0 gives the '
                                             'original image.'))
    sharpness = models.FloatField(_('sharpness'),
                                  default=1.0,
                                  help_text=_('A factor of 0.0 gives a blurred image, a factor of 1.0 gives the '
                                              'original image.'))
    filters = models.CharField(_('filters'),
                               max_length=200,
                               blank=True,
                               help_text=_(IMAGE_FILTERS_HELP_TEXT))
    reflection_size = models.FloatField(_('size'),
                                        default=0,
                                        help_text=_('The height of the reflection as a percentage of the orignal '
                                                    'image. A factor of 0.0 adds no reflection, a factor of 1.0 adds a'
                                                    ' reflection equal to the height of the orignal image.'))
    reflection_strength = models.FloatField(_('strength'),
                                            default=0.6,
                                            help_text=_('The initial opacity of the reflection gradient.'))
    background_color = models.CharField(_('color'),
                                        max_length=7,
                                        default="#FFFFFF",
                                        help_text=_('The background color of the reflection gradient. Set this to '
                                                    'match the background color of your page.'))

    class Meta:
        verbose_name = _("photo effect")
        verbose_name_plural = _("photo effects")

    def pre_process(self, im):
        if self.transpose_method != '':
            method = getattr(Image, self.transpose_method)
            im = im.transpose(method)
        if im.mode != 'RGB' and im.mode != 'RGBA':
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

    def post_process(self, im):
        if self.reflection_size != 0.0:
            im = add_reflection(im, bgcolor=self.background_color,
                                amount=self.reflection_size, opacity=self.reflection_strength)
        return im


class Watermark(BaseEffect):
    image = models.ImageField(_('image'),
                              upload_to=PHOTOLOGUE_DIR + "/watermarks")
    style = models.CharField(_('style'),
                             max_length=5,
                             choices=WATERMARK_STYLE_CHOICES,
                             default='scale')
    opacity = models.FloatField(_('opacity'),
                                default=1,
                                help_text=_("The opacity of the overlay."))

    class Meta:
        verbose_name = _('watermark')
        verbose_name_plural = _('watermarks')

    def delete(self):
        assert self._get_pk_val() is not None, "%s object can't be deleted because its %s attribute is set to None." \
            % (self._meta.object_name, self._meta.pk.attname)
        super(Watermark, self).delete()
        self.image.storage.delete(self.image.name)

    def post_process(self, im):
        mark = Image.open(self.image.storage.open(self.image.name))
        return apply_watermark(im, mark, self.style, self.opacity)


@python_2_unicode_compatible
class PhotoSize(models.Model):

    """About the Photosize name: it's used to create get_PHOTOSIZE_url() methods,
    so the name has to follow the same restrictions as any Python method name,
    e.g. no spaces or non-ascii characters."""

    name = models.CharField(_('name'),
                            max_length=40,
                            unique=True,
                            help_text=_(
                                'Photo size name should contain only letters, numbers and underscores. Examples: '
                                '"thumbnail", "display", "small", "main_page_widget".'),
                            validators=[RegexValidator(regex='^[a-z0-9_]+$',
                                                       message='Use only plain lowercase letters (ASCII), numbers and '
                                                       'underscores.'
                                                       )]
                            )
    width = models.PositiveIntegerField(_('width'),
                                        default=0,
                                        help_text=_(
                                            'If width is set to "0" the image will be scaled to the supplied height.'))
    height = models.PositiveIntegerField(_('height'),
                                         default=0,
                                         help_text=_(
        'If height is set to "0" the image will be scaled to the supplied width'))
    quality = models.PositiveIntegerField(_('quality'),
                                          choices=JPEG_QUALITY_CHOICES,
                                          default=70,
                                          help_text=_('JPEG image quality.'))
    upscale = models.BooleanField(_('upscale images?'),
                                  default=False,
                                  help_text=_('If selected the image will be scaled up if necessary to fit the '
                                              'supplied dimensions. Cropped sizes will be upscaled regardless of this '
                                              'setting.')
                                  )
    crop = models.BooleanField(_('crop to fit?'),
                               default=False,
                               help_text=_('If selected the image will be scaled and cropped to fit the supplied '
                                           'dimensions.'))
    pre_cache = models.BooleanField(_('pre-cache?'),
                                    default=False,
                                    help_text=_('If selected this photo size will be pre-cached as photos are added.'))
    increment_count = models.BooleanField(_('increment view count?'),
                                          default=False,
                                          help_text=_('If selected the image\'s "view_count" will be incremented when '
                                                      'this photo size is displayed.'))
    effect = models.ForeignKey('PhotoEffect',
                               null=True,
                               blank=True,
                               related_name='photo_sizes',
                               verbose_name=_('photo effect'))
    watermark = models.ForeignKey('Watermark',
                                  null=True,
                                  blank=True,
                                  related_name='photo_sizes',
                                  verbose_name=_('watermark image'))

    class Meta:
        ordering = ['width', 'height']
        verbose_name = _('photo size')
        verbose_name_plural = _('photo sizes')

    def __str__(self):
        return self.name

    def clear_cache(self):
        for cls in ImageModel.__subclasses__():
            for obj in cls.objects.all():
                obj.remove_size(self)
                if self.pre_cache:
                    obj.create_size(self)
        PhotoSizeCache().reset()

    def clean(self):
        if self.crop is True:
            if self.width == 0 or self.height == 0:
                raise ValidationError(
                    _("Can only crop photos if both width and height dimensions are set."))

    def save(self, *args, **kwargs):
        super(PhotoSize, self).save(*args, **kwargs)
        PhotoSizeCache().reset()
        self.clear_cache()

    def delete(self):
        assert self._get_pk_val() is not None, "%s object can't be deleted because its %s attribute is set to None." \
            % (self._meta.object_name, self._meta.pk.attname)
        self.clear_cache()
        super(PhotoSize, self).delete()

    def _get_size(self):
        return (self.width, self.height)

    def _set_size(self, value):
        self.width, self.height = value
    size = property(_get_size, _set_size)


class PhotoSizeCache(object):
    __state = {"sizes": {}}

    def __init__(self):
        self.__dict__ = self.__state
        if not len(self.sizes):
            sizes = PhotoSize.objects.all()
            for size in sizes:
                self.sizes[size.name] = size

    def reset(self):
        global size_method_map
        size_method_map = {}
        self.sizes = {}


def init_size_method_map():
    global size_method_map
    for size in PhotoSizeCache().sizes.keys():
        size_method_map['get_%s_size' % size] = \
            {'base_name': '_get_SIZE_size', 'size': size}
        size_method_map['get_%s_photosize' % size] = \
            {'base_name': '_get_SIZE_photosize', 'size': size}
        size_method_map['get_%s_url' % size] = \
            {'base_name': '_get_SIZE_url', 'size': size}
        size_method_map['get_%s_filename' % size] = \
            {'base_name': '_get_SIZE_filename', 'size': size}


def add_default_site(instance, created, **kwargs):
    """
    Called via Django's signals when an instance is created.
    In case PHOTOLOGUE_MULTISITE is False, the current site (i.e.
    ``settings.SITE_ID``) will always be added to the site relations if none are
    present.
    """
    if not created:
        return
    if getattr(settings, 'PHOTOLOGUE_MULTISITE', False):
        return
    if instance.sites.exists():
        return
    instance.sites.add(Site.objects.get_current())
post_save.connect(add_default_site, sender=Gallery)
post_save.connect(add_default_site, sender=Photo)
