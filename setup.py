#/usr/bin/env python
import os
from setuptools import setup, find_packages
import photologue

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)


def get_requirements(requirements_file):
    with open(requirements_file) as f:
        required = [line.split('#')[0] for line in f.read().splitlines()]
    # Temp situation: transition from PIL to Pillow, add a hook so people can
    # skip installing Pillow.
    if os.path.exists('/tmp/PHOTOLOGUE_NO_PILLOW'):
        required = [item for item in required if not item.startswith('Pillow')]
    return required

setup(
    name="django-photologue",
    version=photologue.__version__,
    description="Powerful image management for the Django web framework.",
    author="Justin Driscoll, Marcos Daniel Petry, Richard Barran",
    author_email="justin@driscolldev.com, marcospetry@gmail.com, richard@arbee-design.co.uk",
    url="https://github.com/jdriscoll/django-photologue",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Topic :: Utilities'],
    install_requires=get_requirements(os.path.join(ROOT_DIR, 'requirements.txt'))
)
