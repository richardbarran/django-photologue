Transifex integration
=====================

Photologue uses Transifex's native GitHub integration. The repository owns the
English source catalogue; Transifex owns translated text. The mapping lives in
``transifex.yml`` and defines the language-code mappings.

For this low-activity project, the native integration keeps synchronization
independent of releases and avoids maintaining a custom synchronization workflow.

Integration settings
--------------------

In the Transifex project's Settings > Integrations > GitHub:

* Restrict the GitHub app's access to
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

These are account-side settings; ``transifex.yml`` only defines the file and
language mapping.
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
