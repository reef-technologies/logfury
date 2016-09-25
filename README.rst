========
Logfury
========

Logfury is for python library maintainers. It allows for responsible, low-boilerplate logging of method calls.

*****************
License
*****************

BSD 3-clause

*****************************
whats with the weird import
*****************************

.. sourcecode:: python

    from logfury.v0_1 import DefaultTraceMeta

If you were to use logfury in your library, any change to the API could potentially break your program. Nobody wants that.

Thanks to this import trick I can keep the 0.1.x API very stable. At the same time I can change the functionality of the library and change default behavior of version 0.2.x etc, without changing the name of the package. This way YOU decide when to adopt potentially incompatible API changes, by incrementing the API version on import.


*****************
Installation
*****************

^^^^^^^^^^^^^^^^^^^^
Current stable
^^^^^^^^^^^^^^^^^^^^

::

    pip install logfury

^^^^^^^^^^^^^^^^^^^^
Development version
^^^^^^^^^^^^^^^^^^^^

::

    git clone git@github.com:ppolewicz/logfury.git
    python setup.py install


*****************
Basic usage
*****************

^^^^^^^^^^^^^^^^^^^^^^^^^^^
DefaultTraceMeta metaclass
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. sourcecode:: pycon

    >>> import logging
    >>> import six
    >>>
    >>> from logfury.v0_1 import DefaultTraceMeta, limit_trace_arguments, disable_trace
    >>>
    >>>
    >>> logging.basicConfig()
    >>> logger = logging.getLogger(__name__)
    >>> logger.setLevel(logging.DEBUG)
    >>>
    >>>
    >>> @six.add_metaclass(DefaultTraceMeta)
    >>> class Foo(object):
    ...     def baz(self, a, b, c=None):
    ...         return True
    ...     def get_blah(self):
    ...         return 5
    ...     def _hello(self):
    ...         pass
    ...     @disable_trace
    ...     def world(self):
    ...         pass
    ...     def __repr__(self):
    ...         return '<%s object>' % (self.__class__.__name__,)
    ...
    >>> class Bar(Foo):
    ...     def baz(self, a, b, c=None):
    ...         b += 1
    ...         return super(Bar, self).baz(a, b, c)
    ...     def world(self):
    ...         pass
    ...     @limit_trace_arguments(skip=['password'])
    ...     def secret(self, password, other):
    ...         pass
    ...     @limit_trace_arguments(only=['other'])
    ...     def secret2(self, password, other):
    ...         pass
    ...
    >>> a = Foo()
    >>> a.baz(1, 2, 3)
    DEBUG:__main__:calling Foo.baz(self=<Foo object>, a=1, b=2, c=3)
    >>> a.baz(4, b=8)
    DEBUG:__main__:calling Foo.baz(self=<Foo object>, a=4, b=8)
    >>> a.get_blah()  # nothing happens, since v0_1.DefaultTraceMeta does not trace "get_.*"
    >>> a._hello()  # nothing happens, since v0_1.DefaultTraceMeta does not trace "_.*"
    >>> a.world()  # nothing happens, since v0_1.DefaultTraceMeta does not trace "_.*"
    >>> b = Bar()
    >>> b.baz(4, b=8)  # tracing is inherited
    DEBUG:__main__:calling Bar.baz(self=<Bar object>, a=4, b=8)
    DEBUG:__main__:calling Foo.baz(self=<Bar object>, a=4, b=9, c=None)
    >>> b.world()  # nothing happens, since Foo.world() tracing was disabled and Bar inherited it
    >>> b.secret('correct horse battery staple', 'Hello world!')
    DEBUG:__main__:calling Bar.secret(self=<Bar object>, other='Hello world!') (hidden args: password)
    >>> b.secret2('correct horse battery staple', 'Hello world!')
    DEBUG:__main__:calling Bar.secret2(other='Hello world!') (hidden args: self, password)


^^^^^^^^^^^^^^^^^^^^
trace_call decorator
^^^^^^^^^^^^^^^^^^^^

.. sourcecode:: pycon

    >>> import logging
    >>> from logfury import *
    >>> logging.basicConfig()
    >>> logger = logging.getLogger(__name__)
    >>>
    >>> @trace_call(logger)
    ... def foo(a, b, c=None):
    ...     return True
    ...
    >>> foo(1, 2, 3)
    True
    >>> logger.setLevel(logging.DEBUG)
    >>> foo(1, 2, 3)
    DEBUG:__main__:calling foo(a=1, b=2, c=3)
    True
    >>> foo(1, b=2)
    DEBUG:__main__:calling foo(a=1, b=2)
    True
    >>>
