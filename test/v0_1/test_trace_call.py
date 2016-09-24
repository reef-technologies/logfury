from testfixtures import LogCapture

from logfury.v0_1 import trace_call

from .test_base import TestBase


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
                (self.base_logger_name, 'DEBUG', 'calling %sfoo(a=1, b=2)' % (self._get_prefix(),)),
            )
