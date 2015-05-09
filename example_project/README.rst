#######################
Photologue Demo Project
#######################

About
=====
This project serves 3 purposes:

- It's a quick demo of django-photologue for people who wish to try it out.
- It's an easy way for contributors to the project to have both django-photologue,
  and a project that uses it.
- It's used for Travis CI testing of django-photologue.

It uses the Bootstrap-friendly templates that are supplied in contrib/bootstrap/templates.

The rest of the README will assume that you want to set up the test project in 
order to work on django-photologue itself.

Prerequisites
=============

- python 2.7, 3.3, or 3.4.
- virtualenvwrapper makes it easy to manage your virtualenvs. Strongly recommended!

Installation
============
**Note**: the project is configured so that it can run immediately with zero configuration
(especially of settings files).

Create a virtual python environment for the project. The use of virtualenvwrapper
is strongly recommended::

	mkproject --no-site-packages django-photologue
	or for more sophisticated setups:
	mkvirtualenv --no-site-packages django-photologue


Clone this code into your project folder::

	(cd to the new virtualenv)
	git clone https://github.com/jdriscoll/django-photologue.git .

**Note**: if you plan to contribute code back to django-photologue, then you'll
probably want instead to fork the project on Github, and clone your fork instead.

Install requirements::

	cd example_project
	pip install -r requirements.txt

**Note**: this will install Pillow, which is not always straightforward; sometimes it
will install smoothly out of the box, sometimes you can spend hours figuring it out - installation
issues vary from platform to platform, and from one OS release to the next. Google
is your friend here, and it's worth noting that Pillow is a fork of PIL,
so googling 'PIL installation <your platform>' can also help.

The project is set up to run SQLite in dev so that it can be quickly started
with no configuration required (you can of course specify another database in
the settings file). To setup the database::

	./manage.py syncdb
	./manage.py migrate

Follow the instructions to configure photologue here: `Photologue Docs <http://django-photologue.readthedocs.org/en/latest/pages/installation.html>`_

And finally run the project (it defaults to a safe set of settings for a dev
environment)::

	./manage.py runserver

Open browser to http://127.0.0.1:8000

Thank you
=========
This example project is based on the earlier `photologue_demo project <https://github.com/richardbarran/photologue_demo>`_.
This project included contributions and input from: crainbf, tomkingston, bmcorser.


.. 
	Note: this README is formatted as reStructuredText so that it's in the same
	format as the Sphinx docs. 
