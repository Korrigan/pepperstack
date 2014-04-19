"""
Interface to the host collection

"""

from pepperstack.utils import db
from pepperstack.utils import cred

from .role import Role


class Host:
    """
    Represents an host

    """
    MONGO_COLLECTION = 'hosts'

    def __init__(self, info):
        """
        Simple constructor to construct a Host object since mongo is
        schema-free

        """
        self.info = info


    @property
    def id(self):
        return self.info['_id']


    @classmethod
    def find(cls, name):
        """
        Find host info and return a class instance
        
        """
        collection = db.get_connection()[cls.MONGO_COLLECTION]
        data = collection.find_one({'name': name})
        if data:
            return cls(data)
        else:
            return None


    @classmethod
    def find_all(cls):
        """
        Return a list of Host objects
        
        """
        hosts = []
        collection = db.get_connection()[cls.MONGO_COLLECTION]
        for h in collection.find():
            hosts.append(cls(h))
        return hosts


    def add_role(self, role_name):
        """
        Adds a role to a host
        
        """
        r = role.find(role_name)
        if not r:
            return
        role_data = {
            'id': r.id,
            'name': r.name,
            }
        if not self.info.has_key('roles'):
            self.info['roles'] = [role_data]
        else:
            self.info['roles'].append(role_data)
        for c in getattr(r, 'credentials', []):
            self.generate_credential(c)


    def generate_credentials(self, credential=None):
        """
        Regenerate credentials `credential` for `host`.
        If `credential` is None, regenerate all hosts credentials.
        If `credential` does not exists, it is created

        Please note that old credential will not be recoverable.
        
        """
        if credential:
            self.info['credentials'][credential] = cred.random_password()
        else:
            for c,v in self.info.get('credentials', {}).items():
                self.info['credentials'][c] = cred.random_password()
