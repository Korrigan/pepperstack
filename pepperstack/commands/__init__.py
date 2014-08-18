"""
Module for interacting with pepperstack commands

Provide few utilities functions and a dictionary containing all
commands

"""
import collections

from .host import host_list
from .host import host_show
from .host import host_create
from .host import host_delete
from .host import host_add
from .host import host_remove
from .host import host_get

from .role import role_list
from .role import role_show
from .role import role_create
from .role import role_delete

from .help import help_command


__commands__ = {
    'help': help_command,
    'host': {
        'list': host_list,
        'show': host_show,
        'create': host_create,
        'delete': host_delete,
        'add': host_add,
        'remove': host_remove,
        'get': host_get,
        },
    'role': {
        'list': role_list,
        'show': role_show,
        'create': role_create,
        'delete': role_delete,
        },
    }


def get_command_dict():
    """
    Returns __commands__ dict

    """
    return __commands__.copy()


def get_command(cmd, cli_mode=False):
    """
    Returns the associated command instance

    """
    c = get_command_dict()
    for sub in cmd.split('.'):
        if sub not in c:
            raise CommandException("No such command '{0}'".format(cmd))
        c = c[sub]
    return c(cli_mode=cli_mode)
