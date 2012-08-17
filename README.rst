.. Note: the README is formatted as reStructedText as the plan is to (one day) move most of it into a 
   Sphinx-generated official documentation for Photologue :-)

Photologue
==========

Improved image management for the Django web framework.


Installation
------------

The easiest way to install Photologue is with pip::

   pip install django-photologue

Photologue uses the Python Imaging Library and South; these will be installed
automatically if they are not already there.

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

#. Add 'photologue' to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
         # ...other installed applications,
         'photologue',
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

Run the Django 'syncdb' command to create the appropriate tables. After the database in initialized, run the following command to initialize Photologue::

    python manage.py plinit


Instant Photo Gallery
---------------------

Photologue comes with basic templates for galleries and photos. You can of course override them, or completely
replace them. Note that all Photologue templates inherit from ``photologue/root.html``, which itself just inherits from
a site-wide ``base.html`` - you can change this to use a different base template.

Additional Documentation and Support
------------------------------------

`Offical docs are available on Google Code <http://code.google.com/p/django-photologue/w/list>`_ (Photologue is 
in the process of tranferring from Google Code to Github).

If you have any questions or need help with any aspect of Photologue then please `join the mailing list
<http://groups.google.com/group/django-photologue>`_.

Contributing to Photologue
--------------------------

Contributions are always very welcome.

Workflow
^^^^^^^^
Django-photologue is hosted on Github, so if you have not already done so, read the excellent
`Github help pages <https://help.github.com/articles/fork-a-repo>`_. We try to keep the workflow
as simple as possible, so we more-or-less follow the recommendations in the 
`"GitHub Flow" blog post <http://scottchacon.com/2011/08/31/github-flow.html>`_.

* The "more or less" is because we don't do immediate releases.
* One very important point is: don't take it personaly if your pull request is rejected at first; view a pull
  request as the start of a conversation, with the goal of improving your code, so that it is of the best 
  possible quality when it gets merged into Photologue.

Coding style
^^^^^^^^^^^^
Nothing surprising here - just try to `follow the conventions used by Django itself 
<https://docs.djangoproject.com/en/1.4/internals/contributing/writing-code/>`_.

New features
^^^^^^^^^^^^
If you’re interested in developing a new feature for Photologue, it is recommended that you first 
discuss it on the `mailing list <http://groups.google.com/group/django-photologue>`_ so as not to 
do any work that will not get merged in anyway.

Unit tests
^^^^^^^^^^
Including unit tests with your contributions will earn you bonus points, maybe even a beer. So write
plenty of tests.

Documentation
^^^^^^^^^^^^^
Keeping the documentation up-to-date is very important - so if your code changes how Photologue works,
check that the documentation is still accurate.

.. note:: Right now, this README is the only up-to-date documentation for Photologue (the plan is to use Sphinx in the near future). 

Oh, and in a more general sense, the CHANGELOG is part of the documentation - so if your patch needs 
the end user to be aware of something e.g. need to run a South migration, mention it in the CHANGELOG!
