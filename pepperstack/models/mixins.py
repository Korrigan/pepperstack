"""
Module containing mixins for models class

"""

class ModelMixin(object):
    """
    A simple module providing few helper methods for mongo collections

    """

    @classmethod
    def get_collection(cls):
        """
        This classmethod returns a pymongo.Collection object matching
        cls.MONGO_COLLECTION

        You should either set MONGO_COLLECTION attribute or override this
        method in your child class

        """
        from pepperstack.utils import db
        return db.get_connection()[cls.MONGO_COLLECTION]


    @classmethod
    def get_defaults(cls):
        """
        Returns the defaults for the create classmethod if cls.defaults is
        defined (defaults to {})

        """
        if hasattr(cls, 'defaults'):
            return cls.defaults
        return {}


    @classmethod
    def find(cls, value, attr='name'):
        """
        Find a Mongo document matching {attr: value} and transforms it into
        a `cls` instance
        
        """
        collection = cls.get_collection()
        if not collection:
            return None
        data = collection.find_one({attr: value})
        if data:
            return cls(data)
        else:
            return None


    @classmethod
    def filter(cls, **kwargs):
        """
        Returns a list of all mongo documents in collection as a
        `cls` instances list

        """
        objs = []
        collection = cls.get_collection()
        for o in collection.find(kwargs):
            objs.append(cls(o))
        return objs


    @classmethod
    def create(cls, value, data={}, attr='name'):
        """
        Creates a mongo document with basic attribute `attr` set to `value`.
        This classmethod uses cls.get_defaults() updated with data to populate
        the mongo document.

        Finally, a `cls` instance is created and returned from the new mongo
        document.

        """
        collection = cls.get_collection()
        if not collection:
            return None
        info = cls.get_defaults()
        info.update(data)
        info[attr] = value
        info = collection.insert(info)
        return cls(info)


    @property
    def id(self):
        """
        Returns the object id from the standard _id row

        """
        if not self.info.has_key('_id'):
            return None
        return str(self.info['_id'])


    def __init__(self, info):
        """
        Simple constructor to construct an object from a mongo collection
        
        """
        self.info = info


    def __eq__(self, other):
        return self.id == other.id


    def get_attr_mappings(self):
        """
        Returns attributes name mappings dictionary from self.mappings if
        defined. By default returns just the _id attribute mapping.

        Ensure to define the _id mapping if you define self.mappings.

        """
        if hasattr(self, 'mappings'):
            return self.mappings
        return {'_id': 'id'}


    def as_dict(self):
        """
        This method returns the current object as a clean dictionary for
        printing or exploitation purposes.

        It returns self.info dict copy by replacing:
          - All keys present in self.get_attr_mappings() dict if it exists
            with their values
          - All values for which this object has an attribute with this
            attribute value

        This method shoud be used instead of self.info to guarantee attributes
        that must be cleared are in a good way.

        """
        mappings = self.get_attr_mappings()
        d = self.info.copy()
        for k, v in d.items():
            new_k = k
            if mappings.has_key(k):
                new_k = mappings[k]
                d[new_k] = d.pop(k)
            if hasattr(self, new_k):
                d[new_k] = getattr(self, new_k)
        return d


    def update(self):
        """
        Updates the mongo database from data contained in this object

        """
        collection = self.get_collection()
        collection.update({'_id': self.id}, self.info)


    def delete(self):
        """
        Deletes the current document in mongo collection

        """
        collection = self.get_collection()
        collection.remove({'_id': self.id})
        del self.info['_id']
