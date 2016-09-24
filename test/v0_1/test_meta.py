import six
from testfixtures import LogCapture

from logfury.v0_1 import TraceAllPublicCallsMeta, limit_trace_arguments, disable_trace

from .test_base import TestBase


class TestTraceAllPublicCallsMeta(TestBase):
    def test_subclass(self):
        @six.add_metaclass(TraceAllPublicCallsMeta)
        class Ala(object):
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
                (__name__, 'DEBUG', 'calling %sbar(self=<Ala object>, a=1, b=2, c=3)' % (self._get_prefix(),)),
                (__name__, 'DEBUG', 'calling %sbar(self=<Ala object>, a=1, b=2)' % (self._get_prefix(),)),
            )

        with LogCapture() as l:
            b = Bela()
            b.bar(1, 2, 3)
            b.bar(1, b=2)

            l.check(
                (__name__, 'DEBUG', 'calling %sbar(self=<Bela object>, a=1, b=2, c=3)' % (self._get_prefix(),)),
                (__name__, 'DEBUG', 'calling %sbar(self=<Bela object>, a=1, b=2)' % (self._get_prefix(),)),
            )

    def test_disable_trace(self):
        @six.add_metaclass(TraceAllPublicCallsMeta)
        class Ala(object):
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
        @six.add_metaclass(TraceAllPublicCallsMeta)
        class Ala(object):
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
                (__name__, 'DEBUG', 'calling %sbar() (hidden args: self, a, b, c)' % (self._get_prefix(),)),
                (__name__, 'DEBUG', 'calling %sbar() (hidden args: self, a, b)' % (self._get_prefix(),)),
                (__name__, 'DEBUG', 'calling %sbar() (hidden args: self, a, b, c)' % (self._get_prefix(),)),
                (__name__, 'DEBUG', 'calling %sbar() (hidden args: self, a, b)' % (self._get_prefix(),)),
            )

    def test_skip(self):
        @six.add_metaclass(TraceAllPublicCallsMeta)
        class Ala(object):
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
                (__name__, 'DEBUG', 'calling %sbar(self=<Ala object>, b=2, c=3) (hidden args: a)' % (self._get_prefix(),)),
                (__name__, 'DEBUG', 'calling %sbar(self=<Ala object>, b=2) (hidden args: a)' % (self._get_prefix(),)),
                (__name__, 'DEBUG', 'calling %sbar(self=<Bela object>, b=2, c=3) (hidden args: a)' % (self._get_prefix(),)),
                (__name__, 'DEBUG', 'calling %sbar(self=<Bela object>, b=2) (hidden args: a)' % (self._get_prefix(),)),
            )

    def test_only(self):
        @six.add_metaclass(TraceAllPublicCallsMeta)
        class Ala(object):
            #@limit_trace_arguments(only=['self', 'a', 'b'], skip=['a'])
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
                (__name__, 'DEBUG', 'calling %sbar(a=1) (hidden args: self, b, c)' % (self._get_prefix(),)),
                (__name__, 'DEBUG', 'calling %sbar(a=1) (hidden args: self, b)' % (self._get_prefix(),)),
                (__name__, 'DEBUG', 'calling %sbar(a=1) (hidden args: self, b, c)' % (self._get_prefix(),)),
                (__name__, 'DEBUG', 'calling %sbar(a=1) (hidden args: self, b)' % (self._get_prefix(),)),
            )

    def test_skip_and_only(self):
        @six.add_metaclass(TraceAllPublicCallsMeta)
        class Ala(object):
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
                (__name__, 'DEBUG', 'calling %sbar(self=<Ala object>, b=2) (hidden args: a, c)' % (self._get_prefix(),)),
                (__name__, 'DEBUG', 'calling %sbar(self=<Ala object>, b=2) (hidden args: a)' % (self._get_prefix(),)),
                (__name__, 'DEBUG', 'calling %sbar(self=<Bela object>, b=2) (hidden args: a, c)' % (self._get_prefix(),)),
                (__name__, 'DEBUG', 'calling %sbar(self=<Bela object>, b=2) (hidden args: a)' % (self._get_prefix(),)),
            )
