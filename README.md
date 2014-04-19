Pepperstack
===========

Pepperstack aims to be an inventory tool for physical or virtual hosts.

It stores network information, can generate unique credentials, etc...

The goal to this tool is to provide a great pillar source for salt and to be
easily managable with a web interface (which will certainly be a Django app).


Usage
=====

At this time, pepperstack only provides a command line interface.



Salt integration
================

Pepperstack provides a module to generate pillars from mongo inventory.


Mongo connection parameters
---------------------------

You need to provide Mongo connection parameters the same way they are stated in
salt docs for [salt.returners.mongo_return](http://docs.saltstack.com/en/latest/ref/returners/all/salt.returners.mongo_return.html#module-salt.returners.mongo_return)


External pillar activation
--------------------------

You first need to tell salt the location of pepperstack salt_ext_modules in the
"extensions_modules" master variable.


Then, activate the pepperstack external pillar source by adding an entry in the
"ext_pillar" master variable.

You may want to specify a host collection (in host_collection kwarg, default to
`hosts`) and a role collection (in role_collection kwarg, defaults to `roles`).


*Full configuration Example*:

```
 mongo.db: pepperstack
 mongo.host: 127.0.0.1

 extensions_modules: /path/to/pepperstack/salt_ext_modules

 ext_pillar:
   - pepperstack:
       role_connection: my_roles_collection
       host_collection: my_host_collection
```

*Note*: If you need to supply other extensions modules to salt, just create
symlinks to pepperstack ones in your other extensions modules path.



LICENSE
=======

This project is licensed under MIT License.

Please see the `LICENCE` file for more informations.
