#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'example_project.settings')

    # Add parent folder to path so that we can import Photologue itself.
    PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])
    sys.path.append(os.path.join(PROJECT_PATH, ".."))

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
