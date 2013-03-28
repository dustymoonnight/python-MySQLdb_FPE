'''
Created on 2012-4-11

@author: wanqxu
'''
import unittest
from MySQLdb_Encryption import encryption_lib

encryption_lib.FFX_CONFIG = {
    'key':'a'*16,
    'rounds':10,
    'chars':['0','1']
}

class TestFFX(unittest.TestCase):
    
    def setUp(self):
        self.ffx = encryption_lib.FFX()
    
    def test_achieve_config(self):
        self.ffx._achieve_config()
        self.assertEqual(self.ffx.key, 'a'*16)
        self.assertEqual(self.ffx.rounds, 10)
        self.assertEqual(self.ffx.chars, ['0','1'])
    
    def test_encrypt(self):
        plaintext = '011010010101'
        ciphertext = self.ffx.encrypt(plaintext)
        assert len(ciphertext) == len(plaintext)
        for i in range(0,len(ciphertext)):
            assert ciphertext[i] in ['0','1']
        
    def test_decrypt(self):
        plaintext = '011010010101'
        ciphertext = self.ffx.encrypt(plaintext)
        ret = self.ffx.decrypt(ciphertext)
        assert ret == plaintext
        