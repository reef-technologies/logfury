from abc import abstractmethod

import pytest
from testfixtures import LogCapture

from logfury.v0_1 import AbstractTracePublicCallsMeta, DefaultTraceAbstractMeta


class TestTraceAllPublicCallsMeta:
    def test_subclass(self):
        class Supp(metaclass=AbstractTracePublicCallsMeta):
            @abstractmethod
            def a(self):
                pass

            def __repr__(self):
                return '<%s object>' % (self.__class__.__name__,)

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
                (__name__, 'DEBUG', 'calling %s.bar(self=<Ala object>, a=1, b=2, c=3)' % (self.__class__.__name__,)),
                (__name__, 'DEBUG', 'calling %s.bar(self=<Ala object>, a=1, b=2, c=None)' % (self.__class__.__name__,)),
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
                return '<%s object>' % (self.__class__.__name__,)

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
                (__name__, 'DEBUG', 'calling %s.bar(self=<Ala object>, a=1, b=2, c=3)' % (self.__class__.__name__,)),
                (__name__, 'DEBUG', 'calling %s.bar(self=<Ala object>, a=1, b=2, c=None)' % (self.__class__.__name__,)),
            )

        class Bela(Supp):
            # did not define a()
            def bar(self, a, b, c=None):
                return True

        with pytest.raises(TypeError):
            Bela()
