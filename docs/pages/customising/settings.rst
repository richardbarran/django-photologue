#######################
Customisation: Settings
#######################


Photologue has several settings to customise behaviour.

PHOTOLOGUE_USE_CKEDITOR
-----------------------

    Default: ``False``

If you have already installed `django-ckeditor <https://pypi.python.org/pypi/django-ckeditor>`_
then you can use to edit the TextArea fields of Gallery
and Photo in the admin. Simply set the setting to ``True``.


.. deprecated:: 2.8

    Instead, override the admin; :ref:`see here <customisation-admin-label>`.

PHOTOLOGUE_GALLERY_PAGINATE_BY
------------------------------

    Default: ``20``

Number of galleries to display per page for GalleryListView.

.. deprecated:: 2.8

    Instead, override the view; :ref:`see here <customisation-views-label>`.

PHOTOLOGUE_PHOTO_PAGINATE_BY
----------------------------

    Default: ``20``

Number of photos to display per page for PhotoListView.

.. deprecated:: 2.8

    Instead, override the view; :ref:`see here <customisation-views-label>`.

PHOTOLOGUE_GALLERY_LATEST_LIMIT
-------------------------------

    Default: ``None``

Default limit for gallery.latest


PHOTOLOGUE_GALLERY_SAMPLE_SIZE
------------------------------

    Default: ``5``

Number of random images from the gallery to display.


PHOTOLOGUE_IMAGE_FIELD_MAX_LENGTH
---------------------------------

    Default: ``100``

max_length setting for the ImageModel ImageField


PHOTOLOGUE_SAMPLE_IMAGE_PATH
----------------------------

    Default: ``os.path.join(os.path.dirname(__file__), 'res', 'sample.jpg'))``

Path to sample image


PHOTOLOGUE_MAXBLOCK
-------------------

    Default: ``256 * 2 ** 10``

Modify image file buffer size.


PHOTOLOGUE_DIR
--------------

    Default: ``'photologue'``

The relative path from your ``MEDIA_ROOT`` setting where Photologue will save image files. If your ``MEDIA_ROOT`` is set to "/home/user/media", photologue will upload your images to "/home/user/media/photologue"


PHOTOLOGUE_PATH
---------------

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

.. _settings-photologue-multisite-label:

PHOTOLOGUE_MULTISITE
--------------------

    Default: ``False``

Photologue can integrate galleries and photos with `Django's site framework`_.
Default is for this feature to be switched off, as only a minority of Django projects
will need it.

In this case, new galleries and photos are automatically linked to the current site 
(``SITE_ID = 1``). The Sites many-to-many field is hidden is the admin, as there is no
need for a user to see it.

If the setting is ``True``, the admin interface is slightly changed:

* The Sites many-to-many field is displayed on Gallery and Photos models.
* The Gallery Upload allows you to associate one more sites to the uploaded photos (and gallery).

.. note:: Gallery Uploads (zip archives) are always associated with the current site. This will be
   fixed in a future version of Photologue.

.. _Django's site framework: http://django.readthedocs.org/en/latest/ref/contrib/sites.html