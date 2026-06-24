# /usr/bin/env python
from setuptools import find_packages, setup

import photologue


def get_requirements(source):
    requirements = set()

    with open(source) as f:
        for line in f:
            requirement = line.split('#', 1)[0].strip()
            if requirement:
                requirements.add(requirement)

    return sorted(requirements)


setup(
    name="django-photologue",
    version=photologue.__version__,
    description="Powerful image management for the Django web framework.",
    author="Justin Driscoll, Marcos Daniel Petry, Richard Barran",
    author_email="justin@driscolldev.com, marcospetry@gmail.com, richard@arbee.design",
    url="https://github.com/richardbarran/django-photologue",
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
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.10',
                 'Programming Language :: Python :: 3.11',
                 'Programming Language :: Python :: 3.12',
                 'Programming Language :: Python :: 3.13',
                 'Programming Language :: Python :: 3.14',
                 'Topic :: Utilities'],
    python_requires=">=3.10",
    install_requires=get_requirements('requirements.txt'),
)
