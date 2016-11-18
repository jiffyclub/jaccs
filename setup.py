import os
import sys

import setuptools

# Get version information without importing the package
__version__ = None
with open(os.path.join('jaccs', 'version.py'), 'r') as f:
    exec(f.read())

SHORT_DESCRIPTION = 'Write strings to access nested JSON objects'
with open('README.rst', 'r') as f:
    LONG_DESCRIPTION = f.read()

SETUP_DEPENDENCIES = []
if {'pytest', 'test'}.intersection(sys.argv):
    SETUP_DEPENDENCIES.append('pytest-runner')

setuptools.setup(
    name='jaccs',
    version=__version__,
    author='Matt Davis',
    author_email='jiffyclub@gmail.com',
    url='https://github.com/jiffyclub/jaccs',
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=['jaccs'],
    tests_require=['pytest >= 3.0'],
    setup_requires=SETUP_DEPENDENCIES,
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ])
