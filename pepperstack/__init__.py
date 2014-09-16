"""
Pepperstack entry points

"""
from .commands import get_command


def pepper(cmd, *args, **kwargs):
    """
    Main interface for pepperstack

    """
    c = get_command(cmd, False)
    return c(*args, **kwargs)

def cli(cmd, *args, **kwargs):
    """
    Entry point for CLI

    """
    c = get_command(cmd, True)
    return c(*args, **kwargs)
