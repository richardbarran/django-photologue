"""Dispatch the trusted PyPI publishing workflow after a release."""

import os
import shlex
import shutil
import subprocess

REPOSITORY = "richardbarran/django-photologue"
WORKFLOW = "publish-pypi.yml"


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
