"""
This module contains all role related commands for pepperstsack CLI

"""

from pepperstack.models import Role
from pepperstack.utils.format import title, indent, pretty_print
from pepperstack.utils.exceptions import DoesNotExistsException

from .mixins import CommandMixin


class role_list(CommandMixin):
    """
    List all roles

    """
    description = "Prints all roles names matching filters"

    def __call__(self, **filters):
        if self.cli_mode:
            print(title("Roles:"))
        roles = [r.name for r in Role.filter(**filters)]
        if self.cli_mode:
            for r in roles:
                print(" - {0}".format(r))
        return roles


class role_show(CommandMixin):
    """
    Print one host information fromm it's name

    """
    description = "Print detailed info for role <name>"

    def __call__(self, name):
        r = Role.find(name)
        if not r:
            raise DoesNotExistsException("Role {0} does not exists in database"
                                         .format(name))
        ret = r.as_dict()
        if self.cli_mode:
            print(title(r.name + ':'))
            pretty_print(ret)
        return ret


class role_create(CommandMixin):
    """
    Create a role

    """
    description = "Create role <name>"

    def __call__(self, name, **data):
        r = Role.create(name, data)
        if not r:
            raise DoesNotExistsException("Cannot create role {0}"
                                         .format(name))
        returner = role_show(cli_mode=self.cli_mode)
        return returner(name)


class role_delete(CommandMixin):
    """
    Delete a role

    """
    description = "Delete role <name>"

    def __call__(self, name):
        r = Role.find(name)
        if not r:
            raise DoesNotExistsException("Role {0} does not exists in database"
                                         .format(name))
        r.delete()
        if self.cli_mode:
            print("Role {0} deleted".format(name))
