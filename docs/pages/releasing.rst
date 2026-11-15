Releasing and publishing documentation
======================================

Prepare a release
-----------------

From a clean checkout of ``master``, run::

    uv run --isolated --with-requirements release/requirements-release.txt fullrelease

The isolated environment includes the development and documentation dependencies.
The prerelease hook runs the application tests, checks for missing migrations,
builds the documentation with warnings treated as errors, and updates
``CONTRIBUTORS.txt``. Fix any failing check before continuing the release.

Push the resulting commits and release tag yourself. The postrelease hook asks
GitHub Actions to publish the tag to PyPI; if the tag has not been pushed yet,
the hook prints a command to retry publication after pushing.

Read the Docs builds the pushed release tag independently through its native
GitHub integration. It installs the checked-out project and its documentation
dependencies, rather than downloading the release from PyPI. Documentation can
therefore publish before the package does. No Read the Docs API token is needed
in GitHub Actions.

Read the Docs setup
-------------------

A project administrator must configure these settings in the existing
``django-photologue`` Read the Docs project:

1. Connect the GitHub repository through the native integration and verify its
   webhook. Use ``.readthedocs.yml`` as the configuration file.
2. Under automation rules, enable a rule with version type **Tag**, match
   **Any version**, and action **Activate version**. Add another enabled rule
   with the same conditions and action **Trigger build for version**. Use
   **Any version** because release tags such as ``3.21`` need not contain three
   numeric components.
3. Disable other rules that build or activate branches or pull requests, and
   disable pull-request builds. Keep the tag build rule enabled: the presence
   of an enabled build rule prevents unmatched branch and pull-request webhook
   events from triggering builds.
4. Set the default version to ``stable``. Read the Docs maintains this alias for
   the newest final release. Add a forced **Exact redirect** from
   ``/en/latest/*`` to ``/en/stable/:splat`` so links to pages under ``latest``
   follow the stable version, including pages that already exist.

See the `automation rules reference
<https://docs.readthedocs.com/platform/stable/automation-rules.html>`_ and
`redirects reference
<https://docs.readthedocs.com/platform/stable/user-defined-redirects.html>`_.

Verify the first current build
------------------------------

After pushing the configuration changes, manually build the current ``master``
version from the Read the Docs dashboard and check that the build succeeds.
Preview the Alabaster HTML output and downloadable HTML archive. Check the build
commit matches the pushed commit. This one-time manual build does not require
enabling automatic branch builds or rebuilding historical release tags.

After the next final release tag is pushed, verify its versioned documentation,
the ``stable`` alias, and the ``latest`` redirect. Until that release is built,
``stable`` may continue to serve the existing published release.

Check publication and recover
-----------------------------

Before treating a release as complete or pushing another release tag, check
both the GitHub Actions PyPI publication job and the Read the Docs tag build.
Neither service's result guarantees the other succeeded.

If documentation publication fails, inspect the build log in Read the Docs.
Fix service settings or transient failures and retry the same version there.
If the tagged source needs a fix, make a new release with the correction; do
not move a published release tag. A documentation failure does not fail or
roll back PyPI publication. Historical documentation rebuilds are outside
this restoration work.
