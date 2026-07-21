"""Hooks used by zest.releaser while preparing and publishing releases."""

import codecs
import copy
import os
import shlex
import shutil
import subprocess
import sys

REPOSITORY = "richardbarran/django-photologue"
WORKFLOW = "publish-pypi.yml"


def prereleaser_before(data):
    """
    1. Run the unit tests one last time before we make a release.
    2. Update the CONTRIBUTORS.txt file.

    """
    try:
        import polib
    except ImportError:
        print('Msg to the package releaser: prerelease hooks will not work as you have not installed polib.')
        raise

    print('Running unit tests.')
    subprocess.check_output([sys.executable, "example_project/manage.py", "test", "photologue"])

    print('Checking that we have no outstanding DB migrations.')
    output = subprocess.check_output([sys.executable, "example_project/manage.py", "makemigrations", "--dry-run",
                                      "photologue"])
    if not output == b"No changes detected in app 'photologue'\n":
        raise Exception('There are outstanding migrations for Photologue.')

    print('Updating CONTRIBUTORS.txt')

    # This command will get the author of every commit.
    output = subprocess.check_output(["git", "log", "--format='%aN'"])

    # Convert to a list.
    contributors_list = [contributor.strip("'") for contributor in output.decode('utf-8').split('\n')]

    # Now add info from the translator files. This is incomplete, we can only list
    # the 'last contributor' to each translation.
    for language in os.listdir('photologue/locale/'):
        filename = f'photologue/locale/{language}/LC_MESSAGES/django.po'
        po = polib.pofile(filename)
        last_translator = po.metadata['Last-Translator']
        contributors_list.append(last_translator[:last_translator.find('<') - 1])

    # Now we want to only show each contributor once, and to list them by how many
    # contributions they have made - a rough guide to the effort they have put in.
    contributors_dict = {}

    for author in contributors_list:
        author_copy = copy.copy(author)

        if author_copy in ('', '(no author)', 'FULL NAME'):
            # Skip bad data.
            continue

        # The creator of this project should always appear first in the list - so
        # don't add him to this list, but hard-code his name.
        if author_copy in ('Justin Driscoll', 'justin.driscoll'):
            continue

        # Handle contributors who appear under multiple names.
        if author_copy == 'richardbarran':
            author_copy = 'Richard Barran'

        if author_copy in contributors_dict:
            contributors_dict[author_copy] += 1
        else:
            contributors_dict[author_copy] = 1

    with codecs.open('CONTRIBUTORS.txt', 'w', encoding='utf8') as f:
        f.write('Photologue is made possible by all the people who have contributed'
                ' to it. A non-exhaustive list follows:\n\n')
        f.write('Justin Driscoll\n')
        for i in sorted(contributors_dict, key=contributors_dict.get, reverse=True):
            f.write(i + '\n')

    # And commit the new contributors file.
    if subprocess.check_output(["git", "diff", "CONTRIBUTORS.txt"]):
        subprocess.check_output(["git", "commit", "-m", "Updated the list of contributors.", "CONTRIBUTORS.txt"])


def _run(command, working_dir):
    return subprocess.run(
        command,
        capture_output=True,
        check=True,
        cwd=working_dir,
        text=True,
    )


def _release_tag(working_dir):
    """Return the tag on the release commit preceding postrelease."""
    result = _run(
        ["git", "describe", "--tags", "--exact-match", "HEAD^"],
        working_dir,
    )
    return result.stdout.strip()


def _dispatch_command(tag):
    return [
        "gh",
        "workflow",
        "run",
        WORKFLOW,
        "--repo",
        REPOSITORY,
        "--ref",
        "master",
        "-f",
        f"release_tag={tag}",
    ]


def _error_detail(error):
    stderr = getattr(error, "stderr", None)
    if stderr and stderr.strip():
        return stderr.strip()
    return str(error)


def trigger_pypi_workflow(data):
    """Start PyPI publication without failing a completed local release."""
    working_dir = data.get("workingdir", os.getcwd())
    retry_command = None

    try:
        tag = _release_tag(working_dir)
        if not tag:
            raise RuntimeError("The release commit has no tag.")

        retry_command = _dispatch_command(tag)
        _run(
            ["git", "ls-remote", "--exit-code", "--refs", "origin", f"refs/tags/{tag}"],
            working_dir,
        )

        if shutil.which("gh") is None:
            raise RuntimeError("The GitHub CLI ('gh') is not installed.")

        _run(["gh", "auth", "status", "--hostname", "github.com"], working_dir)
        result = _run(retry_command, working_dir)
    except Exception as error:
        print("\nRelease preparation completed, but the PyPI workflow was not started.")
        print(f"Reason: {_error_detail(error)}")
        if retry_command:
            print("\nRetry with:")
            print(shlex.join(retry_command))
        else:
            print("Resolve the release-tag problem, then start publish-pypi.yml from GitHub Actions.")
        return

    print(f"\nStarted the PyPI publication workflow for release {tag}.")
    if result.stdout.strip():
        print(result.stdout.strip())
