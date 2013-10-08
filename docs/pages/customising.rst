#########################
Customising and extending
#########################


Extending templates
-------------------
Photologue comes with a set of basic templates to get you started quickly - you
can of course replace them with your own. That said, it is possible to extend the basic templates in 
your own project and override various blocks, for example to add css classes.
Often this will be enough.

The trick to extending the templates is not special to Photologue, it's used
in other projects such as `Oscar <https://django-oscar.readthedocs.org/en/latest/recipes/how_to_customise_templates.html>`_.

First, set up your template configuration as so::

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

    from photologue import PHOTOLOGUE_APP_DIR
    TEMPLATE_DIRS = (
        ...other template folders...,
        PHOTOLOGUE_APP_DIR
    )

The ``PHOTOLOGUE_APP_DIR`` points to the directory above Photologue's normal
templates directory.  This means that ``path/to/photologue/template.html`` can also
be reached via ``templates/path/to/photologue/template.html``.

For example, to customise ``photologue/gallery_list.html``, you can have an implementation like::

    # Create your own photologue/gallery_list.html
    {% extends "templates/photologue/gallery_list.html" %}

    ... we are now extending the built-in gallery_list.html and we can override
    the content blocks that we want to customise ...


Settings
--------
Photologue has several settings to customise behaviour; at present this part of the
documentation is unfortunately incomplete.

PHOTOLOGUE_USE_CKEDITOR
~~~~~~~~~~~~~~~~~~~~~~~

    Default: ``False``

If you have already installed `django-ckeditor <https://pypi.python.org/pypi/django-ckeditor>`_
then you can use to edit the TextArea fields of Gallery
and Photo in the admin. Simply set the setting to ``True``.


PHOTOLOGUE_GALLERY_PAGINATE_BY
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Default: ``20``

Number of galleries to display per page for GalleryListView.


PHOTOLOGUE_PHOTO_PAGINATE_BY
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Default: ``20``

Number of photos to display per page for PhotoListView.


PHOTOLOGUE_GALLERY_LATEST_LIMIT
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Default: ``None``

Default limit for gallery.latest


PHOTOLOGUE_GALLERY_SAMPLE_SIZE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Default: ``5``

Number of random images from the gallery to display.


PHOTOLOGUE_IMAGE_FIELD_MAX_LENGTH
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Default: ``100``

max_length setting for the ImageModel ImageField


PHOTOLOGUE_SAMPLE_IMAGE_PATH
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Default: ``os.path.join(os.path.dirname(__file__), 'res', 'sample.jpg'))``

Path to sample image


PHOTOLOGUE_MAXBLOCK
~~~~~~~~~~~~~~~~~~~
    
    Default: ``256 * 2 ** 10``

Modify image file buffer size.


PHOTOLOGUE_DIR
~~~~~~~~~~~~~~
    
    Default: ``'photologue'``

The relative path from your ``MEDIA_ROOT`` setting where Photologue will save image files. If your ``MEDIA_ROOT`` is set to "/home/user/media", photologue will upload your images to "/home/user/media/photologue"


PHOTOLOGUE_PATH
~~~~~~~~~~~~~~~

    Default: ``None``

Look for user function to define file paths. Specifies a "callable" that takes a model instance and the original uploaded filename and returns a relative path from your ``MEDIA_ROOT`` that the file will be saved. This function can be set directly.

For example you could use the following code in a util module::

    # myapp/utils.py:

    import os 

    def get_image_path(instance, filename): 
        return os.path.join('path', 'to', 'my', 'files', filename) 

Then set in settings::

    # settings.py:

    from utils import get_image_path
    
    PHOTOLOGUE_PATH = get_image_path

Or instead, pass a string path::

    # settings.py:

    PHOTOLOGUE_PATH = 'myapp.utils.get_image_path'



Third-party contributions
-------------------------
Photologue has a 'contrib' folder that includes some
useful tweaks to the base project. At the moment, we have just one contribution:

Bootstrap templates
~~~~~~~~~~~~~~~~~~~
Replaces the normal templates with a new set that work well with `Bootstrap <http://twitter.github.io/bootstrap/index.html>`_.

To use these, edit your ``TEMPLATE_DIRS`` setting::


    from photologue import PHOTOLOGUE_APP_DIR
    TEMPLATE_DIRS = (
        ...
        os.path.join(PHOTOLOGUE_APP_DIR, 'contrib/bootstrap/templates'),
        ... other folders containing Photologue templates should come after...
    )

The templates are incomplete - for example, we are missing templates for date-filtered galleries and photos.
Pull requests are welcome!
    