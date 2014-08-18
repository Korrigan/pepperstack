"""
Module for interacting with pepperstack commands

Provide few utilities functions and a dictionary containing all
commands

"""
import collections

from .host import host_list
from .host import host_show

from .role import role_list
from .role import role_show
from .role import role_create
from .role import role_delete

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
        'create': role_create(),
        'delete': role_delete(),
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
        if sub not in c:
            print("No such command '{0}'".format(cmd))
            return None
        c = c[sub]
    if not isinstance(c, collections.Callable):
        print("Command '{0}' is not a valid command".format(cmd))
        return None
    return c

