############
Installation
############


Introduction
------------
The easiest way to install Photologue is with pip::

   pip install django-photologue

You can verify Photologue is available to your project by running the following
commands from within your project directory::

    manage.py shell
    >>> import photologue
    >>> photologue.VERSION
    (2, 0, 'rc1')

Dependencies
------------

* `PIL <http://www.pythonware.com/products/pil/>`_.
* `South <http://south.aeracode.org/>`_.

These 2 apps will be installed automatically if they are not already there.

Photologue also uses the Django admin app, `so enable it if you have not already done so <https://docs.djangoproject.com/en/1.4/ref/contrib/admin/>`_.

Configure Your Django Settings
------------------------------

#. Add 'photologue' to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
         # ...other installed applications,
         'photologue',
         'south',
    )

#. Confirm that your `MEDIA_ROOT <https://docs.djangoproject.com/en/1.4/ref/settings/#media-root>`_ and
   `MEDIA_URL <https://docs.djangoproject.com/en/1.4/ref/settings/#std:setting-MEDIA_URL>`_ settings 
   are correct (Photologue will store uploaded files in a folder called 'photologue' under your ``MEDIA_ROOT``).

Add the urls
------------

Add photologue to your projects urls.py file::

    urlpatterns += patterns('',
        ...
        (r'^photologue/', include('photologue.urls')),
    )
    
Sync Your Database
------------------

Use South to setup the new tables::

    python manage.py migrate photologue

After the database in initialized, run the following command to setup some 
default values for Photologue::

    python manage.py plinit


Instant Photo Gallery
---------------------

Photologue comes with basic templates for galleries and photos. You can of course override them, or completely
replace them. Note that all Photologue templates inherit from ``photologue/root.html``, which itself just inherits from
a site-wide ``base.html`` - you can change this to use a different base template.
