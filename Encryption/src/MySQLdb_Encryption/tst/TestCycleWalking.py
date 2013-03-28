'''
Created on 2012-3-20

@author: wanqxu
'''
import unittest
import random
from MySQLdb_Encryption import encryption_lib

encryption_lib.CYCLEWALKING_CONFIG = {
    'size':1<<120,
    'key':'a'*16,
}

class TestCycleWalking(unittest.TestCase):
    
    def setUp(self):
        self.feistel_cycle = encryption_lib.CycleWalking()
    
    def test_achieve_config(self):
        self.feistel_cycle._achieve_config()
        self.assertEqual(self.feistel_cycle.key, 'a'*16)
        self.assertEqual(self.feistel_cycle.size, 1<<120)
    
    def test_encode_long(self):
        self.assertEqual(self.feistel_cycle._encode_long(257), '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01')
    
    def test_encrypt(self):
        plaintext = random.randint(0, (1<<120)-1)
        ciphertext = self.feistel_cycle.encrypt(plaintext)
        assert ciphertext < (1<<120)
        
    def test_decrypt(self):
        plaintext = random.randint(0, (1<<120)-1)
        ciphertext = self.feistel_cycle.encrypt(plaintext)
        self.assertEqual(self.feistel_cycle.decrypt(ciphertext),plaintext)
    