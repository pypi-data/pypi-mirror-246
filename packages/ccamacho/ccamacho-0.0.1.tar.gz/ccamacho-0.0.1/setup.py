#!/usr/bin/env python

"""
Copyright.

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
"""

import os
from sys import version_info

from setuptools import find_packages, setup

if version_info < (3, 5):
    raise RuntimeError(
        'Python 3.5 or greater is required'
    )

_NAME = 'ccamacho'
_DESCRIPTION = 'ccamacho CLI'
_REVISION = '0.0.1'
_URL = 'https://github.com/ccamacho/cv'
_AUTHOR = 'Carlos Camacho'
_AUTHOR_EMAIL = 'carloscamachoucv@gmail.com'

package_revision = os.environ.get('PACKAGE_REVISION', "")
if (package_revision != ""):
    _REVISION = _REVISION + "." + package_revision

if os.path.isfile('../README.md'):
    with open('../README.md') as f:
        long_description = f.read()
else:
    long_description = _DESCRIPTION

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name=_NAME,
    version=_REVISION,
    description=_DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=long_description,
    url=_URL,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Testing',
    ],
    author=_AUTHOR,
    author_email=_AUTHOR_EMAIL,
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            '{0} = {0}.cli:main'.format(_NAME),
        ]
    }
)
