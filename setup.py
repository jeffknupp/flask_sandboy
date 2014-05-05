from __future__ import print_function
from setuptools import setup, find_packages
import codecs
import os
import sys
import re

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

long_description = read('README.rst')

setup(
    name='flask_sandboy',
    version=find_version('flask_sandboy', '__init__.py'),
    url='http://github.com/jeffknupp/flask_sandboy/',
    license='BSD License',
    author='Jeff Knupp',
    install_requires=['Flask>=0.10.1',
                      ],
    author_email='jeff@jeffknupp.com',
    description='Automated REST APIs for SQLAlchemy models',
    long_description=long_description,
    packages=['flask_sandboy'],
    include_package_data=True,
    platforms='any',
    zip_safe=False,
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
)
