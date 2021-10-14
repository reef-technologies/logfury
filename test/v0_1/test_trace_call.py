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

    def test_class(self):
        with LogCapture() as l:

            @trace_call(logger)
            class Ala:
                def __init__(a, b, c=None):
                    pass

            Ala(1, 2, 3)
            l.check((logger_name, 'DEBUG', 'calling %s.__init__(a=1, b=2, c=3)' % (self.__class__.__name__,)),)

    def test_classmethod(self):
        with LogCapture() as l:

            class MetaAla(type):
                def __repr__(self):
                    return '<%s object>' % (self.__class__.__name__,)

            class Ala(metaclass=MetaAla):
                @classmethod
                @trace_call(logger)
                def bar(cls, a, b, c=None):
                    return True

                def __repr__(self):
                    return '<%s object>' % (self.__class__.__name__,)

            a = Ala()
            a.bar(1, 2, 3)
            l.check((logger_name, 'DEBUG', 'calling %s.bar(cls=<MetaAla object>, a=1, b=2, c=3)' % (self.__class__.__name__,)),)

    def test_staticmethod(self):
        with LogCapture() as l:

            class Bela:
                @staticmethod
                @trace_call(logger)
                def bar(a, b, c=None):
                    return True

                def __repr__(self):
                    return '<%s object>' % (self.__class__.__name__,)

        with LogCapture() as l:
            b = Bela()
            b.bar(1, 2, 3)
            l.check((logger_name, 'DEBUG', 'calling %s.bar(a=1, b=2, c=3)' % (self.__class__.__name__,)),)
