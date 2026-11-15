Transifex integration
=====================

Photologue uses Transifex's native GitHub integration. The repository owns the
English source catalogue; Transifex owns translated text. The mapping lives in
``transifex.yml`` and retains the existing language-code mappings.

For this low-activity project, the native integration keeps synchronization
independent of releases and avoids maintaining a custom synchronization workflow.

Connect the existing resource
-----------------------------

The repository changes must first be committed and pushed to ``master`` by the
maintainer so the integration can read ``transifex.yml``.

Before the first sync, link the existing Transifex resource to its repository
path. Transifex identifies GitHub resources using the MD5 hash of this exact
text, without a trailing newline::

    github#richardbarran/django-photologue#master#photologue/locale/en_US/LC_MESSAGES/django.po

In the existing resource's settings, set its slug to::

    e4cf37141cca7310ad1aa4f21fbb9263

Verify that this is the existing English (United States) source resource before
changing its slug. Reusing it preserves its translations and history rather
than creating a second resource. Do not delete the resource. See Transifex's
`existing-resource instructions
<https://help.transifex.com/en/articles/8065148-github-auto-syncing-and-management>`_.

In the Transifex project's Settings > Integrations > GitHub:

* Install or reconnect the GitHub app, granting access only to
  ``richardbarran/django-photologue``.
* Link the repository's ``master`` branch and select the checked-in
  ``transifex.yml`` configuration. Test the configuration and check the detected
  source file and language paths before saving.
* Select a custom threshold for **translated** content. Use the lowest permitted
  percentage so incomplete languages can contribute improvements.
* Select **Create a Pull Request**, grouped by **All resources and languages**.
* Set the interval between commits to **60 minutes**.
* Leave **Receive updates for source files** disabled: English strings are
  maintained in the repository.
* Save and sync. Confirm in the activity log that the existing resource was
  linked, and inspect the first translation PR before merging it.

These are account-side settings; ``transifex.yml`` only defines the file and
language mapping. The old CLI configuration under ``.tx/`` is no longer used.
See the `Transifex installation and configuration guide
<https://help.transifex.com/en/articles/6265125-github-installation-and-configuration>`_
for the current interface.

Maintenance and recovery
------------------------

Transifex updates an existing translation PR while it remains open. Once merged,
later updates create another PR. Follow the compilation and review steps in
:doc:`contributing` before merging each batch.

If updates stop arriving, check the integration's activity log and confirm the
linked branch, resource slug, configuration path, and app access. Its manual
sync option can send eligible translations again without running a release.
Neither synchronization nor translation completion is a prerequisite for
publishing a package.
