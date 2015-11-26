# -*- coding: utf-8 -*-
import re
import os
import sys
import os.path
import string
import logging
import atexit

from pdb import set_trace

import bsddb3.db
from bsddb3.db import DBEnv, DB


def import_constants(module, pattern=None, types=(int, long, basestring)):
    """
    Import constants from a python module into the global namespace,
    should only be used at module level :)

    Example::

        import bsddb
        import_constants(bsddb, '^DB_')
        print DB_VERSION_MAJOR

    """

    for name in dir(module):
        if pattern and not re.search(pattern, name):
            continue

        value = getattr(module, name)
        if types and not isinstance(value, types):
            continue

        globals()[name] = value

import_constants(bsddb3.db, '^DB_')

HOME = './data'
flags = (DB_CREATE | DB_INIT_LOCK | DB_INIT_MPOOL | DB_INIT_LOG |
         DB_INIT_TXN | DB_THREAD)

env = DBEnv()
env.set_cachesize(0, 32 * 1024 * 1024, 0)
env.open(HOME, flags)

db = DB(env)
db.set_flags(DB_DUP | DB_DUPSORT)
db.open('main', dbname='records',
        flags=DB_CREATE | DB_AUTO_COMMIT | DB_MULTIVERSION, dbtype=DB_BTREE)


def finish():
    db.close()
    env.close()
atexit.register(finish)


def popuplate():
    txn = env.txn_begin(flags=0)
    for l in string.letters:
        for i in range(25):
            db.put(l, '%03d' % i, txn=txn)
    txn.commit()

if __name__ == '__main__':
    popuplate()
