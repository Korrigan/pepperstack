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
    if not c:
        return False
    try:
        c(*args, **kwargs)
    except Exception as e:
        print("Error: {0}".format(e))
        return False
    else:
        return True
