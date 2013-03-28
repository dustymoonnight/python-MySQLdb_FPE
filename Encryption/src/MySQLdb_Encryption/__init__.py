# Copyright (C) 2012 Xu Wanqing (Vane)
#
# This module is part of MySQLdb_Encryption for python.

''' Encrypt sql values for MySQLdb module '''

__version__ = '1.0'

# Setup namespace
from engine import Encrypt
from filters import ParseSQL
from encryption import Encryption
from setting import ENCRYPT_KEY_WORD

def encrypt(sql):
    e = Encrypt(ParseSQL(sql),ENCRYPT_KEY_WORD,Encryption)
    return e.get_prased_sql()