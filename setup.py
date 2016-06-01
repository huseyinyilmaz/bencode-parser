from setuptools import find_packages
from setuptools import setup

VERSION = 0.1

DESCRIPTION = 'encoder library for bencode format.'


setup(
    name='python-bencode',
    version=VERSION,
    description=DESCRIPTION,
    url='https://github.com/huseyinyilmaz/python-bencode',
    author='Huseyin Yilmaz',
    author_email='yilmazhuseyin@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='tests',
    tests_require=[
        'pyparsing>=2.1.4',
    ],
)
