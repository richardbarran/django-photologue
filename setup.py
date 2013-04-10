#/usr/bin/env python
import os
from setuptools import setup, find_packages

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

version = '2.6.dev0'

setup(
    name="django-photologue",
    version=version,
    description="Powerful image management for the Django web framework.",
    author="Justin Driscoll, Marcos Daniel Petry, Richard Barran",
    author_email="justin@driscolldev.com, marcospetry@gmail.com",
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
    install_requires=['Django>=1.4', # Timezone support means 1.4 minimum.
                      'South>=0.7.5', # Might work with earlier versions, but not tested.
                      'Pillow>=2.0.0', # Might work with earlier versions, but not tested. YMMV. Note that 2.0.0 needed for Mac users.
                      ],
)
