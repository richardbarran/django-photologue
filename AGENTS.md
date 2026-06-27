# AGENTS.md

## Running the Full Test Matrix

Run tox from the repository root:

```bash
tox
```

## Updating Django and Python Compatibility

Use this runbook when updating the project for the current supported Django and
Python releases. Run the phases in order. Stop and prompt the user if there are
errors, conflicting source data, unclear compatibility decisions, missing
credentials, or changes that require judgment beyond routine maintenance.

### 1. Discovery

Check the currently supported Django release series from:

https://www.djangoproject.com/download/

Check the Python versions supported by each Django release series from:

https://docs.djangoproject.com/en/dev/faq/install/#what-python-version-can-i-use-with-django

Check which Python versions are themselves still supported from:

https://devguide.python.org/versions/

Build the target matrix by intersecting the supported Django release series, the
Python versions supported by each Django series, and Python versions in `bugfix`
or `security` status. Exclude prerelease Django or Python versions unless the
user explicitly asks to test prereleases.

Check which target Python versions are available in the local environment. If
some are missing, continue updating project config from official sources, but
tell the user that full local verification may rely on CI.

### 2. Baseline Verification

Run the unit tests from the repository root:

```bash
python scripts/run_tests.py
```

Run the full existing tox matrix from the repository root:

```bash
tox
```

If either command fails before any changes are made, investigate and report the
failure before changing compatibility files.

### 3. Deprecation Warning Cleanup

Re-run unit tests with deprecation warnings enabled:

```bash
PYTHONWARNINGS=default python scripts/run_tests.py
```

If warnings appear, fix clear warnings from project code directly. Do not make
behavior-changing fixes without explaining the proposed change first. Do not
change dependency minimums solely for third-party warnings unless compatibility
requires it. For third-party warnings that cannot reasonably be fixed in project
code, report them to the user.

If project code changed to fix warnings, add this changelog entry under the
current unreleased section:

```text
- Fixed deprecation warnings.
```

### 4. Matrix and Metadata Update

Update `tox.ini` so its environment list matches the target supported
Django/Python matrix.

Update `setup.py` classifiers so supported Python and Django classifiers match
the target support policy.

Update `.github/workflows/ci.yml` so CI runs the intended Python/Django matrix.
Prefer mirroring tox unless the project deliberately uses a smaller CI matrix.

If the project has other compatibility metadata, update it consistently.

### 5. Dependency Lower-Bound Review

Read all relevant requirement files, including `requirements.txt`,
`example_project/requirements.txt`, and any other `requirements*.txt` files that
affect tests, docs, or supported installs.

For each lower-bound dependency, verify that the minimum version supports the
full target Python/Django matrix using package metadata, especially
`Requires-Python`. Verify lower bounds by installing and testing them, not just
by reading metadata.

Read dependency changelogs when a minimum version needs to change,
compatibility is unclear, package metadata is incomplete, or a test failure
points at dependency behavior. Update requirement files only when needed for the
target matrix.

### 6. Changelog Update

Update `CHANGELOG.txt` under the current unreleased section for compatibility
changes. Use the project's existing concise bullet style. Remove
`- Nothing changed yet.` when adding the first real entry.

Add entries only for actual changes. Examples:

```text
- Added support for Django 6.0 and Python 3.14.
- Dropped Django 4.2, Django 5.1, Python 3.8, and Python 3.9.
```

If code changes were made beyond compatibility metadata, propose changelog
wording to the user before finalizing those entries.

### 7. Full Verification Loop

Re-run tox from the repository root:

```bash
tox
```

If tox fails, investigate the failure, propose or apply clear fixes, re-run the
relevant failed tox environment first, then re-run full tox. Repeat until the
full intended matrix passes or the user decides to stop.

### 8. Final Review and Commit

Show the user the final changed files and summarize the changes. Ask the user
to confirm the commit message. Commit all approved changes together unless the
user asks for separate commits.

### 9. Push and CI Monitoring

Only the user can push to GitHub. Do not push branches or tags. After the user
pushes, monitor GitHub Actions if credentials and network access are available.
If CI fails, report the failing job and logs summary, then propose fixes before
making further changes.

## Updating the Changelog

When a change affects users, compatibility, migrations, dependencies, or release
behavior, add an entry to `CHANGELOG.txt` under the current unreleased section.
Remove `- Nothing changed yet.` when adding the first real entry for that
release. Keep entries concise and consistent with the existing bullet style.

## Running Unit Tests

Run the Django unit tests from the example project directory:

```bash
cd example_project
./manage.py test photologue
```

Alternatively, use the helper script from the repository root:

```bash
python scripts/run_tests.py
```

Any extra arguments are passed through to `manage.py test`:

```bash
python scripts/run_tests.py photologue.tests.test_models
```
