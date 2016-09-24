from __future__ import print_function

from functools import wraps
import inspect
import itertools
import logging

import six

from .utils import get_class_that_defined_method, OrderedDict


class trace_call(object):
    """
    A decorator which causes the function execution to be logged using a passed logger
    """

    LEVEL = logging.DEBUG

    def __init__(self, logger, only=None, skip=None):
        """
            only - if not None, contains a whitelist (tuple of names) of arguments
                   that are safe to be logged. All others can not be logged.
            skip - if not None, contains a whitelist (tuple of names) of arguments
                   that are not safe to be logged.
        """
        self.logger = logger
        self.only = only
        self.skip = skip

    def __call__(self, function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if self.logger.isEnabledFor(self.LEVEL):
                #print(inspect.getargspec(function)[0])
                args_names = OrderedDict.fromkeys(
                    itertools.chain(inspect.getargspec(function)[0], six.iterkeys(kwargs))
                )  # yapf: disable
                args_dict = OrderedDict(
                    itertools.chain(six.moves.zip(args_names, args), six.iteritems(kwargs))
                )  # yapf: disable

                # filter arguments
                output_arg_names = []
                skipped_arg_names = []
                if self.skip is not None and self.only is not None:
                    for arg in six.iterkeys(args_dict):
                        if arg in self.only and arg not in self.skip:
                            output_arg_names.append(arg)
                        else:
                            skipped_arg_names.append(arg)
                elif self.only is not None:
                    for arg in six.iterkeys(args_dict):
                        if arg in self.only:
                            output_arg_names.append(arg)
                        else:
                            skipped_arg_names.append(arg)
                elif self.skip is not None:
                    for arg in six.iterkeys(args_dict):
                        if arg in self.skip:
                            skipped_arg_names.append(arg)
                        else:
                            output_arg_names.append(arg)
                else:
                    output_arg_names = args_dict

                # format output
                suffix = ''
                if skipped_arg_names:
                    suffix = ' (hidden args: %s)' % (', '.join(skipped_arg_names))
                arguments = ', '.join('%s=%s' % (k, repr(args_dict[k])) for k in output_arg_names)

                #if six.PY3 and len(args_dict) != 3:
                #    #print([k for k in args_dict])
                #    print(arguments, output_arg_names, args_dict, list(k for k in args_dict))
                #    #assert False

                function_name = function.__name__
                klass = get_class_that_defined_method(function)
                if klass is not None:
                    function_name = '%s.%s' % (klass.__name__, function_name)

                # actually log the call
                self.logger.log(self.LEVEL, 'calling %s(%s)%s', function_name, arguments, suffix)
            return function(*args, **kwargs)

        return wrapper
