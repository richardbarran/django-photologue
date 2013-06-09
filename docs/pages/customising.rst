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

    from photologue import PHOTOLOGUE_TEMPLATE_DIR
    TEMPLATE_DIRS = (
        ...other template folders...,
        PHOTOLOGUE_TEMPLATE_DIR
    )

The ``PHOTOLOGUE_TEMPLATE_DIR`` points to the directory above Photologue's normal
templates directory.  This means that ``path/to/photologue/template.html`` can also
be reached via ``templates/path/to/photologue/template.html``.

For example, to customise ``photologue/gallery_list.html``, you can have an implementation like::

    # Create your own photologue/gallery_list.html
    {% extends "templates/photologue/gallery_list.html" %}

    ... we are now extending the built-in gallery_list.html and we can override
    the content blocks that we want to customise ...


Third-party contributions
-------------------------
Photologue has a 'contrib' folder that includes some
useful tweaks to the base project. At the moment, we have just one contribution:

Bootstrap templates
~~~~~~~~~~~~~~~~~~~
Replaces the normal templates with a new set that work well with `Bootstrap <http://twitter.github.io/bootstrap/index.html>`_.

To use these, edit your ``TEMPLATE_DIRS`` setting::


    from photologue import PHOTOLOGUE_TEMPLATE_DIR
    TEMPLATE_DIRS = (
        ...
        os.path.join(PHOTOLOGUE_TEMPLATE_DIR, 'contrib/bootstrap/templates'),
        ... other folders containing Photologue templates should come after...
    )

The templates are incomplete - for example, we are missing templates for date-filtered galleries and photos.
Pull requests are welcome!
    