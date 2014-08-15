"""
Main module for pepperstack
Calls pepperstack with formatted parameters

"""

import sys

from .cli import cli

if __name__ == "__main__":
    args = []
    kwargs = {}
    sys.argv.pop(0)
    for a in sys.argv:
        if a.find('='):
            (k, v) = a.split('=')
            kwargs[k] = v
        else:
            args.append(a)
    print "Args: {0}\nKwargs: {1}".format(args, kwargs)
