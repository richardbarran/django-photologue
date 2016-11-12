from django.core.management.base import BaseCommand, CommandError
from photologue.models import PhotoSize, ImageModel


class Command(BaseCommand):

    help = 'Manages Photologue cache file for the given sizes.'

    def add_arguments(self, parser):
        parser.add_argument('sizes',
                            nargs='*',
                            type=str,
                            help='Name of the photosize.')
        parser.add_argument('--reset',
                            action='store_true',
                            default=False,
                            dest='reset',
                            help='Reset photo cache before generating.')

    def handle(self, *args, **options):
        reset = options['reset']
        sizes = options['sizes']

        if not sizes:
            photosizes = PhotoSize.objects.all()
        else:
            photosizes = PhotoSize.objects.filter(name__in=sizes)

        if not len(photosizes):
            raise CommandError('No photo sizes were found.')

        print('Caching photos, this may take a while...')

        for cls in ImageModel.__subclasses__():
            for photosize in photosizes:
                print('Cacheing %s size images' % photosize.name)
                for obj in cls.objects.all():
                    if reset:
                        obj.remove_size(photosize)
                    obj.create_size(photosize)
