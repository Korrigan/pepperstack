"""
This module contains all role related commands for pepperstsack CLI

"""

from pepperstack.models import Role

from pepperstack.cli.format import title, indent, pretty_print


class role_list:
    """
    List all roles

    """
    description = "Prints all roles names matching filters"
    help_text = ""

    def __call__(self, **filters):
        print title("Roles:")
        for r in Role.filter(**filters):
            print " - {0}".format(r.name)
        return True


class role_show:
    """
    Print one host information fromm it's name

    """
    description = "Print detailed info for role <name>"
    help_text = ""

    def __call__(self, name):
        r = Role.find(name)
        if not r:
            return False
        print title(r.name + ':')
        pretty_print(r.as_dict())
        return True
