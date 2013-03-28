'''_subduction
Created on 2012-5-3

@author: wanqxu
'''
import unittest
import random
from MySQLdb_Encryption.cipher import BPS_BC

class TestBPS(unittest.TestCase):
    
    def setUp(self):
        self.key = 'a'*16
        self.bc = BPS_BC(10,self.key,16,9223372036855207028)
    
    def test_encode_long(self):
        assert self.bc._encode_long(257) == '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01'
    
    def test_addition(self):
        assert self.bc._addition(11, 22, 24) == 9
    
    def test_subduction(self):
        assert self.bc._subduction(9, 11, 24) == 22
        assert self.bc._subduction(9, 7, 24) == 2
        
    def test_psuedo_random_func(self):
        assert self.bc.psuedo_random_func(random.randint(0, 256)) < 1<<96
    
    def test_bc(self):
        X = [1,6,2,1,4,5,2,8]
        Y = self.bc.encryption(X)
        assert self.bc.decryption(Y) == X
    
    
    
    
    
    
    
    
    
    