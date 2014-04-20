"""
This module contains all hosts related pepperstack commands

"""

from pepperstack.models import Host

from pepperstack.cli.format import title, indent, pretty_print

class host_list:
    """
    List all hosts without credential information

    """
    description = "Prints all hosts names"
    help_text = ""

    def __call__(*args, **kwargs):
        print "Hosts:"
        for h in Host.find_all():
            print "  - {0}".format(h.name)
        return True


class host_show:
    """
    Print one host information fromm it's name

    """
    description = "Print detailed info for host <name>"
    help_text = ""

    def __call__(self, name):
        import yaml

        h = Host.find(name)
        if not h:
            return False
        print title(h.name + ':')
        pretty_print(h.as_dict())
#        print yaml.safe_dump(h.as_dict(),
#                             indent=4,
#                             default_flow_style=False,
#                             canonical=False,
#                             tags=False)
        return True
