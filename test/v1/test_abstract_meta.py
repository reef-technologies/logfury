from abc import abstractmethod

import pytest
from testfixtures import LogCapture

from logfury.v1 import AbstractTracePublicCallsMeta, DefaultTraceAbstractMeta


class TestTraceAllPublicCallsMeta:
    def test_subclass(self):
        class Supp(metaclass=AbstractTracePublicCallsMeta):
            @abstractmethod
            def a(self):
                pass

            def __repr__(self):
                return '<{} object>'.format(self.__class__.__name__,)

        class Ala(Supp):
            def a(self):
                pass

            def bar(self, a, b, c=None):
                return True

        a = Ala()
        a.bar(1, 2, 3)
        a.bar(1, b=2)

        with LogCapture() as l:
            a = Ala()
            a.bar(1, 2, 3)
            a.bar(1, b=2)
            l.check(
                (__name__, 'DEBUG', 'calling {}(self=<Ala object>, a=1, b=2, c=3)'.format(a.bar.__qualname__)),
                (__name__, 'DEBUG', 'calling {}(self=<Ala object>, a=1, b=2, c=None)'.format(a.bar.__qualname__)),
            )

        class Bela(Supp):
            # did not define a()
            def bar(self, a, b, c=None):
                return True

        with pytest.raises(TypeError):
            Bela()


class TestDefaultTraceAbstractMeta(TestTraceAllPublicCallsMeta):
    def test_subclass(self):
        class Supp(metaclass=DefaultTraceAbstractMeta):
            @abstractmethod
            def a(self):
                pass

            def __repr__(self):
                return '<{} object>'.format(self.__class__.__name__,)

        class Ala(Supp):
            def a(self):
                pass

            def bar(self, a, b, c=None):
                return True

        a = Ala()
        a.bar(1, 2, 3)
        a.bar(1, b=2)

        with LogCapture() as l:
            a = Ala()
            a.bar(1, 2, 3)
            a.bar(1, b=2)
            l.check(
                (__name__, 'DEBUG', 'calling {}(self=<Ala object>, a=1, b=2, c=3)'.format(a.bar.__qualname__)),
                (__name__, 'DEBUG', 'calling {}(self=<Ala object>, a=1, b=2, c=None)'.format(a.bar.__qualname__)),
            )

        class Bela(Supp):
            # did not define a()
            def bar(self, a, b, c=None):
                return True

        with pytest.raises(TypeError):
            Bela()
