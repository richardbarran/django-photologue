import os

__version__ = '2.7.dev0'

PHOTOLOGUE_APP_DIR = os.path.dirname(os.path.abspath(__file__))


from django.core.exceptions import ImproperlyConfigured


def get_photo_model():
    "Return the Photo model that is active in this project"
    from django.conf import settings
    from django.db.models import get_model

    try:
        CUSTOM_PHOTO_MODEL = settings.CUSTOM_PHOTO_MODEL
    except AttributeError:
        CUSTOM_PHOTO_MODEL = 'photologue.Photo'

    try:
        app_label, model_name = CUSTOM_PHOTO_MODEL.split('.')
    except ValueError:
        raise ImproperlyConfigured("CUSTOM_PHOTO_MODEL must be of the form 'app_label.model_name'")
    photo_model = get_model(app_label, model_name)
    if photo_model is None:
        raise ImproperlyConfigured("CUSTOM_PHOTO_MODEL refers to model '%s' that has not been installed" % CUSTOM_PHOTO_MODEL)
    return photo_model
