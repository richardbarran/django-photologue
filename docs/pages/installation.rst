############
Installation
############


Introduction
------------
The easiest way to install Photologue is with pip::

    pip install django-photologue

You can also install the development
version which is on `Github <https://github.com/>`_::

    git clone git://github.com/jdriscoll/django-photologue.git
    cd django-photologue
    python setup.py install

This code should work ok - like `Django <https://www.djangoproject.com/>`_
itself, we try to keep the master branch bug-free.

Python 3
~~~~~~~~
Photologue works with Python 3 >= 3.3 and Django >= 1.5. Like Django itself,
support for Python 3 can be described as "should work, but needs more time on
production sites to prove itself". Use it, but make sure that all features work!  

Dependencies
------------

* `Django <https://www.djangoproject.com/>`_.
* `Pillow <http://python-imaging.github.io/Pillow/>`_.
* `South <http://south.aeracode.org/>`_.

These 3 apps will be installed automatically if they are not already there.

.. note::

    * Pillow can be tricky to install; sometimes it will install smoothly
      out of the box, sometimes you can spend hours figuring it out - installation
      issues vary from platform to platform, and from one OS release to the next, so listing
      them here would not be practical. Google
      is your friend, and it's worth noting that Pillow is a fork of PIL,
      so googling 'PIL installation <your platform>' can also help.
    * You should not have installed both PIL and Pillow; this can cause strange bugs. 
    * Photologue has the same support policy as Django (last 2 versions released).

Photologue also uses the Django admin app, `so enable it if you have not already done so <https://docs.djangoproject.com/en/1.4/ref/contrib/admin/>`_.

Configure Your Django Settings
------------------------------

#. Add 'photologue' to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
         # ...other installed applications,
         'photologue',
         'south',
    )

#. Confirm that your `MEDIA_ROOT <https://docs.djangoproject.com/en/dev/ref/settings/#media-root>`_ and
   `MEDIA_URL <https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-MEDIA_URL>`_ settings 
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

If you are installing Photologue for the first time, this will set up some
default PhotoSizes to get you started - you are free to change them of course!


Instant Photo Gallery
---------------------

Photologue comes with basic templates for galleries and photos. You can of course override them, or completely
replace them. Note that all Photologue templates inherit from ``photologue/root.html``, which itself just inherits from
a site-wide ``base.html`` - you can change this to use a different base template.

Sitemap
-------

.. automodule:: photologue.sitemaps

