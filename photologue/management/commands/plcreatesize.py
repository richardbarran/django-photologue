from django.core.management.base import BaseCommand
from photologue.management.commands import create_photosize


class Command(BaseCommand):
    help = ('Creates a new Photologue photo size interactively.')
    requires_model_validation = True
    can_import_settings = True

    def add_arguments(self, parser):
        parser.add_argument('name',
                            type=str,
                            help='Name of the new photo size')

    def handle(self, *args, **options):
        create_photosize(options['name'])
