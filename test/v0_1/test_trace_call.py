from nose import SkipTest
import six
from testfixtures import LogCapture

from logfury.v0_1 import trace_call

from .test_base import TestBase

try:
    from inspect import signature
    INSPECT_MODULE_NAME = 'inspect'
except ImportError:
    INSPECT_MODULE_NAME = 'funcsigs'
    from funcsigs import signature
assert signature


class TestTraceCall(TestBase):
    def test_all_arguments(self):
        with LogCapture() as l:

            @trace_call(self.logger)
            def foo(a, b, c=None):
                return True

            foo(1, 2, 3)
            foo(1, b=2)
            l.check(
                (self.base_logger_name, 'DEBUG', 'calling %sfoo(a=1, b=2, c=3)' % (self._get_prefix(),)),
                (self.base_logger_name, 'DEBUG', 'calling %sfoo(a=1, b=2, c=None)' % (self._get_prefix(),)),
            )

    def test_complex_signature_py2(self):
        with LogCapture() as l:

            @trace_call(self.logger)
            def foo(a, b, c, d, e, g='G', h='H', i='ii', j='jj', *varargs_, **varkwargs_):
                pass

            foo('a', 'b', *['c', 'd'], e='E', Z='Z', **{'g': 'g', 'h': 'h'})

            l.check(
                (
                    'test.v0_1.test_base', 'DEBUG', "calling %sfoo(a='a', b='b', c='c', d='d', e='E', "
                    "g='g', h='h', varkwargs_={'Z': 'Z'}, "
                    "i='ii', j='jj', varargs_=<class '%s._empty'>)" % (self._get_prefix(), INSPECT_MODULE_NAME)
                ),
            )

    def test_complex_signature_py3(self):
        if six.PY2:
            raise SkipTest()
        with LogCapture() as l:
            # without this exec Python 2 and pyflakes complain about syntax errors etc
            exec (
                """@trace_call(self.logger)
def foo(a, b, c, d, e, *varargs_, f=None, g='G', h='H', i='ii', j='jj', **varkwargs_: None):
    pass
foo('a', 'b', *['c', 'd'], e='E', f='F', Z='Z', **{'g':'g', 'h':'h'})
""", locals(), globals()
            )
            l.check(
                (
                    'test.v0_1.test_base',
                    'DEBUG',
                    "calling foo(a='a', b='b', c='c', d='d', e='E', f='F', "
                    "g='g', h='h', varkwargs_={'Z': 'Z'}, varargs_=<class '%s._empty'>, "
                    "i='ii', j='jj')" % (INSPECT_MODULE_NAME,)  # prefix does not work because of the eval, inspect module is for pypy3
                ),
            )
