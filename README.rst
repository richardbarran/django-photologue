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

Dependencies
------------

Photologue uses the Django admin app, `so enable it if you have not already done so <https://docs.djangoproject.com/en/1.4/ref/contrib/admin/>`_.

Configure Your Django Settings
------------------------------

#. Add 'photologue' to your INSTALLED_APPS setting::

    INSTALLED_APPS = (
         # ...other installed applications,
         'photologue',
    )

#. Confirm that your `MEDIA_ROOT <https://docs.djangoproject.com/en/1.4/ref/settings/#media-root>`_ and `MEDIA_URL <https://docs.djangoproject.com/en/1.4/ref/settings/#std:setting-MEDIA_URL>`_ settings are correct (Photologue will store uploaded files in a folder called 'photologue' under your MEDIA_ROOT).

Sync Your Database
------------------

Run the Django 'syncdb' command to create the appropriate tables. After the database in initialized, run the following command to initialize Photologue::

    python manage.py plinit


Instant Photo Gallery
---------------------

Photologue comes with basic templates for galleries and photos. You can of course override them, or completely
replace them. Note that all Photologue templates inherit from ``photologue/root.html``, which itself just inherits from
a site-wide ``base.html`` - you can change this to use a different base template.

To use the included photo gallery templates and views you need to first add photologue to your projects urls.py file::

    urlpatterns += patterns('',
        ...
        (r'^photologue/', include('photologue.urls')),
    )
    
Additional Documentation and Support
------------------------------------

Offical docs are available on Google Code: http://code.google.com/p/django-photologue/w/list (Photologue is 
in the process of tranferring from Google Code to Github).

If you have any questions or need help with any aspect of Photologue please feel free to join the discussion group at http://groups.google.com/group/django-photologue.

