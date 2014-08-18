"""
This module contains all hosts related pepperstack commands

"""

from pepperstack.models import Host
from pepperstack.utils.format import title, indent, pretty_print
from pepperstack.utils.exceptions import DoesNotExistsException

from .mixins import CommandMixin


class host_list(CommandMixin):
    """
    List all hosts matching filters

    """
    description = "Prints all hosts names matching filters"

    def __call__(self, **filters):
        if self.cli_mode:
            print(title("Hosts:"))
        hosts = [h.name for h in Host.filter(**filters)]
        if self.cli_mode:
            for h in hosts:
                print(" - {0}".format(h))
        return hosts


class host_show(CommandMixin):
    """
    Print one host information fromm it's name

    """
    description = "Print detailed info for host <name>"

    def __call__(self, name):
        h = Host.find(name)
        if not h:
            raise DoesNotExistsException("Host {0} does not exists in database"
                                         .format(name))
        ret = h.as_dict()
        if self.cli_mode:
            print(title(h.name + ':'))
            pretty_print(ret)
        return ret


class host_create(CommandMixin):
    """
    Create an host with name <name>

    """
    description = "Create an host with name <name>"

    def __call__(self, name, **data):
        h = Host.create(name, data)
        if not h:
            raise DoesNotExistsException("Cannot create host {0}"
                                         .format(name))
        returner = host_show(cli_mode=self.cli_mode)
        return returner(name)


class host_delete(CommandMixin):
    """
    Delete host <name>

    """
    description = "Delete host <name>"

    def __call__(self, name):
        h = Host.find(name)
        if not h:
            raise DoesNotExistsException("Host {0} does not exists in database"
                                         .format(name))
        h.delete()
        if self.cli_mode:
            print("Host {0} deleted".format(name))


class host_add(CommandMixin):
    """
    Add an attribute to host by calling is method 'add'

    """

    def __call__(self, name, key, *args, **kwargs):
        h = Host.find(name)
        if not h:
            raise DoesNotExistsException("Host {0} does not exists in database"
                                         .format(name))
        h.add(key, *args, **kwargs)
        if self.cli_mode:
            print("Host {0} updated at {1}".format(name, key))


class host_remove(CommandMixin):
    """
    Remove an attribute from host by calling is method 'remove'

    """

    def __call__(self, name, key):
        h = Host.find(name)
        if not h:
            raise DoesNotExistsException("Host {0} does not exists in database"
                                         .format(name))
        h.remove(key)
        if self.cli_mode:
            print("Host {0} updated (removed {1})".format(name, key))


class host_get(CommandMixin):
    """
    Get an attribute from host by calling is method 'get'

    """

    def __call__(self, name, key, default=None):
        h = Host.find(name)
        if not h:
            raise DoesNotExistsException("Host {0} does not exists in database"
                                         .format(name))
        ret = h.get(key, default)
        if self.cli_mode:
            print(title(h.name + ':'))
            print("{0}: {1}".format(key, ret))
        return ret
