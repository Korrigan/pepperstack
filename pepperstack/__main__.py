"""
Main module for pepperstack
Calls pepperstack with formatted parameters

"""

import sys

from .cli import cli

def usage(exit=1):
    """
    Prints a brief usage on stdout and exit

    """
    print "Usage: pepper <command> [arg[=value], ...]"
    print ""
    print "Run `pepper help` for more info"
    sys.exit(exit)


def main():
    """
    Main function for pepperstack

    """
    args = []
    kwargs = {}
    cmd = sys.argv.pop(0)
    for arg in sys.argv:
        if arg.find('=') != -1:
            (k, v) = arg.split('=', 1)
            kwargs[k] = v
        else:
            args.append(arg)
    if cli(cmd, *args, **kwargs):
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
    sys.argv.pop(0)
    main()
        
