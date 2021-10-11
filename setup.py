from codecs import open
import os.path
from setuptools import setup, find_packages

################################################################### yapf: disable

NAME         = 'logfury'
VERSION      = '0.1.2'

AUTHOR       = 'Pawel Polewicz'
AUTHOR_EMAIL = 'p.polewicz@gmail.com'

DESCRIPTION  = 'Toolkit for responsible, low-boilerplate logging of library method calls',
LICENSE      = 'BSD'
KEYWORDS     = ['logging', 'tracing']
URL          = 'https://github.com/ppolewicz/logfury'

DOWNLOAD_URL_TEMPLATE = URL + '/tarball/%s'

CLASSIFIERS = [
    'Development Status :: 4 - Beta',

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
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: Jython',
    'Programming Language :: Python :: Implementation :: PyPy',
]

################################################################### yapf: enable

here = os.path.abspath(os.path.dirname(__file__))


def read_file_contents(filename):
    with open(os.path.join(here, filename), 'rb', encoding='utf-8') as f:
        return f.read()


setup(
    name             = NAME,
    version          = VERSION,
    url              = URL,
    download_url     = DOWNLOAD_URL_TEMPLATE % (VERSION,),

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
)  # yapf: disable
