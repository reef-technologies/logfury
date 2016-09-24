from abc import abstractmethod

import six
from testfixtures import LogCapture

from logfury.v0_1 import AbstractTracePublicCallsMeta

from .test_base import TestBase


class TestTraceAllPublicCallsMeta(TestBase):
    def test_subclass(self):
        @six.add_metaclass(AbstractTracePublicCallsMeta)
        class Supp(object):
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
                (__name__, 'DEBUG', 'calling %sbar(self=<Ala object>, a=1, b=2, c=3)' % (self._get_prefix(),)),
                (__name__, 'DEBUG', 'calling %sbar(self=<Ala object>, a=1, b=2)' % (self._get_prefix(),)),
            )

        class Bela(Supp):
            # did not define a()
            def bar(self, a, b, c=None):
                return True

        with self.assertRaises(TypeError):
            Bela()
