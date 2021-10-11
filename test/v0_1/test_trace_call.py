import logging

from testfixtures import LogCapture

from logfury.v0_1 import trace_call

logger_name = "testlogger"
logger = logging.getLogger(logger_name)


class TestTraceCall:
    def test_all_arguments(self):

        with LogCapture() as l:

            @trace_call(logger)
            def foo(a, b, c=None):
                return True

            foo(1, 2, 3)
            foo(1, b=2)
            l.check(
                (logger_name, 'DEBUG', 'calling %s.foo(a=1, b=2, c=3)' % (self.__class__.__name__,)),
                (logger_name, 'DEBUG', 'calling %s.foo(a=1, b=2, c=None)' % (self.__class__.__name__,)),
            )

    def test_complex_signature(self):
        with LogCapture() as l:

            @trace_call(logger)
            def foo(a, b, c, d, e, *varargs_, f=None, g='G', h='H', i='ii', j='jj', **varkwargs_: None):
                pass

            foo('a', 'b', *['c', 'd'], e='E', f='F', Z='Z', **{'g': 'g', 'h': 'h'})
            l.check(
                (
                    logger_name, 'DEBUG', "calling %s.foo(a='a', b='b', c='c', d='d', e='E', f='F', "
                    "g='g', h='h', varkwargs_={'Z': 'Z'}, varargs_=<class 'inspect._empty'>, "
                    "i='ii', j='jj')" % (self.__class__.__name__,)
                ),
            )
