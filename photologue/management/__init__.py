from django.db.models.signals import post_syncdb
from django.db.models.loading import get_model

from commands.plcreatesize import create_size
from commands.utils import get_response

APP_NAME = __name__.split('.')[0]

try:
    models = __import__(APP_NAME).models
except:
    models = None
    
PhotoEffect = get_model(APP_NAME, 'PhotoEffect')

def post_sync(sender, app, created_models, verbosity, interactive, **kwargs):
    if interactive:
        print '\nInitializing %s' % APP_NAME
        msg = '\nPhotologue requires a specific photo size to display thumbnail previews in the Django admin application.\nWould you like to generate this size now? (yes, no):'
        if get_response(msg, lambda inp: inp == 'yes', False):
            admin_thumbnail = create_size('admin_thumbnail', width=100, height=75, crop=True, pre_cache=True)
            msg = 'Would you like to apply a sample enhancement effect to your admin thumbnails? (yes, no):'
            if get_response(msg, lambda inp: inp == 'yes', False):
                effect, created = models.PhotoEffect.objects.get_or_create(name='Enhance Thumbnail', description="Increases sharpness and contrast. Works well for smaller image sizes such as thumbnails.", contrast=1.2, sharpness=1.3)
                admin_thumbnail.effect = effect
                admin_thumbnail.save()                
        msg = '\nPhotologue comes with a set of templates for setting up a complete photo gallery. These templates require you to define both a "thumbnail" and "display" size.\nWould you like to define them now? (yes, no):'
        if get_response(msg, lambda inp: inp == 'yes', False):
            thumbnail = create_size('thumbnail', width=100, height=75)
            display = create_size('display', width=400, increment_count=True)
            msg = 'Would you like to apply a sample reflection effect to your display images? (yes, no):'
            if get_response(msg, lambda inp: inp == 'yes', False):
                effect, created = models.PhotoEffect.objects.get_or_create(name='Display Reflection', description="Generates a reflection with a white background", reflection_size=0.4)
                display.effect = effect
                display.save()

post_syncdb.connect(post_sync, sender=models)
