"""
This module contains help commands for pepperstack

"""

from pepperstack.cli.format import title


def _build_cmd_list_r(obj, base_key):
    """
    Recursively build a list of keys and command description

    """
    if isinstance(obj, dict):
        cmds = []
        for k, v in obj.items():
            cmds += _build_cmd_list_r(v, '{0}.{1}'.format(base_key, k))
        return cmds
    elif callable(obj):
        return [(base_key, obj.description)]


def command_list_help(in_help_text=True):
    """
    Returns a string describing each command and his short help

    """
    from . import get_command_dict

    if in_help_text:
        help_text = "available commands:"
    else:
        help_text = title("Available commands:") + '\n'
    for k, v in get_command_dict().items():
        for c, d in _build_cmd_list_r(v, k):
            help_text += '  {0: <12}{1}\n'.format(c, d)
        help_text += '\n'
    return help_text


class help_command:
    """
    Returns the detailed help for command `cmd`

    """
    description = "Returns detailed help for <command>"
    help_text = ("'{command}' takes an argument <command> and displays the extended help "
                 "about <command>.\n\n"

                 "'{command} {command}' displays this help text.\n\n"

                 "'{command}' with no parameters displays the command list and short help")

    def __call__(self, cmd=None):
        from . import get_command

        if not cmd:
            print command_list_help(in_help_text=False)
        else:
            c = get_command(cmd)
            if not c:
                return False
            t = "Command '{0}' help:".format(cmd)
            print title(t)
            print c.help_text.format(command=cmd)
        return True
