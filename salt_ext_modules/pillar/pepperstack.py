"""
External pillar module to fetch hosts roles information fron Mongodb
Developped for Quanta internal uses


"""

import logging

try:
    import pymongo
    HAS_PYMONGO = True
except ImportError:
    HAS_PYMONGO = False


__opts__ = {
    'mongo.db': 'salt',
    'mongo.host': 'salt',
    'mongo.password': '',
    'mongo.port': 27017,
    'mongo.user': '',
    }


def __virtual__():
    if not HAS_PYMONGO:
        return False
    return __name__.split('.')[-1]


logger = logging.getLogger(__name__)


def _merge_dict(*args):
    '''
    Recursively performs a non destructive merge of 2 or more dictionaries.

    If a key exists in 2 or more dict and both are dict, this function is
    called recursiveley on thoses 2 dicts.

    If a key exists in 2 or more dict and both are list, thoses lists are
    merged under this key.
    
    '''
    res = {}
    for d in args:
        for k, v in d.iteritems():
            if not res.has_key(k):
                res[k] = v
            elif isinstance(res[k], dict) and isinstance(v, dict):
                res[k] = _merge_dict(res[k], v)
            elif isinstance(res[k], list) and isinstance(v, list):
                res[k] += v
    return res


def _map_roles(roles):
    '''
    Mapping function for roles
    Transforms roles dict list into a list of names and nest it
    under roles:local

    '''
    return {
        'roles': {
            'local': [r['name'] for r in roles]
            }
        }


def _map_id(_id):
    '''
    Mapping function for _id
    Renames _id to pepperstack_id and str() it

    '''
    return {
        'pepperstack_id': str(_id)
        }


def _map_name(name):
    '''
    Mapping function for name
    Returns an empty dict since `name` is actually the dict key on
    returned pillar.

    '''
    return {}


_default_attr_mappings = {
    '_id': _map_id,
    'roles': _map_roles,
    'name': _map_name,
    }


def _map_attribute(attr, value, mappings=_default_attr_mappings):
    '''
    Returns a dict containing only a key and an associated value
    This method goal is to easily rename attributes or modify their values

    If `attr` does not match a key in `mappings` dict, the dict {`attr`: `value`}
    is returned, else:
      - If `mappings[attr]` is a callable, `mappings[attr](value)` is returned
      - Else, the dictionary {`mappings[attr]`: `value`} is returned

    '''
    if not mappings.has_key(attr):
        return {attr: value}
    elif callable(mappings[attr]):
        return mappings[attr](value)
    else:
        return {mappings[attr]: value}


def _map_dict(d, mappings=_default_attr_mappings):
    '''
    Use _map_attribute on every element of a copy `d`
    Returns this altered copy
    
    '''
    mapped = d.copy()
    for k, v in mapped.items():
        del mapped[k]
        mapped.update(_map_attribute(k, v, mappings))
    return mapped


def _get_roles_pillar(host_collection, role_collection):
    '''
    Retrieves all hosts and their roles from mongodb and reorganize them
    in a dict of hosts lists

    '''
    role_key_fmt = '{0}_servers'
    roles = {r['name']:r for r in role_collection.find()}
    roles_mapping = {name:[] for name,r in roles.items()}
    roles_pillar = {
        'available': [name for name,r in roles.items()]
        }

    def _get_inherited_roles(name, role_list):
        '''
        Returns a list of roles in which an host begins if he has `role`
        Uses a dynamic algorithm for faster resolution
        
        '''
        if not role_list.has_key(name):
            return []
        if roles_mapping[name]:
            return roles_mapping[names]
        role = role_list[name]
        del role_list[name]
        inherited = [name]
        for r in role.get('inherits', []):
            inherithed.append(_get_inherited_roles(r['name'], role_list))
        roles_mapping[name] = inherited
        return inherited

    for h in host_collection.find(fields=['name', 'roles']):
        for r in h.get('roles', []):
            for inh_r in _get_inherited_roles(r['name'], roles):
                k = role_key_fmt.format(inh_r)
                if not roles_pillar.has_key(k):
                    roles_pillar[k] = []
                roles_pillar[k].append(h['name'])
    return {'roles': roles_pillar}


def _get_hosts_pillar(host_collection):
    '''
    Returns an host dictionary containing all hosts and the followinf infos:
      - IP addresses in `ip_address`
      - Internal ID in `pepperstack_id`

    '''
    return {
        'hosts': {
            h['name']:_map_dict(h) for h in host_collection.find(
                fields={
                    '_id': True,
                    'name': True,
                    'ip_address': True
                    })
            }
        }


def _get_minion_pillar(minion_id, host_collection):
    '''
    Return all minion informations after mappings attributes

    '''
    return _map_dict(host_collection.find_one({'name': minion_id}))


def ext_pillar(minion_id, pillar, host_collection='hosts', role_collection='roles'):
    '''
    Return external pillars from mongodb collection
    
    '''
    host = __opts__['mongo.host']
    port = __opts__['mongo.port']
    db_name = __opts__['mongo.db']
    user = __opts__['mongo.user']
    password = __opts__['mongo.password']

    logger.info('connecting to mongo on {0}:{1}'.format(host, port))
    conn = pymongo.MongoClient(host, port)
    logger.debug('using database "{0}"'.format(db_name))
    db = conn[db_name]
    if user and password:
        logger.debug('authenticating as "{0}"'.format(user))
        db.authenticate(user, password)

    logger.info('fetching pillar infos for {0} in mongo'.format(minion_id))
    return _merge_dict(_get_roles_pillar(db[host_collection], db[role_collection]),
                       _get_hosts_pillar(db[host_collection]),
                       _get_minion_pillar(minion_id, db[host_collection]))
