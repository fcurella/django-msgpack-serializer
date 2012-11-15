import os
from setuptools import setup

from msgpack_serializer import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requirements = [
    'Django',
    'msgpack-python'
]

setup(
    name = "django msgpack serializer",
    version = ".".join(map(str, __version__)),
    description = "A MsgPack serializer for Django.",
    long_description = read('README.rst'),
    url = 'https://github.com/fcurella/django-msgpack-serializer',
    license = 'MIT',
    author = 'Flavio Curella',
    author_email = 'flavio.curella@gmail.com',
    packages = ['msgpack_serializer'],
    include_package_data = False,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    install_requires = requirements,
    tests_require = [],
)
