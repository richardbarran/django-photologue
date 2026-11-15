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

