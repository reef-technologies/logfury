from testfixtures import LogCapture

from logfury.v0_1 import TraceAllPublicCallsMeta, limit_trace_arguments, disable_trace


class TestTraceAllPublicCallsMeta:
    def test_subclass(self):
        class Ala(metaclass=TraceAllPublicCallsMeta):
            def bar(self, a, b, c=None):
                return True

            def __repr__(self):
                return '<%s object>' % (self.__class__.__name__,)

        class Bela(Ala):
            def bar(self, a, b, c=None):
                return False

        with LogCapture() as l:
            a = Ala()
            a.bar(1, 2, 3)
            a.bar(1, b=2)
            l.check(
                (__name__, 'DEBUG', 'calling %s.bar(self=<Ala object>, a=1, b=2, c=3)' % (self.__class__.__name__,)),
                (__name__, 'DEBUG', 'calling %s.bar(self=<Ala object>, a=1, b=2, c=None)' % (self.__class__.__name__,)),
            )

        with LogCapture() as l:
            b = Bela()
            b.bar(1, 2, 3)
            b.bar(1, b=2)

            l.check(
                (__name__, 'DEBUG', 'calling %s.bar(self=<Bela object>, a=1, b=2, c=3)' % (self.__class__.__name__,)),
                (__name__, 'DEBUG', 'calling %s.bar(self=<Bela object>, a=1, b=2, c=None)' % (self.__class__.__name__,)),
            )

    def test_disable_trace(self):
        class Ala(metaclass=TraceAllPublicCallsMeta):
            @disable_trace
            def bar(self, a, b, c=None):
                return True

            def __repr__(self):
                return '<%s object>' % (self.__class__.__name__,)

        class Bela(Ala):
            def bar(self, a, b, c=None):
                return False

        with LogCapture() as l:
            a = Ala()
            a.bar(1, 2, 3)
            a.bar(1, b=2)
            b = Bela()
            b.bar(1, 2, 3)
            b.bar(1, b=2)
            l.check()

    def test_empty_only(self):
        class Ala(metaclass=TraceAllPublicCallsMeta):
            @limit_trace_arguments(only=tuple())
            def bar(self, a, b, c=None):
                return True

            def __repr__(self):
                return '<%s object>' % (self.__class__.__name__,)

        class Bela(Ala):
            def bar(self, a, b, c=None):
                return False

        with LogCapture() as l:
            a = Ala()
            a.bar(1, 2, 3)
            a.bar(1, b=2)
            b = Bela()
            b.bar(1, 2, 3)
            b.bar(1, b=2)
            l.check(
                (__name__, 'DEBUG', 'calling %s.bar() (hidden args: self, a, b, c)' % (self.__class__.__name__,)),
                (__name__, 'DEBUG', 'calling %s.bar() (hidden args: self, a, b, c)' % (self.__class__.__name__,)),
                (__name__, 'DEBUG', 'calling %s.bar() (hidden args: self, a, b, c)' % (self.__class__.__name__,)),
                (__name__, 'DEBUG', 'calling %s.bar() (hidden args: self, a, b, c)' % (self.__class__.__name__,)),
            )

    def test_skip(self):
        class Ala(metaclass=TraceAllPublicCallsMeta):
            @limit_trace_arguments(skip=['a'])
            def bar(self, a, b, c=None):
                return True

            def __repr__(self):
                return '<%s object>' % (self.__class__.__name__,)

        class Bela(Ala):
            def bar(self, a, b, c=None):
                return False

        with LogCapture() as l:
            a = Ala()
            a.bar(1, 2, 3)
            a.bar(1, b=2)
            b = Bela()
            b.bar(1, 2, 3)
            b.bar(1, b=2)
            l.check(
                (__name__, 'DEBUG', 'calling %s.bar(self=<Ala object>, b=2, c=3) (hidden args: a)' % (self.__class__.__name__,)),
                (__name__, 'DEBUG', 'calling %s.bar(self=<Ala object>, b=2, c=None) (hidden args: a)' % (self.__class__.__name__,)),
                (__name__, 'DEBUG', 'calling %s.bar(self=<Bela object>, b=2, c=3) (hidden args: a)' % (self.__class__.__name__,)),
                (__name__, 'DEBUG', 'calling %s.bar(self=<Bela object>, b=2, c=None) (hidden args: a)' % (self.__class__.__name__,)),
            )

    def test_only(self):
        class Ala(metaclass=TraceAllPublicCallsMeta):
            @limit_trace_arguments(only=['a'])
            def bar(self, a, b, c=None):
                return True

            def __repr__(self):
                return '<%s object>' % (self.__class__.__name__,)

        class Bela(Ala):
            def bar(self, a, b, c=None):
                return False

        with LogCapture() as l:
            a = Ala()
            a.bar(1, 2, 3)
            a.bar(1, b=2)
            b = Bela()
            b.bar(1, 2, 3)
            b.bar(1, b=2)
            l.check(
                (__name__, 'DEBUG', 'calling %s.bar(a=1) (hidden args: self, b, c)' % (self.__class__.__name__,)),
                (__name__, 'DEBUG', 'calling %s.bar(a=1) (hidden args: self, b, c)' % (self.__class__.__name__,)),
                (__name__, 'DEBUG', 'calling %s.bar(a=1) (hidden args: self, b, c)' % (self.__class__.__name__,)),
                (__name__, 'DEBUG', 'calling %s.bar(a=1) (hidden args: self, b, c)' % (self.__class__.__name__,)),
            )

    def test_skip_and_only(self):
        class Ala(metaclass=TraceAllPublicCallsMeta):
            @limit_trace_arguments(only=['self', 'a', 'b'], skip=['a'])
            def bar(self, a, b, c=None):
                return True

            def __repr__(self):
                return '<%s object>' % (self.__class__.__name__,)

        class Bela(Ala):
            def bar(self, a, b, c=None):
                return False

        with LogCapture() as l:
            a = Ala()
            a.bar(1, 2, 3)
            a.bar(1, b=2)
            b = Bela()
            b.bar(1, 2, 3)
            b.bar(1, b=2)
            l.check(
                (__name__, 'DEBUG', 'calling %s.bar(self=<Ala object>, b=2) (hidden args: a, c)' % (self.__class__.__name__,)),
                (__name__, 'DEBUG', 'calling %s.bar(self=<Ala object>, b=2) (hidden args: a, c)' % (self.__class__.__name__,)),
                (__name__, 'DEBUG', 'calling %s.bar(self=<Bela object>, b=2) (hidden args: a, c)' % (self.__class__.__name__,)),
                (__name__, 'DEBUG', 'calling %s.bar(self=<Bela object>, b=2) (hidden args: a, c)' % (self.__class__.__name__,)),
            )

    def test_class(self):
        class Ala(metaclass=TraceAllPublicCallsMeta):
            class Bela:
                def __init__(self, a, b, c=None):
                    pass

                def __repr__(self):
                    return '<%s object>' % (self.__class__.__name__,)

            def __repr__(self):
                return '<%s object>' % (self.__class__.__name__,)

        with LogCapture() as l:
            a = Ala()
            a.Bela(1, 2, 3)
            Ala.Bela(1, 2, 3)
            l.check(
                (__name__, 'DEBUG', 'calling %s.__init__(self=<Bela object>, a=1, b=2, c=3)' % (self.__class__.__name__,)),
                (__name__, 'DEBUG', 'calling %s.__init__(self=<Bela object>, a=1, b=2, c=3)' % (self.__class__.__name__,)),
            )

    def test_classmethod(self):
        class MetaAla(TraceAllPublicCallsMeta):
            def __repr__(self):
                return '<%s object>' % (self.__class__.__name__,)

        class Ala(metaclass=MetaAla):
            @classmethod
            def bar(cls, a, b, c=None):
                return True

            def __repr__(self):
                return '<%s object>' % (self.__class__.__name__,)

        with LogCapture() as l:
            a = Ala()
            a.bar(1, 2, 3)
            l.check((__name__, 'DEBUG', 'calling %s.bar(cls=<MetaAla object>, a=1, b=2, c=3)' % (self.__class__.__name__,)),)

    def test_staticmethod(self):
        def ala(a, b, c=None):
            pass

        class Ala:
            def __init__(self, a, b, c=None):
                pass

            def __repr__(self):
                return '<%s object>' % (self.__class__.__name__,)

        class Bela(metaclass=TraceAllPublicCallsMeta):

            foo = staticmethod(ala)
            Foo = staticmethod(Ala)

            @staticmethod
            def bar(a, b, c=None):
                return True

            def __repr__(self):
                return '<%s object>' % (self.__class__.__name__,)

        with LogCapture() as l:
            b = Bela()
            b.foo(1, 2, 3)
            b.Foo(1, 2, 3)
            b.bar(1, 2, 3)
            l.check(
                (__name__, 'DEBUG', 'calling %s.ala(a=1, b=2, c=3)' % (self.__class__.__name__,)),
                (__name__, 'DEBUG', 'calling %s.__init__(self=<Ala object>, a=1, b=2, c=3)' % (self.__class__.__name__,)),
                (__name__, 'DEBUG', 'calling %s.bar(a=1, b=2, c=3)' % (self.__class__.__name__,)),
            )
