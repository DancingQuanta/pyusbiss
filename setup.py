#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['pyserial']

setup(
    name='pyusbiss',
    version='0.1.0',
    description="A Python module for interfacing with USB-ISS multifunction USB Communication Module",
    long_description=readme + '\n\n' + history,
    author="Andrew Tolmie",
    author_email='andytheseeker@gmail.com',
    url='https://github.com/DancingQuanta/pyusbiss',
    packages=[
        'pyusbiss',
    ],
    package_dir={'pyusbiss':
                 'pyusbiss'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='pyusbiss',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
