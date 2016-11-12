from django.core.management.base import BaseCommand, CommandError
from photologue.models import PhotoSize, ImageModel


class Command(BaseCommand):
    help = 'Clears the Photologue cache for the given sizes.'

    def add_arguments(self, parser):
        parser.add_argument('sizes',
                            nargs='*',
                            type=str,
                            help='Name of the photosize.')

    def handle(self, *args, **options):
        sizes = options['sizes']

        if not sizes:
            photosizes = PhotoSize.objects.all()
        else:
            photosizes = PhotoSize.objects.filter(name__in=sizes)

        if not len(photosizes):
            raise CommandError('No photo sizes were found.')

        print('Flushing cache...')

        for cls in ImageModel.__subclasses__():
            for photosize in photosizes:
                print('Flushing %s size images' % photosize.name)
                for obj in cls.objects.all():
                    obj.remove_size(photosize)
