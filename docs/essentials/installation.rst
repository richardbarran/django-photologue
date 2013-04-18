############
Installation
############


Introduction
------------
The easiest way to install Photologue is with pip::

    pip install django-photologue

If you like taking risks, you can also install the development
version which is on `Github <https://github.com/>`_::

    git clone git://github.com/jdriscoll/django-photologue.git
    cd django-photologue
    python setup.py install

(that said, the risk should be minimal - like `Django <https://www.djangoproject.com/>`_
itself, we try to keep the code in the master branch bug-free).

Dependencies
------------

* `Pillow <http://python-imaging.github.io/Pillow/>`_.
* `South <http://south.aeracode.org/>`_.
* `Django <https://www.djangoproject.com/>`_.

These 3 apps will be installed automatically if they are not already there.

.. note::

    * Pillow is notoriously tricky to install; sometimes it will install smoothly
      out of the box, sometimes you can spend hours figuring it out - installation
      issues vary from platform to platform, and from one OS release to the next. Google
      is your friend here, and it's worth noting that Pillow is a fork of PIL,
      so googling 'PIL installation <your platform>' can also help.
    * Photologue, like Django itself, only supports the last 2 releases of Django - 
      so it will automatically try to install at least version (current release - 1).

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
