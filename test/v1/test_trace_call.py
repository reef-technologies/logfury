import logging

from testfixtures import LogCapture

from logfury.v1 import trace_call

logger_name = "testlogger"
logger = logging.getLogger(logger_name)


@trace_call(logger)
def global_foo(a, b, c=None):
    return True


class TestTraceCall:
    def test_global_and_local_name(self):
        @trace_call(logger)
        def local_foo(a, b, c=None):
            return True

        with LogCapture() as l:
            global_foo(1, 2, 3)
            local_foo(1, 2, 3)
            l.check(
                (logger_name, 'DEBUG', 'calling global_foo(a=1, b=2, c=3)'),
                (logger_name, 'DEBUG', 'calling TestTraceCall.test_global_and_local_name.<locals>.local_foo(a=1, b=2, c=3)'),
            )

    def test_all_arguments(self):

        with LogCapture() as l:

            @trace_call(logger)
            def foo(a, b, c=None):
                return True

            foo(1, 2, 3)
            foo(1, b=2)
            l.check(
                (logger_name, 'DEBUG', 'calling {}(a=1, b=2, c=3)'.format(foo.__qualname__)),
                (logger_name, 'DEBUG', 'calling {}(a=1, b=2, c=None)'.format(foo.__qualname__)),
            )

    def test_complex_signature(self):
        with LogCapture() as l:

            @trace_call(logger)
            def foo(a, b, c, d, e, *varargs, f=None, g='G', h='H', i='ii', j='jj', **varkwargs):
                pass

            foo('a', 'b', *['c', 'd'], e='E', f='F', Z='Z', **{'g': 'g', 'h': 'h'})
            l.check(
                (
                    logger_name, 'DEBUG', "calling {}(a='a', b='b', c='c', d='d', e='E', "
                    "varargs=<class 'inspect._empty'>, f='F', g='g', h='h', "
                    "i='ii', j='jj', varkwargs={{'Z': 'Z'}})".format(foo.__qualname__)
                ),
            )

    def test_class(self):
        with LogCapture() as l:

            @trace_call(logger)
            class Ala:
                def __init__(self, a, b, c=None):
                    pass

                def __repr__(self):
                    return '<{} object>'.format(self.__class__.__name__,)

            Ala(1, 2, 3)
            l.check((logger_name, 'DEBUG', 'calling {}(a=1, b=2, c=3)'.format(Ala.__qualname__)),)

    def test_class_that_use_self_object_attributes_in_repr(self):
        with LogCapture() as l:

            @trace_call(logger)
            class Ala:
                def __init__(self, a, b, c=None):
                    self.a = a

                def __repr__(self):
                    # We use self.a here, so the self argument can not be printed in `trace_call`
                    # wrapper as the object is not yet initialized
                    return '<{} a={}>'.format(self.__class__.__name__, self.a)

            Ala(1, 2, 3)
            l.check((logger_name, 'DEBUG', 'calling {}(a=1, b=2, c=3)'.format(Ala.__qualname__)),)

    def test_classmethod(self):
        with LogCapture() as l:

            class MetaAla(type):
                def __repr__(self):
                    return '<{} object>'.format(self.__class__.__name__,)

            class Ala(metaclass=MetaAla):
                @classmethod
                @trace_call(logger)
                def bar(cls, a, b, c=None):
                    return True

                def __repr__(self):
                    return '<{} object>'.format(self.__class__.__name__,)

            a = Ala()
            a.bar(1, 2, 3)
            l.check((logger_name, 'DEBUG', 'calling {}(cls=<MetaAla object>, a=1, b=2, c=3)'.format(a.bar.__qualname__)),)

    def test_staticmethod(self):
        with LogCapture() as l:

            class Bela:
                @staticmethod
                @trace_call(logger)
                def bar(a, b, c=None):
                    return True

                def __repr__(self):
                    return '<{} object>'.format(self.__class__.__name__,)

        with LogCapture() as l:
            b = Bela()
            b.bar(1, 2, 3)
            l.check((logger_name, 'DEBUG', 'calling {}(a=1, b=2, c=3)'.format(b.bar.__qualname__)),)
