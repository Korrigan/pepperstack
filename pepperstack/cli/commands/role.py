"""
This module contains all role related commands for pepperstsack CLI

"""

from pepperstack.models import Role
from pepperstack.utils.exceptions import DoesNotExistsException
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


class role_show:
    """
    Print one host information fromm it's name

    """
    description = "Print detailed info for role <name>"
    help_text = ""

    def __call__(self, name):
        r = Role.find(name)
        if not r:
            raise DoesNotExistsException("Role {0} does not exists in database"
                                         .format(name))
        print title(r.name + ':')
        pretty_print(r.as_dict())


class role_create:
    """
    Create a role

    """
    description = "Create role <name>"
    help_text = ""

    def __call__(self, name, **data):
        r = Role.create(name, data)
        if not r:
            raise DoesNotExistsException("Cannot create role {0}"
                                         .format(name))
        role_show()(name)


class role_delete:
    """
    Delete a role

    """
    description = "Delete role <name>"
    help_text = ""

    def __call__(self, name):
        r = Role.find(name)
        if not r:
            raise DoesNotExistsException("Role {0} does not exists in database"
                                         .format(name))
        r.delete()
        print "Role {0} deleted".format(name)
