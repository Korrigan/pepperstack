"""
Interface for the role collection

"""

from .mixins import ModelMixin


class Role(ModelMixin):
    """
    Represents a role mongo document

    """
    MONGO_COLLECTION = 'roles'
    defaults = {
        'inherits': [],
        'credentials': [],
        }
    

    @property
    def name(self):
        return self.info['name']


    @property
    def inherits(self):
        return [
            r['name'] for f in self.info.get('inherits', [])
            if 'name' in r
            ]


    def add_parent(self, role_name, update=True):
        """
        Adds a role to inheritance list

        The `update` argument defines if the mongo collection shoud be updated

        """
        r = role.find(role_name)
        if not r:
            return False
        role_data = {
            'id': r.id,
            'name': r.name,
            }
        if 'inherits' not in self.info:
            self.info['inherits'] = [role_data]
        else:
            self.info['inherits'].append(role_data)
        if update:
            self.update()
        return True


    def del_parent(self, role_name, update=True):
        """
        Deletes a role from inheritance list

        The `update` argument defines if the mongo collection shoud be updated

        """
        inherits = []
        deleted = False
        if 'inherits' in self.info:
            for r in self.info['inherits']:
                if r.get('name', None) == role_name:
                    deleted = True
                else:
                    inherits.append(r)
            self.info['inherits'] = inherits
        if update:
            self.update()
        return deleted
