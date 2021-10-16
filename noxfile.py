import os
from glob import glob

import nox

CI = os.environ.get('CI') is not None
NOX_PYTHONS = os.environ.get('NOX_PYTHONS')

PYTHON_VERSIONS = [
    '3.5',
    '3.6',
    '3.7',
    '3.8',
    '3.9',
    '3.10',
] if NOX_PYTHONS is None else NOX_PYTHONS.split(',')
PYTHON_DEFAULT_VERSION = PYTHON_VERSIONS[-1]

PY_PATHS = ['logfury', 'test', 'noxfile.py', 'setup.py']

REQUIREMENTS_FORMAT = ['yapf==0.27']
REQUIREMENTS_LINT = [*REQUIREMENTS_FORMAT, 'flake8==4.0.1', 'pytest==6.2.5']
REQUIREMENTS_TEST = [
    "pytest==6.2.5;python_version>'3.5'",
    "pytest==6.1.1;python_version=='3.5'",
    "pytest-cov==3.0.0;python_version>'3.5'",
    "pytest-cov==2.10.1;python_version=='3.5'",
    "testfixtures==6.18.3",
]
REQUIREMENTS_COVER = ['cover']
REQUIREMENTS_BUILD = ['setuptools>=20.2']

nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = [
    'lint',
    'test',
]

# In CI, use Python interpreter provided by GitHub Actions
if CI:
    nox.options.force_venv_backend = 'none'


def install_myself(session, extras=None):
    """Install from the source."""
    arg = '.'
    if extras:
        arg += '[{}]'.format(','.join(extras))

    session.install('-e', arg)


@nox.session(name='format', python=PYTHON_DEFAULT_VERSION)
def format_(session):
    """Format the code."""
    session.install(*REQUIREMENTS_FORMAT)
    session.run('yapf', '--in-place', '--parallel', '--recursive', *PY_PATHS)


@nox.session(python=PYTHON_DEFAULT_VERSION)
def lint(session):
    """Run linters."""
    install_myself(session)
    session.install(*REQUIREMENTS_LINT)
    session.run('yapf', '--diff', '--parallel', '--recursive', *PY_PATHS)
    session.run('flake8', *PY_PATHS)


@nox.session(python=PYTHON_VERSIONS)
def test(session):
    """Run unit tests."""
    install_myself(session)
    session.install(*REQUIREMENTS_TEST)
    args = ['--cov=logfury', '--cov-branch', '--cov-report=xml', '--doctest-modules']
    session.run('pytest', *args, *session.posargs, 'test')

    if not session.posargs:
        session.notify('cover')


@nox.session
def cover(session):
    """Perform coverage analysis."""
    session.install(*REQUIREMENTS_COVER)
    session.run('coverage', 'report', '--fail-under=75', '--show-missing', '--skip-covered')
    session.run('coverage', 'erase')


@nox.session(python=PYTHON_DEFAULT_VERSION)
def build(session):
    """Build the distribution."""
    session.install(*REQUIREMENTS_BUILD)
    session.run('python', 'setup.py', 'check', '--metadata', '--strict')
    session.run('rm', '-rf', 'build', 'dist', 'logfury.egg-info', external=True)
    session.run('python', 'setup.py', 'bdist_wheel', *session.posargs)

    # Set outputs for GitHub Actions
    if CI:
        asset_path = glob('dist/*')[0]
        print('::set-output name=asset_path::', asset_path, sep='')

        version = os.environ['GITHUB_REF'].replace('refs/tags/v', '')
        print('::set-output name=version::', version, sep='')
