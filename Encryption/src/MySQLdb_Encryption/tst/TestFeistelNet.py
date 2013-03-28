'''
Created on 2012-3-27

@author: wanqxu
'''
import unittest
import os
import random
from MySQLdb_Encryption.cipher import BalanceFeistelNet,ImbalanceFeistelNet

def mork_char_to_digit(value):
    return '11'

def mork_digit_to_char(value):
    return 'b'

class TestBalanceFeistelNet(unittest.TestCase):
    
    def setUp(self):
        self.key = 'a'*16
        self.feister_net = BalanceFeistelNet(1<<8,self.key,16)
    
    def test_psuedo_random_func(self):
        assert self.feister_net.psuedo_random_func(random.randint(0, 256)) < 16
    
    def test_round(self):
        ret = random.randint(0, 256)
        left = self.feister_net.round(ret, 16)
        assert self.feister_net.round(left, 16) == ret
    
    def test_feistel(self):
        plaintext = random.randint(0, 256)
        ciphertext = self.feister_net.feistel(plaintext) 
        de_plaintext = self.feister_net.re_feistel(ciphertext)
        assert de_plaintext == plaintext
        assert ciphertext <= 256

class TestImbalanceFeistelNet(unittest.TestCase):
    
    def setUp(self):
        self.key = 'a'*16
        self.chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.feister_net = ImbalanceFeistelNet(self.chars,self.key,16)
    
    def test_get_digit_len(self):
        assert self.feister_net._get_digit_len() == 2
    
    def test_char_to_digit_in_chars(self):
        assert self.feister_net._char_to_digit('a') == '00'
    
    def test_char_to_digit_not_in_chars(self):
        try:
            self.feister_net._char_to_digit('1')
        except Exception,e:
            self.assertEqual(str(e), 'Input error, the plaintext has some chars not in FFX configuration.')
    
    def test_str_to_digit(self):
        self.feister_net._char_to_digit = mork_char_to_digit
        assert self.feister_net.str_to_digit('abv') == '111111'
    
    def test_digit_to_char_in_chars(self):
        assert self.feister_net._digit_to_char('01') == 'b'
    
    def test_digit_to_str(self):
        self.feister_net._digit_to_char = mork_digit_to_char
        assert self.feister_net.digit_to_str('111111') == 'bbb'
    
    def test_fill_zero(self):
        assert self.feister_net._fill_zero('1') == '01'
        assert self.feister_net._fill_zero('11') == '11'
    
    def test_getwidth(self):
        assert self.feister_net._getwidth('value') == 2
        assert self.feister_net._getwidth('avalue') == 3
    
    def test_addition_single_char(self):
        assert self.feister_net._addition_single_char('1', '2') == '03'
        assert self.feister_net._addition_single_char('21', '12') == '07'

    def test_addition(self):
        assert self.feister_net._addition('100218', '090723') == '190915'
    
    def test_subduction(self):
        assert self.feister_net._subduction('190915', '100218') == '090723'
    
    def test_bin_to_digit(self):
        assert self.feister_net._bin_to_digit('100110101001', 2) == '1309'
    
    def test_psuedo_random_func(self):
        assert len(self.feister_net.psuedo_random_func('100100010101010101', 2)) == 2*self.feister_net._digit_len

    def test_feistel(self):
        ciphertext = self.feister_net.feistel('plaintext')
        assert self.feister_net.re_feistel(ciphertext) == 'plaintext'
        
        
        
        
        
        
        
        
        
        
        
        