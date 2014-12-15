.. _customising-models-label:

#####################
Customisation: Models
#####################

The photologue models can be extended to better suit your project. The technique described on this page
is not specific to Photologue - it can be applied to any 3rd party library. 

The models within Photologue cannot be directly modified (unlike, for example, Django's own User model).
There are a number of reasons behind this decision, including:

- If code within a project modifies directly the Photologue models' fields, it leaves the Photologue
  schema migrations in an ambiguous state.
- Likewise, model methods can no longer be trusted to behave as intended (as fields on which they
  depend may have been overridden).

However, it's easy to create new models linked by one-to-one relationships to Photologue's own
``Gallery`` and ``Photo`` models.

On this page we will show how you can add tags to the ``Gallery`` model. For this we will use
the popular 3rd party application `django-taggit <https://github.com/alex/django-taggit>`_.

.. note::

    The ``Gallery`` and ``Photo`` models currently have tag fields, however these are based on the
    abandonware `django-tagging <https://github.com/brosner/django-tagging>`_ application. Instead,
    tagging is being entirely removed from Photologue, as it is a non-core functionality of a
    gallery application, and is easy to add back in - as this page shows!

Create a customisation application
----------------------------------
For clarity, it's best to put our customisation code in a new application; let's call it
``photologue_custom``; create the application and add it to your ``INSTALLED_APPS`` setting.

Extending
---------

Within the ``photologue_custom`` application, we will edit 2 files:

Models.py
~~~~~~~~~

.. code-block:: python

    from django.db import models

    from taggit.managers import TaggableManager

    from photologue.models import Gallery


    class GalleryExtended(models.Model):

        # Link back to Photologue's Gallery model.
        gallery = models.OneToOneField(Gallery, related_name='extended')

        # This is the important bit - where we add in the tags.
        tags = TaggableManager(blank=True)

        # Boilerplate code to make a prettier display in the admin interface.
        class Meta:
            verbose_name = u'Extra fields'
            verbose_name_plural = u'Extra fields'

        def __str__(self):
            return self.gallery.title


Admin.py
~~~~~~~~

.. code-block:: python

    from django.contrib import admin

    from photologue.admin import GalleryAdmin as GalleryAdminDefault
    from photologue.models import Gallery
    from .models import GalleryExtended


    class GalleryExtendedInline(admin.StackedInline):
        model = GalleryExtended
        can_delete = False


    class GalleryAdmin(GalleryAdminDefault):

        """Define our new one-to-one model as an inline of Photologue's Gallery model."""

        inlines = [GalleryExtendedInline, ]

    admin.site.unregister(Gallery)
    admin.site.register(Gallery, GalleryAdmin)

The above code is enough to start entering tags in the admin interface. To use/display them in the front
end, you will also need to override Photologue's own templates - as the templates are likely to be
heavily customised for your specific project, an example is not included here.


