from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

APP_NAME = __name__.split('.')[0]

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--reset', '-r', action='store_true', dest='reset', help='Reset photo cache before generating'),
    )

    help = ('Manages Photologue cache file for the given sizes.')
    args = '[sizes]'

    requires_model_validation = True
    can_import_settings = True

    def handle(self, *args, **options):
        return create_cache(args, options)

def create_cache(sizes, options):
    """
    Creates the cache for the given files
    """
    from django.db.models.loading import get_model
    Photo = get_model(APP_NAME, 'Photo')
    PhotoSize = get_model(APP_NAME, 'PhotoSize')
    reset = options.get('reset', None)
    
    size_list = [size.strip(' ,') for size in sizes]
    
    if len(size_list) < 1:
        sizes = PhotoSize.objects.filter(pre_cache=True)
    else:
        sizes = PhotoSize.objects.filter(name__in=size_list)
        
    if not len(sizes):
        raise CommandError('No photo sizes were found.')
        
    print 'Caching photos, this may take a while...'
        
    for photo in Photo.objects.all():
       for photosize in sizes:
           print 'Creating %s size images' % photosize.name
           for photo in Photo.objects.all():
               if reset:
                    photo.remove_size(photosize)
               photo.create_size(photosize)


