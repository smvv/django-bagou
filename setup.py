# -*- coding: utf-8 -*-
import re
import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def get_version():
    VERSIONFILE = 'bagou/__init__.py'
    initfile_lines = open(VERSIONFILE, 'rt').readlines()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(VSRE, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError('Unable to find version string in %s.' % (VERSIONFILE,))

setup(
    name='django-bagou',
    version=get_version(),
    packages=[
        'bagou',
        'bagou.management',
        'bagou.management.commands'],
    include_package_data=True,
    license='BSD License',
    description='A simple Django app to conduct Web-based polls.',
    long_description=README,
    url='https://github.com/socketubs/bagou',
    author='Geoffrey Lehée',
    author_email='hello@socketubs.org',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        # TODO: Set to MIT
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # replace these appropriately if you are using Python 3
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
