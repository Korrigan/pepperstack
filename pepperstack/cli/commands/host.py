"""
This module contains all hosts related pepperstack commands

"""

from pepperstack.models import Host

from pepperstack.cli.format import title, indent, pretty_print


class host_list:
    """
    List all hosts matching filters

    """
    description = "Prints all hosts names matching filters"
    help_text = ""

    def __call__(self, **filters):
        print(title("Hosts:"))
        for h in Host.filter(**filters):
            print(" - {0}".format(h.name))
        return True


class host_show:
    """
    Print one host information fromm it's name

    """
    description = "Print detailed info for host <name>"
    help_text = ""

    def __call__(self, name):
        h = Host.find(name)
        if not h:
            return False
        print(title(h.name + ':'))
        pretty_print(h.as_dict())
        return True
