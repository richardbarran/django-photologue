Photologue
==========

Improved image management for the Django web framework.


Installation
------------

The easiest way to install Photologue is with pip::

   pip install django-photologue

You can verify Photologue is available to your project by running the following
commands from within your project directory::

    manage.py shell
    >>> import photologue
    >>> photologue.VERSION
    (2, 0, 'rc1')

Tracking the Development Version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The current development version of Photologue can be checked out via Git from the project site using the following command::

    git clone git://github.com/jdriscoll/django-photologue.git

Configure Your Django Settings
------------------------------

Add 'photologue' to your INSTALLED_APPS setting::

    INSTALLED_APPS = (
         # ...other installed applications,
         'photologue',
    )

**Confirm that your MEDIA_ROOT and MEDIA_URL settings are correct.**


Register Photologue with the Django Admin
-----------------------------------------

Add the following to your projects urls.py file::

    from django.contrib import admin
    admin.autodiscover()

Sync Your Database
------------------

Run the Django 'syncdb' command to create the appropriate tables. After the database in initialized, run the following command to initialize Photologue::

    python manage.py plinit


Instant Photo Gallery
---------------------

To use the included photo gallery templates and views you need to first add photologue to your projects urls.py file::

    urlpatterns += patterns('',
        ...
        (r'^photologue/', include('photologue.urls')),
    )
    
Once your urls are configured you need to copy the directory photologue/templates/photologue to your projects "templates" directory::

    myproject/
        myapp/
            ...
        templates/
            photologue/
                ...

If you'd rather, you can also add the absolute path to the photologue/templates directory to your TEMPLATE_DIRS setting::

    TEMPLATE_DIRS = ('/path/to/photologue/templates',)

Additional Documentation and Support
------------------------------------

Offical docs: http://code.google.com/p/django-photologue/w/list.

If you have any questions or need help with any aspect of Photologue please feel free to join the discussion group at http://groups.google.com/group/django-photologue.

