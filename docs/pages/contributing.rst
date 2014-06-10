##########################
Contributing to Photologue
##########################

Contributions are always very welcome. Even if you have never contributed to an
open-source project before - please do not hesitate to offer help. Fixes for typos in the
documentation, extra unit tests, etc... are welcome. And look in the issues
list for anything tagged "easy_win".

Example project
---------------
Photologue includes an example project under ``/example_project/`` to get you quickly ready for 
contributing to the project - do not hesitate to use it! Please refer to ``/example_project/README.rst``
for installation instructions.

You'll probably also want to manually install
`Sphinx <http://sphinx.pocoo.org/>`_ if you're going to update the documentation.

Workflow
--------
Photologue is hosted on Github, so if you have not already done so, read the excellent
`Github help pages <https://help.github.com/articles/fork-a-repo>`_. We try to keep the workflow
as simple as possible; most pull requests are merged straight into the master branch. Please
ensure your pull requests are on separate branches, and please try to only include one new 
feature per pull request!

Features that will take a while to develop might warrant a separate branch in the project;
at present only the ImageKit integration project is run on a separate branch.

Coding style
------------
No surprises here - just try to `follow the conventions used by Django itself 
<https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/>`_.

Unit tests
----------
Including unit tests with your contributions will earn you bonus points, maybe even a beer. So write
plenty of tests, and run them from the ``/example_project/`` with a 
``python manage.py test photologue``.

Documentation
-------------
Keeping the documentation up-to-date is very important - so if your code changes
how Photologue works, or adds a new feature, please check that the documentation is still accurate, and
update it if required.

We use `Sphinx <http://sphinx.pocoo.org/>`_ to prepare the documentation; please refer to the excellent docs
on that site for help.

.. note::
    
    The CHANGELOG is part of the documentation, so if your patch needs the
    end user to do something - e.g. run a South migration - don't forget to update
    it!

Translations
------------
`Photologue manages string translations with Transifex 
<https://www.transifex.com/projects/p/django-photologue/>`_. The easiest way to help is
to add new/updated translations there. 

Once you've added translations, give the maintainer a wave and he will pull the updated
translations into the master branch, so that you can install Photologue directly from the 
Github repository (see :ref:`installing-photologue-label`) and use your translations straight away. Or you can do nothing - just before a release
any new/updated translations get pulled from Transifex and added to the Photologue project.

New features
------------
In the wiki there is a `wishlist of new features already planned
for Photologue <https://github.com/jdriscoll/django-photologue/wiki/Photologue-3.X-wishlist>`_ - you are welcome to suggest other useful improvements.

If you’re interested in developing a new feature, it is recommended that you first 
discuss it on the `mailing list <http://groups.google.com/group/django-photologue>`_ 
or open a new ticket in Github, in order to avoid working on a feature that will
not get accepted as it is judged to not fit in with the goals of Photologue.

A bit of history
~~~~~~~~~~~~~~~~
Photologue was started by Justin Driscoll in 2007. He quickly built it into a powerful
photo gallery and image processing application, and it became successful.

Justin then moved onto other projects, and no longer had the time required to maintain
Photologue - there was only one commit between August 2009 and August 2012, and 
approximately 70 open tickets on the Google Code project page.

At this point Richard Barran took over as maintainer of the project. First priority
was to improve the infrastructure of the project: moving to Github, adding South,
Sphinx for documentation, Transifex for translations, Travis for continuous integration,
zest.releaser.

The codebase has not changed much so far - and it needs quite a bit of TLC
(Tender Loving Care), and new features are waiting to be added. This is where you step in...

And finally...
--------------
Please remember that the maintainer looks after Photologue in his spare time -
so it might be a few weeks before your pull request gets looked at... and the pull
requests that are nicely formatted, with code, tests and docs included, will 
always get reviewed first ;-)
