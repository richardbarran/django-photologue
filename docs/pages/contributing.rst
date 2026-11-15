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

There's also a `Tox <https://tox.readthedocs.io/en/latest/index.html>`_ configuration file - so if
you have tox installed, run ``tox`` from the ``/example_project/`` folder, and it will run the entire
test suite against all versions of Python and Django that are supported.

Documentation
-------------
Keeping the documentation up-to-date is very important - so if your code changes
how Photologue works, or adds a new feature, please check that the documentation is still accurate, and
update it if required.

We use `Sphinx <http://sphinx.pocoo.org/>`_ to prepare the documentation; please refer to the excellent docs
on that site for help.

From the repository root, install the documentation dependencies and build HTML::

    python -m pip install -r docs/requirements.txt
    python -m sphinx -E -W --keep-going -b html docs docs/_build/html

Open ``docs/_build/html/index.html`` to preview the result. Warnings fail the
build, matching the prerelease check and Read the Docs. See :doc:`releasing`
for publication setup and recovery.

.. note::

    The CHANGELOG is part of the documentation, so if your patch needs the
    end user to do something - e.g. run a database migration - don't forget to update
    it!

Translations
------------
`Photologue manages string translations with Transifex
<https://app.transifex.com/richardbarran/django-photologue/dashboard/>`_. The easiest way to help is
to add new/updated translations there.

The native Transifex GitHub integration is configured to collect updates for all
languages in one pull request, batching edits at 60-minute intervals. Partial
translations are welcome; a language need not be complete. The maintainer reviews
and merges updates when convenient. Releases include the translations already
merged into ``master`` and do not wait for pending translation work or Transifex
availability.

Updating English source strings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When changing translatable strings in Python code or templates, regenerate the
English source catalogue from the ``photologue`` directory::

    cd photologue
    python -m django makemessages -l en_US

Commit the updated ``photologue/locale/en_US/LC_MESSAGES/django.po`` with the code
change. This command requires Django and GNU gettext (``sudo apt install gettext``
on Ubuntu). Transifex reads this catalogue after it reaches ``master``; the
integration does not extract strings from Python code or templates. Make source
string changes in the repository, and translated text changes in Transifex.

Reviewing translation updates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Check out the translation PR branch locally. From the repository root, run::

    python bin/compile_translations.py

The command requires GNU gettext. It checks catalogue syntax and marked format
placeholders, then regenerates the committed ``.mo`` files used by Django. Empty
and fuzzy translations are left out of compiled catalogues, allowing Django to
fall back to the source text. A compilation error stops the command; resolve it
before merging. Earlier catalogues may already have been compiled successfully.

Review the ``.po`` changes and commit the regenerated ``.mo`` files on the PR
branch before merging. Run the compilation command again if Transifex adds more
changes after that commit. The same command should be run before merging an
English source catalogue update. No release-time download is needed.

See :doc:`translations` for integration setup and reconnection instructions.

New features
------------
In the wiki there is a `wishlist of new features already planned
for Photologue <https://github.com/richardbarran/django-photologue/wiki/Photologue-3.X-wishlist>`_ - you are welcome to suggest other useful improvements.

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
