############################
Installation & configuration
############################


.. _installing-photologue-label:

Installation
------------
The easiest way to install Photologue is with pip::

    pip install django-photologue

You can also live life on the edge and install the latest code directly from the
Github repository::

    pip install -e git+https://github.com/jdriscoll/django-photologue.git#egg=django-photologue

This code should work ok - like `Django <https://www.djangoproject.com/>`_
itself, we try to keep the master branch bug-free.

Python 3
~~~~~~~~
Django from version 1.5 onwards works with Python 3.

Photologue also works with Python 3 (3.3 or later). Like Django itself,
support for Python 3 can be described as "should work, but needs more time on
production sites to prove itself". Use it, but apply caution!

Dependencies
------------

5 apps that will be installed automatically if required.

* `Django <https://www.djangoproject.com/>`_.
* `Pillow <http://python-imaging.github.io/Pillow/>`_.
* `South <http://south.aeracode.org/>`_.
* `Django-sortedm2m <https://pypi.python.org/pypi/django-sortedm2m>`_.
* `Django-model-utils <https://pypi.python.org/pypi/django-model-utils>`_.

And 2 dependencies that you will have to manage yourself:

* `Pytz <https://pypi.python.org/pypi/pytz>`_. Only applies if you're using Django >= 1.6, see the 
  Django release notes `for more information 
  <https://docs.djangoproject.com/en/1.6/releases/1.6/#time-zone-aware-day-month-and-week-day-lookups>`_.
* `Django’s site framework <https://docs.djangoproject.com/en/dev/ref/contrib/sites/#enabling-the-sites-framework>`_
  - only applies if you're using Django >= 1.6.

.. note::

    * Photologue has the same support policy as Django.

That troublesome Pillow...
~~~~~~~~~~~~~~~~~~~~~~~~~~
Pillow can be tricky to install; sometimes it will install smoothly
out of the box, sometimes you can spend hours figuring it out - installation
issues vary from platform to platform, and from one OS release to the next, so listing
them all here would not be realistic. Google
is your friend, and it's worth noting that Pillow is a fork of PIL,
so googling 'PIL installation <your platform>' can also help.

#. You should not have installed both PIL and Pillow; this can cause strange bugs.
   Please uninstall PIL before you install Pillow.

#. In some situations, you might not be able to use Pillow at all (e.g. if another
   package has a dependency on PIL). Photologue has a clumsy answer for this:
   write a temporary file ``/tmp/PHOTOLOGUE_NO_PILLOW``, then install Photologue.
   This will tell Photologue to install without Pillow. It *should* work, but it
   hasn't been tested!

#. Sometimes Pillow will install... but is not actually installed. This 'undocumented feature' has been
   reported by a user on Windows. If you can't get Photologue to disaply any images, check
   that you can actually import Pillow::

     $ python manage.py shell
     Python 3.3.1 (default, Sep 25 2013, 19:29:01)
     [GCC 4.7.3] on linux
     Type "help", "copyright", "credits" or "license" for more information.
     (InteractiveConsole)
     >>> from PIL import Image
     >>>


Configure Your Django Settings
------------------------------

#. Add to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
         # ...other installed applications,
         'photologue',
         'south',		# if it's not already in your INSTALLED_APPS.
         'sortedm2m',
    )

#. Confirm that your `MEDIA_ROOT <https://docs.djangoproject.com/en/dev/ref/settings/#media-root>`_ and
   `MEDIA_URL <https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-MEDIA_URL>`_ settings
   are correct (Photologue will store uploaded files in a folder called 'photologue' under your ``MEDIA_ROOT``).

#. `Enable the admin app if you have not already done so <https://docs.djangoproject.com/en/dev/ref/contrib/admin/>`_.

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

Sites
-----

Photologue supports `Django's site framework`_ since version 2.8. That means
that each Gallery and each Photo can be displayed on one or more sites.

Please bear in mind that photos don't necessarily have to be assigned to the
same sites as the gallery they're belonging to: each gallery will only display
the photos that are on its site. When a gallery does not belong the current site
but a single photo is, that photo is only accessible directly as the gallery
won't be shown in the index.

.. note:: If you're upgrading from a version earlier than 2.8 you don't need to
   worry about the assignment of already existing objects to a site because a
   datamigration will assign all your objects to the current site automatically.

.. note:: This feature is switched off by default. :ref:`See here to enable it 
   <settings-photologue-multisite-label>` and for more information.

.. _Django's site framework: http://django.readthedocs.org/en/latest/ref/contrib/sites.html



