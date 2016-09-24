from __future__ import print_function

from contextlib import contextmanager
import logging
import platform
import six
import unittest


class TestBase(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        self.base_logger_name = __name__

    def _get_prefix(self):
        if six.PY2 or platform.python_implementation() == 'PyPy':
            return ''
        else:
            return self.__class__.__name__ + '.'

    @contextmanager
    def assertRaises(self, exc):
        try:
            yield
        except exc:
            pass
        else:
            assert False, 'should have thrown %s' % (exc,)
