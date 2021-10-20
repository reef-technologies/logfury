# noqa

import os.path
from codecs import open

from setuptools import find_packages, setup

################################################################### yapf: disable

NAME         = 'logfury'

AUTHOR       = 'Pawel Polewicz'
AUTHOR_EMAIL = 'p.polewicz@gmail.com'

DESCRIPTION  = 'Toolkit for responsible, low-boilerplate logging of library method calls',
LICENSE      = 'BSD'
KEYWORDS     = ['logging', 'tracing']
URL          = 'https://github.com/reef-technologies/logfury'
DOWNLOAD_URL = URL + '/releases'

CLASSIFIERS = [
    'Development Status :: 6 - Mature',

    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: System :: Logging',

    'Natural Language :: English',

    'License :: OSI Approved :: BSD License',

    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
]

################################################################### yapf: enable

here = os.path.abspath(os.path.dirname(__file__))


def read_file_contents(filename):
    with open(os.path.join(here, filename), 'rb', encoding='utf-8') as f:
        return f.read()


setup(
    name             = NAME,
    url              = URL,
    download_url     = DOWNLOAD_URL,

    author           = AUTHOR,
    author_email     = AUTHOR_EMAIL,
    maintainer       = AUTHOR,
    maintainer_email = AUTHOR_EMAIL,

    packages         = find_packages(exclude=['test*']),
    license          = LICENSE,

    description      = DESCRIPTION,
    long_description = read_file_contents('README.rst'),
    keywords         = KEYWORDS,

    classifiers      = CLASSIFIERS,
    package_data     = {NAME: ['requirements.txt', 'LICENSE']},

    setup_requires   = ['setuptools_scm<6.0'],  # setuptools_scm>=6.0 doesn't support Python 3.5
    use_scm_version  = True,
)  # yapf: disable
