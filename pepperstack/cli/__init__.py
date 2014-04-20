"""
Command line interface module to pepperstack

"""

from .commands import get_command

from .commands.help import command_list_help


def cli(cmd, *args, **kwargs):
    """
    Main interface for the command line interface

    """
    c = get_command(cmd)
    return c(*args, **kwargs)

