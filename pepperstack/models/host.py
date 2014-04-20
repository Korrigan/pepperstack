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
    mappings = {
        '_id': 'id',
        }


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


    @property
    def name(self):
        return self.info['name']

    @property
    def id(self):
        return str(self.info['_id'])

    @property
    def roles(self):
        return [
            r['name'] for r in self.info.get('roles', [])
            if r.has_key('name')
            ]


    def __init__(self, info):
        """
        Simple constructor to construct a Host object
        
        """
        self.info = info


    def as_dict(self):
        """
        Return self as a cleaned dict ready to print

        """
        d = self.info.copy()
        for k, v in d.items():
            new_k = k
            if self.mappings.has_key(k):
                new_k = self.mappings[k]
                d[new_k] = d.pop(k)
            if hasattr(self, new_k):
                d[new_k] = getattr(self, new_k)
        return d


    def update(self):
        """
        Updates the mongo database from data contained in this object

        """
        collection = db.get_connection()[cls.MONGO_COLLECTION]
        collection.update({'_id': self.id}, self.info)


    def add_role(self, role_name, update=True):
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
            self.generate_credential(c, update=False)
        if update:
            self.update()


    def generate_credentials(self, credential=None, update=True):
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
        if update:
            self.update()
