''' Tests encryption functions. '''

import unittest
import os
from MySQLdb_Encryption import encryption_lib

encryption_lib.PREFIX_CONFIG = {
    'size':10,
    'key':'a'*16,
    'tweak':5,
}

def get_table():
    return ['2','1','0','3']

class TestPrefix(unittest.TestCase):
    
    def setUp(self):
        self.prefix = encryption_lib.Prefix()
    
    def test_achieve_config(self):
        self.prefix._achieve_config()
        self.assertEqual(self.prefix.key, 'a'*16)
        self.assertEqual(self.prefix.size, 10)
        self.assertEqual(self.prefix.tweak, 5)
    
    def test_get_table(self):
        encryption_lib.PREFIX_CONFIG = {
            'size':1,
            'key':'a'*16,
            'tweak':5,
        }
        self.prefix._achieve_config()
        table = self.prefix._get_table()
        os.remove('1n61616161616161616161616161616161')
        self.assertEqual(table,['0'])
    
    def test_encrypt(self):
        self.prefix._get_table=get_table
        self.assertEqual(self.prefix.encrypt(0),2)
        
    def test_decrypt(self):
        self.prefix._get_table=get_table
        self.assertEqual(self.prefix.decrypt(2),0)
    
    
    
    