from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from utils import get_response

APP_NAME = __name__.split('.')[0]

class Command(BaseCommand):  
    help = ('Creates a new Photologue photo size interactively.')
    requires_model_validation = True
    can_import_settings = True

    def handle(self, args, **options):
        return _create_size(args)
        
def _create_size(name):
    create_size(name)

def create_size(name, width=0, height=0, crop=False, pre_cache=False, increment_count=False):
    from django.db.models.loading import get_model
    PhotoSize = get_model(APP_NAME, 'PhotoSize')
    try:
        size = PhotoSize.objects.get(name=name)
    except PhotoSize.DoesNotExist:
        size = PhotoSize(name=name)
    print '\nWe will now define the "%s" photo size:\n' % size
    w = get_response('Width (in pixels):', lambda inp: int(inp), width)
    h = get_response('Height (in pixels):', lambda inp: int(inp), height)
    c = get_response('Crop to fit? (yes, no):', lambda inp: inp == 'yes', crop)
    p = get_response('Pre-cache? (yes, no):', lambda inp: inp == 'yes', pre_cache)
    i = get_response('Increment count? (yes, no):', lambda inp: inp == 'yes', increment_count)
    size.width = w
    size.height = h
    size.crop = c
    size.pre_cache = p
    size.increment_count = i
    size.save()
    print '\nA "%s" photo size has been created.\n' % name
    return size
