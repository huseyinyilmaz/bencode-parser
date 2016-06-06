import os
from setuptools import find_packages
from setuptools import setup

VERSION = '1.0.1'

DESCRIPTION = ('Library that encodes/decodes bencode formated strings to'
               'python objects.')

# read long description from the file
path = os.path.join(os.path.dirname(__file__), 'README.rst')
with open(path) as f:
    LONG_DESCRIPTION = f.read()

REQUIREMENTS = ['six',
                'pyparsing>=2.1.4',
                ]

setup(
    name='bencode-parser',
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url='https://github.com/huseyinyilmaz/python-bencode',
    author='Huseyin Yilmaz',
    author_email='yilmazhuseyin@gmail.com',
    packages=find_packages(),
    py_modules=['bencode'],
    include_package_data=True,
    zip_safe=False,
    test_suite='tests',
    tests_require=REQUIREMENTS,
    install_requires=REQUIREMENTS,
)
