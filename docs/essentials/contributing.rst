##########################
Contributing to Photologue
##########################

Contributions are always very welcome.

Workflow
--------
Django-photologue is hosted on Github, so if you have not already done so, read the excellent
`Github help pages <https://help.github.com/articles/fork-a-repo>`_. We try to keep the workflow
as simple as possible, so we more-or-less follow the recommendations in the 
`"GitHub Flow" blog post <http://scottchacon.com/2011/08/31/github-flow.html>`_.

* The "more or less" is because we don't do immediate releases.
* One very important point is: don't take it personaly if your pull request is rejected at first; view a pull
  request as the start of a conversation, with the goal of improving your code, so that it is of the best 
  possible quality when it gets merged into Photologue.

Coding style
------------
Nothing surprising here - just try to `follow the conventions used by Django itself 
<https://docs.djangoproject.com/en/1.4/internals/contributing/writing-code/>`_.

New features
------------
If you’re interested in developing a new feature for Photologue, it is recommended that you first 
discuss it on the `mailing list <http://groups.google.com/group/django-photologue>`_ so as not to 
do any work that will not get merged in anyway.

Unit tests
----------
Including unit tests with your contributions will earn you bonus points, maybe even a beer. So write
plenty of tests.

Documentation
-------------
Keeping the documentation up-to-date is very important - so if your code changes
how Photologue works, please check that the documentation is still accurate, and
update it if required.

We use `Sphinx <http://sphinx.pocoo.org/>`_ to prepare the documentation; please refer to the excellent docs
on that site for help.

P.S. The CHANGELOG is part of the documentation :-) so if your patch needs the
end user to do something - e.g. run a South migration - don't forget to update
it!
