from django.utils.text import slugify
from django.utils.timezone import utc
from django.conf import settings

import os
import datetime

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
    title_slug = factory.LazyAttribute(lambda a: slugify(unicode(a.title)))
    # Have to cater projects being non-timezone aware.
    if settings.USE_TZ:
        date_added = datetime.datetime(year=2011, month=12, day=23, hour=17, minute=40, tzinfo=utc)
    else:
        date_added = datetime.datetime(year=2011, month=12, day=23, hour=17, minute=40)

class PhotoFactory(factory.django.DjangoModelFactory):

    FACTORY_FOR = Photo

    title = factory.Sequence(lambda n: 'photo{0:0>3}'.format(n))
    title_slug = factory.LazyAttribute(lambda a: slugify(unicode(a.title)))
    image = factory.django.ImageField(from_path=LANDSCAPE_IMAGE_PATH)
    if settings.USE_TZ:
        date_added = datetime.datetime(year=2011, month=12, day=23, hour=17, minute=40, tzinfo=utc)
    else:
        date_added = datetime.datetime(year=2011, month=12, day=23, hour=17, minute=40)

class PhotoSizeFactory(factory.django.DjangoModelFactory):

    FACTORY_FOR = PhotoSize

    name = factory.Sequence(lambda n: 'name{0:0>3}'.format(n))
