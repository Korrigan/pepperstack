"""
Interface to the host collection

"""

from pepperstack.utils import cred

from .mixins import ModelMixin
from .role import Role


class Host(ModelMixin):
    """
    Represents an host mongo document

    """
    MONGO_COLLECTION = 'hosts'
    defaults = {
        'roles': [],
        'credentials': [],
        }


    @property
    def name(self):
        return self.info['name']


    @property
    def roles(self):
        return [
            r['name'] for r in self.info.get('roles', [])
            if r.has_key('name')
            ]


    def add_role(self, role_name, update=True):
        """
        Adds a role to host

        The `update` argument defines if the mongo collection shoud be updated
        
        """
        r = role.find(role_name)
        if not r:
            return False
        role_data = {
            'id': r.id,
            'name': r.name,
            }
        if not self.info.has_key('roles'):
            self.info['roles'] = [role_data]
        else:
            self.info['roles'].append(role_data)
        for c in getattr(r, 'credentials', []):
            self.generate_credential(c, update=False)
        if update:
            self.update()
        return True


    def del_role(self, role_name, update=True):
        """
        Deletes a role named `role_name` from host.
        Returns True if role has been deleted, False else.

        The `update` argument defines if the mongo collection shoud be updated

        """
        roles = []
        deleted = False
        if self.info.has_key('roles'):
            for r in self.info['roles']:
                if r.get('name', None) == role_name:
                    deleted = True
                else:
                    roles.append(r)
            self.info['roles'] = roles
        if update:
            self.update()
        return deleted


    def generate_credentials(self, credential=None, update=True):
        """
        Regenerate credentials `credential` for this host
        If `credential` is None, regenerate all this host's credentials.
        If `credential` does not exists, it is created

        Please note that old credential will not be recoverable.

        The `update` argument defines if the mongo collection shoud be updated
        
        """
        if credential:
            self.info['credentials'][credential] = cred.random_password()
        else:
            for c,v in self.info.get('credentials', {}).items():
                self.info['credentials'][c] = cred.random_password()
        if update:
            self.update()


    def del_credential(self, credential, update=True):
        """
        Delete a credential named `credential` for this host.
        Returns True if the credential has been deleted, False else.

        The `update` argument defines if the mongo collection shoud be updated
        
        """
        c =  self.info.get('credentials', {})
        if c.has_key(credential):
            del self.info['credentials'][credential]
            return True
        return False
