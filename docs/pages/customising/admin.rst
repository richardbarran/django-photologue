.. _customisation-admin-label:

####################
Customisation: Admin
####################

The Photologue admin can easily be customised to your project's requirements. The technique described on this page
is not specific to Photologue - it can be applied to any 3rd party library. 

Create a customisation application
----------------------------------
For clarity, it's best to put our customisation code in a new application; let's call it
``photologue_custom``; create the application and add it to your ``INSTALLED_APPS`` setting.


Changing the admin
------------------
In the new ``photologue_custom`` application, create a new empty ``admin.py`` file. In this file we
can replace the admin configuration supplied by Photologue, with a configuration specific to your project.
For example:

.. code-block:: python

    from django import forms
    from django.contrib import admin

    from photologue.admin import GalleryAdmin as GalleryAdminDefault
    from photologue.models import Gallery


    class GalleryAdminForm(forms.ModelForm):
        """Users never need to enter a description on a gallery."""

        class Meta:
            model = Gallery
            exclude = ['description']


    class GalleryAdmin(GalleryAdminDefault):
        form = GalleryAdminForm

    admin.site.unregister(Gallery)
    admin.site.register(Gallery, GalleryAdmin)


This snippet will define a new Gallery admin class based on Photologue's own. The only change we make
is to exclude the ``description`` field from the change form.

We then unregister the default admin for the Gallery model and replace it with our new class.

Possible uses
-------------

The technique outlined above can be used to make many changes to the admin; here are a couple of suggestions.

Custom rich text editors
~~~~~~~~~~~~~~~~~~~~~~~~
The description field on the Gallery model (and the caption field on the Photo model) are plain text fields.
With the above technique, it's easy to use a rich text editor to manage these fields in the admin. For example,
if you have `django-ckeditor <https://github.com/shaunsephton/django-ckeditor>`_ installed:

.. code-block:: python

    from django import forms
    from django.contrib import admin

    from ckeditor.widgets import CKEditorWidget
    from photologue.admin import GalleryAdmin as GalleryAdminDefault
    from photologue.models import Gallery


    class GalleryAdminForm(forms.ModelForm):
        """Replace the default description field, with one that uses a custom widget."""

        description = forms.CharField(widget=CKEditorWidget())

        class Meta:
            model = Gallery
            exclude = ['']


    class GalleryAdmin(GalleryAdminDefault):
        form = GalleryAdminForm

    admin.site.unregister(Gallery)
    admin.site.register(Gallery, GalleryAdmin)

