#!/usr/bin/env python

import ntpapi as project

import os
from setuptools import find_packages
from setuptools import setup


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except:
        return None

setup(
    name=project.NAME,
    version=project.VERSION,
    description=project.DESCRIPTION,
    long_description=read('README.md'),
    author=project.AUTHOR_NAME,
    author_email=project.AUTHOR_EMAIL,
    url=project.URL,
    packages=find_packages(),
    install_requires=read('requirements.txt'),
    package_data={
    },
    license=project.LICENSE,
    entry_points={
        'console_scripts': [
            'ntpapi = ntpapi.main:cli',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
    include_package_data=True,
)
