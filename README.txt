Photologue

Powerful image management for the Django web framework.


Installation
============

Offical releases are available from: http://code.google.com/p/django-photologue/


Source Distribution
-------------------

Download the .zip distribution file and unpack it. From within the extracted directory run the following command:

   python setup.py install


Tracking the Development Version
--------------------------------

The current development version of Photologue can be checked out via Subversion from the project site using the following command:

    svn checkout http://django-photologue.googlecode.com/svn/trunk/ photologue-trunk

Then either copy the photologue-trunk/photologue directory or create a symlink to the photologue-trunk/photologue directory somewhere on your python path, such as your Django project or site-packages directory.

You can verify Photologue is available to your project by running the following commands from within your project directory:

    manage.py shell

    >>> import photologue
    >>> photologue.VERSION
    (2, 0, 'rc1')


Configure Your Django Settings
------------------------------

Add 'photologue' to your INSTALLED_APPS setting:

    INSTALLED_APPS = (
         # ...other installed applications,
         'photologue',
    )

*** Confirm that your MEDIA_ROOT and MEDIA_URL settings are correct. ***


Register Photologue with the Django Admin
-----------------------------------------

Add the following to your projects urls.py file:

    from django.contrib import admin

    admin.autodiscover()


Sync Your Database
------------------

Run the Django 'syndb' command to create the appropriate tables. After the database in initialized, run the following command to initialize Photologue:

    python manage.py plinit

Additional Documentation and Support
------------------------------------

Offical docs:

    http://code.google.com/p/django-photologue/w/list

Discussion group:

    http://groups.google.com/group/django-photologue