import os
import datetime
try:
    from django.utils.text import slugify
except ImportError:
    # Django 1.4
    from django.template.defaultfilters import slugify
from django.utils.timezone import utc
from django.utils import six
from django.conf import settings
try:
    import factory
except ImportError:
    raise ImportError("No module named factory. To run photologue's tests you need to install factory-boy.")

from ..models import Gallery, Photo, PhotoSize

RES_DIR = os.path.join(os.path.dirname(__file__), '../res')
LANDSCAPE_IMAGE_PATH = os.path.join(RES_DIR, 'test_photologue_landscape.jpg')
PORTRAIT_IMAGE_PATH = os.path.join(RES_DIR, 'test_photologue_portrait.jpg')
SQUARE_IMAGE_PATH = os.path.join(RES_DIR, 'test_photologue_square.jpg')
QUOTING_IMAGE_PATH = os.path.join(RES_DIR, 'test_photologue_&quoting.jpg')


class GalleryFactory(factory.django.DjangoModelFactory):

    FACTORY_FOR = Gallery

    title = factory.Sequence(lambda n: 'gallery{0:0>3}'.format(n))
    title_slug = factory.LazyAttribute(lambda a: slugify(six.text_type(a.title)))

    @factory.sequence
    def date_added(n):
        # Have to cater projects being non-timezone aware.
        if settings.USE_TZ:
            sample_date = datetime.datetime(year=2011, month=12, day=23, hour=17, minute=40, tzinfo=utc)
        else:
            sample_date = datetime.datetime(year=2011, month=12, day=23, hour=17, minute=40)
        return sample_date + datetime.timedelta(minutes=n)


class PhotoFactory(factory.django.DjangoModelFactory):

    """Note: after creating Photo instances for tests, remember to manually 
    delete them.
    """

    FACTORY_FOR = Photo

    title = factory.Sequence(lambda n: 'photo{0:0>3}'.format(n))
    title_slug = factory.LazyAttribute(lambda a: slugify(six.text_type(a.title)))
    image = factory.django.ImageField(from_path=LANDSCAPE_IMAGE_PATH)

    @factory.sequence
    def date_added(n):
        # Have to cater projects being non-timezone aware.
        if settings.USE_TZ:
            sample_date = datetime.datetime(year=2011, month=12, day=23, hour=17, minute=40, tzinfo=utc)
        else:
            sample_date = datetime.datetime(year=2011, month=12, day=23, hour=17, minute=40)
        return sample_date + datetime.timedelta(minutes=n)


class PhotoSizeFactory(factory.django.DjangoModelFactory):

    FACTORY_FOR = PhotoSize

    name = factory.Sequence(lambda n: 'name{0:0>3}'.format(n))
