'''
Created on 2012-5-3

@author: wanqxu
'''
import unittest
from MySQLdb_Encryption import encryption_lib

encryption_lib.BPS_CONFIG = {
    'key':'a'*16,
    'rounds':10,
    'chars':['0','1'],
    'tweak':9223372036855207028
}

class TestBPS(unittest.TestCase):
    
    def setUp(self):
        self.bps = encryption_lib.BPS()
        self.bps._achieve_config()
    
    def test_achieve_config(self):
        self.assertEqual(self.bps.key, 'a'*16)
        self.assertEqual(self.bps.rounds, 10)
        self.assertEqual(self.bps.chars, ['0','1'])
        self.assertEqual(self.bps.tweak, 9223372036855207028)
    
    def test_get_s(self):
        assert self.bps._get_s() == 2
    
    def test_get_s_integer(self):
        assert self.bps._get_s_integer('01101010101') == [0,1,1,0,1,0,1,0,1,0,1]
    
    def test_return_to_string(self):
        assert self.bps._return_to_string([0,1,1,0,1,0,1,0,1,0,1]) == '01101010101'
    
    def test_subduction(self):
        assert self.bps._subduction(1, 2, 4) == 3
        assert self.bps._subduction(3, 1, 4) == 2
    
    def test_encrypt(self):
        plaintext = '011010010101'
        ciphertext = self.bps.encrypt(plaintext)
        assert len(ciphertext) == len(plaintext)
        for i in range(0,len(ciphertext)):
            assert ciphertext[i] in ['0','1']
        
    def test_decrypt(self):
        plaintext = '011010010101'
        ciphertext = self.bps.encrypt(plaintext)
        ret = self.bps.decrypt(ciphertext)
        assert ret == plaintext