##################################
Customisation: extending templates
##################################

Photologue comes with a set of basic templates to get you started quickly - you
can of course replace them with your own. That said, it is possible to extend the basic templates in 
your own project and override various blocks, for example to add css classes.
Often this will be enough.

The trick to extending the templates is not special to Photologue, it's used
in other projects such as `Oscar <https://django-oscar.readthedocs.org/en/latest/recipes/how_to_customise_templates.html>`_.

First, set up your template configuration as so:

.. code-block:: python

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

For example, to customise ``photologue/gallery_list.html``, you can have an implementation like:

.. code-block:: html+django

    # Create your own photologue/gallery_list.html
    {% extends "templates/photologue/gallery_list.html" %}

    ... we are now extending the built-in gallery_list.html and we can override
    the content blocks that we want to customise ...


