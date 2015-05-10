############################
Installation & configuration
############################


.. _installing-photologue-label:

Installation
------------
The easiest way to install Photologue is with `pip <https://pip.pypa.io/en/latest/>`_; this will give you the latest
version available on `PyPi <https://pypi.python.org/pypi>`_::

    pip install django-photologue

You can also take risks and install the latest code directly from the
Github repository::

    pip install -e git+https://github.com/jdriscoll/django-photologue.git#egg=django-photologue

This code should work ok - like `Django <https://www.djangoproject.com/>`_
itself, we try to keep the master branch bug-free. However, we strongly recommend that you 
stick with a release from the PyPi repository, unless if you're confident in your abilities 
to fix any potential bugs on your own!

Python 3
~~~~~~~~
Photologue works with Python 3 (3.3 or later).

Dependencies
------------
3 apps that will be installed automatically if required.

* `Django <https://www.djangoproject.com/>`_.
* `Pillow <http://python-imaging.github.io/Pillow/>`_.
* `Django-sortedm2m <https://pypi.python.org/pypi/django-sortedm2m>`_.

And 1 dependency that you will have to manage yourself:

* `Pytz <https://pypi.python.org/pypi/pytz>`_. See the Django release notes `for more information 
  <https://docs.djangoproject.com/en/1.6/releases/1.6/#time-zone-aware-day-month-and-week-day-lookups>`_.

.. note::

    Photologue tries to support the same Django version as are supported by the Django 
    project itself.

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
   reported by a user on Windows. If you can't get Photologue to display any images, check
   that you can actually import Pillow::

     $ python manage.py shell
     Python 3.3.1 (default, Sep 25 2013, 19:29:01)
     [GCC 4.7.3] on linux
     Type "help", "copyright", "credits" or "license" for more information.
     (InteractiveConsole)
     >>> from PIL import Image
     >>>


Configure Your Django Settings file
-----------------------------------

#. Add to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
         # ...other installed applications...
         'photologue',
         'sortedm2m',
    )

#. Confirm that your `MEDIA_ROOT <https://docs.djangoproject.com/en/dev/ref/settings/#media-root>`_ and
   `MEDIA_URL <https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-MEDIA_URL>`_ settings
   are correct (Photologue will store uploaded files in a folder called 'photologue' under your ``MEDIA_ROOT``).

#. `Enable the admin app if you have not already done so <https://docs.djangoproject.com/en/dev/ref/contrib/admin/>`_.

#. Django has `an optional site framework
   <https://docs.djangoproject.com/en/dev/ref/contrib/sites/#enabling-the-sites-framework>`_.
   This is not enabled by default in Django, but is required by Photologue.

Add the urls
------------

Add photologue to your projects urls.py file::

    urlpatterns += patterns('',
        ...
        url(r'^photologue/', include('photologue.urls', namespace='photologue')),
    )

Sync Your Database
------------------

You can now sync your database::

    python manage.py migrate photologue

If you are installing Photologue for the first time, this will set up some
default PhotoSizes to get you started - you are free to change them of course!

Instant templates
-----------------

Photologue comes with basic templates for galleries and photos, which are designed
to work well with `Twitter-Bootstrap <http://twitter.github.io/bootstrap/index.html>`_.
You can of course override them, or completely replace them. Note that all 
Photologue templates inherit from ``photologue/root.html``, which itself just inherits
from a site-wide ``base.html`` - you can change this to use a different base template.

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

Amazon S3
---------

Photologue can use a custom file storage system, for example
`Amazon's S3 <http://aws.amazon.com/s3/>`_.

You will need to configure your Django project to use Amazon S3 for storing files; a full discussion of 
how to do this is outside the scope of this page.

However, there is a quick demo of using Photologue with S3 in the ``example_project`` directory; if you look 
at these files:

* ``example_project/example_project/settings.py``
* ``example_project/requirements.txt``

At the end of each file you will commented-out lines for configuring S3 functionality. These point to extra files
stored under ``example_project/example_storages/``. Uncomment these lines, run the example
project, then study these files for inspiration! After that, setting up S3 will consist of
(at minimum) the following steps:

#. Signup for Amazon AWS S3 at http://aws.amazon.com/s3/.
#. Create a Bucket on S3 to store your media and static files.
#. Set the environment variables:
   
   * ``AWS_ACCESS_KEY_ID`` - issued to your account by S3.
   * ``AWS_SECRET_ACCESS_KEY`` - issued to your account by S3.
   * ``AWS_STORAGE_BUCKET_NAME`` - name of your bucket on S3.

#. To copy your static files into your S3 Bucket, type ``python manage.py collectstatic`` in the ``example_project`` directory.

.. note:: This simple setup does not handle S3 regions.






