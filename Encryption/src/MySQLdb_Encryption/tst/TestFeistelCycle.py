'''
Created on 2012-3-27

@author: wanqxu
'''
import unittest
import random
from MySQLdb_Encryption import encryption_lib

encryption_lib.FEISTELCYCLE_CONFIG = {
    'size':1<<230,
    'key':'a'*16,
}

class TestFeistelCycle(unittest.TestCase):
    
    def setUp(self):
        self.feistel_cycle = encryption_lib.FeistelCycle()
    
    def test_achieve_config(self):
        self.feistel_cycle._achieve_config()
        self.assertEqual(self.feistel_cycle.key, 'a'*16)
        self.assertEqual(self.feistel_cycle.size, 1<<230)
    
    def test_encrypt(self):
        plaintext = random.randint(0, (1<<230)-1)
        ciphertext = self.feistel_cycle.encrypt(plaintext)
        assert ciphertext < (1<<230)
        
    def test_decrypt(self):
        plaintext = random.randint(0, (1<<230)-1)
        ciphertext = self.feistel_cycle.encrypt(plaintext)
        self.assertEqual(self.feistel_cycle.decrypt(ciphertext),plaintext)
        
        
        