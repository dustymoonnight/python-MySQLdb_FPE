'''
Created on 2012-3-17

@author: wanqxu
'''
import unittest
import os
from MySQLdb_Encryption.cipher import AESTable

class TestAESTable(unittest.TestCase):
    
    def setUp(self):
        self.key = 'a'*16
        self.aes_table = AESTable(10,self.key)
    
    def tearDown(self):
        pass
    
    def test_aes_encrypt(self):
        self.assertEqual(self.aes_table._aes_encrypt(1).plaintext, '1')
        self.assertEqual(self.aes_table._aes_encrypt(1).ciphertext, '\x9b')
    
    def test_construct_permutation_table(self):
        self.assertEqual(len(self.aes_table._permutation_table), 0)
        self.aes_table._construct_permutation_table()
        self.assertEqual(len(self.aes_table._permutation_table), 10)
    
    def test_construct_table(self):
        self.assertEqual(len(self.aes_table.table), 0)
        self.aes_table.construct_table()
        self.assertEqual(len(self.aes_table.table), 10)
    
    def test_get_file_name(self):
        self.assertEqual(self.aes_table._get_file_name(), '10n61616161616161616161616161616161')
    
    def test_store_table(self):
        self.assertEqual(self.aes_table._has_table_in_file(), False)
        self.aes_table.store_table()
        self.assertEqual(self.aes_table._has_table_in_file(), True)
        os.remove(self.aes_table._get_file_name())
        
    def test_get_table(self):
        self.aes_table.construct_table()
        self.assertNotEqual(self.aes_table.get_table(), None)
        self.aes_table.store_table()
        aes_table2 = AESTable(10,self.key)
        self.assertNotEqual(aes_table2.get_table(), None)
        os.remove(aes_table2._get_file_name())
    
    def test_tweak(self):
        self.aes_table.construct_table()
        self.assertNotEqual(self.aes_table.tweak(1),self.aes_table.table)
        
        
