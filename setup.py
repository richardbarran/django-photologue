#/usr/bin/env python
import os
from setuptools import setup, find_packages

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)


def get_required_packages(path):
    required = []
    with open(path) as f:
        for line in f.read().splitlines():
            if not line.startswith('-r'):
                try:
                    i = line.index('#')
                    required.append(line[:i].strip())
                except:
                    required.append(line)
    return required

version = '2.6.dev0'

setup(
    name="django-photologue",
    version=version,
    description="Powerful image management for the Django web framework.",
    author="Justin Driscoll, Marcos Daniel Petry, Richard Barran",
    author_email="justin@driscolldev.com, marcospetry@gmail.com, richard@arbee-design.co.uk",
    url="https://github.com/jdriscoll/django-photologue",
    packages=find_packages(),
    package_data={
        'photologue': [
            'res/*.jpg',
            'locale/*/LC_MESSAGES/*',
            'templates/photologue/*.html',
            'templates/photologue/tags/*.html',
        ]
    },
    zip_safe=False,
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Utilities'],
    install_requires=get_required_packages('example_project/requirements.txt'),
)
