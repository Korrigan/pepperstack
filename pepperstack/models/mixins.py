"""
Module containing mixins for models class

"""

from pepperstack.utils.exceptions import DoesNotExistsException, DuplicateException


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
        if cls.find(value, attr=attr):
            raise DuplicateException("{0} already exists in database"
                                     .format(value))
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
        if '_id' not in self.info:
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
        for k, v in list(d.items()):
            new_k = k
            if k in mappings:
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
        collection.update({'_id': self.info['_id']}, self.info)



    def delete(self):
        """
        Deletes the current document in mongo collection

        """
        collection = self.get_collection()
        collection.remove({'_id': self.info['_id']})
        del self.info['_id']

    def _key_apply(self, key_path, f, create_subkeys=False):
        """
        Finds the dict at the end of key_path in self.info and apply f to it
        the following way):
          f(dict, key)
        with:
        - dict: the recursively found dict
        - key: the key to apply in this dict

        If create_subkeys is True, sub-dictionaries will be created if missing

        If key_path is a top-level key for self.info. self.get_attr_mappings()
        will be used

        """
        mappings = self.get_attr_mappings()
        subkeys = key_path.split('.')
        if '.' not in key_path and key_path in mappings:
            key = mappings[key_path]
        else:
            key = subkeys[-1]
        attr = self.info
        print("Debug: sub = {0}, key = {1}".format(subkeys[:-1], key))
        for sub in subkeys[:-1]:
            print("Debut: cur = {0}".format(sub))
            if not sub in attr:
                if create_subkeys:
                    attr[sub] = {}
                    attr = attr[sub]
                else:
                    raise KeyError("Cannot found {0} in object".format(key_path))
            elif isinstance(attr[sub], dict):
                attr = attr[sub]
            else:
                raise KeyError("Cannot found {0} in object".format(key_path))
        return f(attr, key)


    def add(self, key_path, *args, **kwargs):
        """
        Add data to self.info at the following key_path
        Sub-dictionaries will be created if needed

        If the attribute at key_path is a list, args are appened to it
        If it's a scalar type, it is transformed into a list and args are appened
        If it's a dict, it will be updated with kwargs
        
        If this attribute does not exists, it will be created as the following:
        - If args is present and len(args) is 1, it will be filled with args[0]
        - Else if args is present, it will be filled with args
        - Else if kwargs is present, it will be a copy of it
        - Else an exception is raised

        """
        def _add(attr, key):
            err = ValueError("Noting to add at {0}".format(key_path))
            if not key in attr:
                if len(args) == 1:
                    attr[key] = args[0]
                elif len(args) > 1:
                    attr[key] = list(args)
                elif len(kwargs):
                    attr[key] = kwargs.copy()
                else:
                    raise err
            else:
                if isinstance(attr[key], list):
                    if not len(args):
                        raise err
                    attr[key].append(args)
                elif isinstance(attr[key], dict):
                    if not len(kwargs):
                        raise err
                    attr[key].update(kwargs)
                else:
                    if not len(args):
                        raise err
                    attr[key] = [attr[key]]
                    attr[key].append(*args)

        self._key_apply(key_path, _add, True)
        self.update()


    def remove(self, key_path):
        """
        Remove a dict from self.info at key_path and all its contents

        """
        def _remove(attr, key):
            if key in attr:
                return attr.pop(key)
            else:
                raise KeyError("Cannot found {0} in object".format(key_path))

        ret = self._key_apply(key_path, _remove, False)
        self.update()
        return ret


    def get(self, key_path, default=None):
        """
        Returns a copy of the data in self.info at key_path
        If default is not None and the attribute is not found, default is
        returned; else an exception is raised

        """
        def _get(attr, key):
            if key in attr:
                ret = attr[key]
                if isinstance(ret, list):
                    return list(ret)
                elif isintance(ret, dict):
                    return ret.copy()
                else:
                    return ret
            else:
                raise KeyError("Cannot found {0} in object".format(key_path))

        try:
            ret = self._key_apply(key_path, _get)
        except KeyError as e:
            if default is not None:
                return default
            else:
                raise e
        else:
            return ret
