import io
import subprocess
from contextlib import redirect_stdout
from unittest import TestCase
from unittest.mock import call, patch

from release import releaser_hooks


class ReleaserHooksTests(TestCase):
    working_dir = "/checkout"

    @staticmethod
    def completed(stdout=""):
        return subprocess.CompletedProcess([], 0, stdout=stdout, stderr="")

    @patch("release.releaser_hooks.shutil.which", return_value="/usr/bin/gh")
    @patch("release.releaser_hooks.subprocess.run")
    def test_successfully_dispatches_release_tag(self, run, which):
        run.side_effect = [
            self.completed("3.20\n"),
            self.completed("remote tag\n"),
            self.completed(),
            self.completed("https://github.com/richardbarran/django-photologue/actions/runs/1\n"),
        ]

        output = io.StringIO()
        with redirect_stdout(output):
            releaser_hooks.trigger_pypi_workflow({"workingdir": self.working_dir})

        self.assertIn("Started the PyPI publication workflow for release 3.20", output.getvalue())
        self.assertIn("actions/runs/1", output.getvalue())
        which.assert_called_once_with("gh")
        self.assertEqual(
            run.call_args_list[-1],
            call(
                [
                    "gh",
                    "workflow",
                    "run",
                    "publish-pypi.yml",
                    "--repo",
                    "richardbarran/django-photologue",
                    "--ref",
                    "master",
                    "-f",
                    "release_tag=3.20",
                ],
                capture_output=True,
                check=True,
                cwd=self.working_dir,
                text=True,
            ),
        )

    @patch("release.releaser_hooks.shutil.which", return_value=None)
    @patch("release.releaser_hooks.subprocess.run")
    def test_missing_github_cli_is_recoverable(self, run, which):
        run.side_effect = [self.completed("3.20\n"), self.completed("remote tag\n")]

        output = io.StringIO()
        with redirect_stdout(output):
            result = releaser_hooks.trigger_pypi_workflow({"workingdir": self.working_dir})

        self.assertIsNone(result)
        self.assertIn("is not installed", output.getvalue())
        self.assertIn("gh workflow run publish-pypi.yml", output.getvalue())

    @patch("release.releaser_hooks.subprocess.run")
    def test_unpushed_tag_is_recoverable(self, run):
        run.side_effect = [
            self.completed("3.20\n"),
            subprocess.CalledProcessError(2, ["git", "ls-remote"], stderr="tag not found"),
        ]

        output = io.StringIO()
        with redirect_stdout(output):
            result = releaser_hooks.trigger_pypi_workflow({"workingdir": self.working_dir})

        self.assertIsNone(result)
        self.assertIn("tag not found", output.getvalue())
        self.assertIn("release_tag=3.20", output.getvalue())

    @patch("release.releaser_hooks.shutil.which", return_value="/usr/bin/gh")
    @patch("release.releaser_hooks.subprocess.run")
    def test_authentication_failure_is_recoverable(self, run, which):
        run.side_effect = [
            self.completed("3.20\n"),
            self.completed("remote tag\n"),
            subprocess.CalledProcessError(1, ["gh", "auth"], stderr="not logged in"),
        ]

        output = io.StringIO()
        with redirect_stdout(output):
            result = releaser_hooks.trigger_pypi_workflow({"workingdir": self.working_dir})

        self.assertIsNone(result)
        self.assertIn("not logged in", output.getvalue())
        self.assertIn("gh workflow run publish-pypi.yml", output.getvalue())

    @patch("release.releaser_hooks.shutil.which", return_value="/usr/bin/gh")
    @patch("release.releaser_hooks.subprocess.run")
    def test_dispatch_failure_is_recoverable(self, run, which):
        run.side_effect = [
            self.completed("3.20\n"),
            self.completed("remote tag\n"),
            self.completed(),
            subprocess.CalledProcessError(1, ["gh", "workflow"], stderr="dispatch failed"),
        ]

        output = io.StringIO()
        with redirect_stdout(output):
            result = releaser_hooks.trigger_pypi_workflow({"workingdir": self.working_dir})

        self.assertIsNone(result)
        self.assertIn("dispatch failed", output.getvalue())
        self.assertIn("gh workflow run publish-pypi.yml", output.getvalue())

    @patch("release.releaser_hooks.subprocess.run")
    def test_missing_release_tag_is_recoverable(self, run):
        run.side_effect = subprocess.CalledProcessError(
            128,
            ["git", "describe"],
            stderr="no tag exactly matches the release commit",
        )

        output = io.StringIO()
        with redirect_stdout(output):
            result = releaser_hooks.trigger_pypi_workflow({"workingdir": self.working_dir})

        self.assertIsNone(result)
        self.assertIn("no tag exactly matches", output.getvalue())
        self.assertIn("start publish-pypi.yml from GitHub Actions", output.getvalue())
