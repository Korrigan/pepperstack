"""
Module for interacting with pepperstack commands

Provide few utilities functions and a dictionary containing all
commands

"""

from .host import host_list
from .host import host_show

from .role import role_list
from .role import role_show

from .help import help_command


__commands__ = {
    'help': help_command(),
    'host': {
        'list': host_list(),
        'show': host_show(),
        },
    'role': {
        'list': role_list(),
        'show': role_show(),
        },
    }


def get_command_dict():
    """
    Returns __commands__ dict

    """
    return __commands__


def get_command(cmd):
    """
    Returns the associated command instance

    """
    c = get_command_dict()
    for sub in cmd.split('.'):
        if not c.has_key(sub):
            print "No such command '{0}'".format(cmd)
            return None
        c = c[sub]
    if not callable(c):
        print "Command '{0}' is not a valid command".format(cmd)
        return None
    return c

