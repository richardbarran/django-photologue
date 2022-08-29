#####
Usage
#####

Now that you've installed Photologue, here are a few suggestions on how to use it:

Upload some photos in the admin
-------------------------------
The ``Photo`` model in the admin allows you to add new photos to Photologue. You can add photos one by one - and
it the top-right corner there is a 'Upload a Zip archive' button that will allow you to upload many photos at once.

Define some Photosizes
----------------------
Photologue will create thumbnails of the photos that you upload, and the thumbnails are what is displayed in the
public website. By default Photologue comes with a few Photosizes to get you started - feel free to tweak them, or
to create new ones.

Just note that the ``admin_thumbnail`` size is used by the admin pages, so it's not a good idea to delete it!

Built-in pages and templates
----------------------------

If you've followed all the instructions in the installation page, you will have included Photologue's
urls at ``/photologue/`` - you can use these, tweak them, or discard them if they do not fit in with your website's
requirements.

Custom usage
------------
The base of Photologue is the ``Photo`` model. When an instance is created, we automatically add methods to retrieve
photos at various photosizes. E.g. if you have an instance of ``Photo`` called ``photo``, then the
following methods will have been added automatically::

    photo.get_thumbnail_url()
    photo.get_display_url()
    photo.get_admin_thumbnail_url()

These can be used in a custom template to display a thumbnail, e.g.::

    <a href="{{ photo.image.url }}">
        <img src="{{ photo.get_display_url }}" alt="{{ photo.title }}">
    </a>

This will display an image, sized to the dimensions specified in the Photosize ``display``,
and provide a clickable link to the raw image. Please refer to the example templates for ideas on how to use
``Photo`` and ``Gallery`` instances!

Data integrity
--------------
Photologue will store 'as-is' any data stored for galleries and photos.
You may want to enforce some data integrity rules - e.g. to sanitise
any javascript injected into a ``Photo`` ``caption`` field. An easy way to do this
would be to add extra processing on a ``post-save`` signal.

Photologue does not sanitise data itself as you may legitimately want to store html and
javascript in a caption field e.g. if you use a rich-text editor.

