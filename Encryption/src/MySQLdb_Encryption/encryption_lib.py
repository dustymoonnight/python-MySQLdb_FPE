'''
Created on 2012-1-5

@author: wanqxu
'''
from compiler.ast import While

'''This module contains classes which are different functions to encrypt value.'''

import setting
import copy
from encryption import Encryption
from math import log
from cipher import *

PREFIX_CONFIG = setting.PREFIX_CONFIG
CYCLEWALKING_CONFIG = setting.CYCLEWALKING_CONFIG
FEISTELCYCLE_CONFIG = setting.FEISTELCYCLE_CONFIG
FFX_CONFIG = setting.FFX_COMFIG
BPS_CONFIG = setting.BPS_COMFIG
CHAOS_CONFIG = setting.CHAOS_CONFIG

# For adding an encryption functions, you just need to first add a class inherit 
# Encryption class, then overwrite the encrypt() function and decrypt() function 
# Of course, you can do anything you want in encrypt() function and decrypt() function.
class Prefix(Encryption):
    '''
    suited set size(bit): 1~20
    suited decimal digits: 1~6
    '''
    def __init__(self):
        '''
        Initialize size, key and tweak.
        '''
        self.size = 100000
        self.key = 'a,igfn/;[ciej37x'
        self.tweak = None
    
    def _achieve_config(self):
        '''
        Achieve Configuration for Prefix.
        '''
        if 'size' in PREFIX_CONFIG.keys():
            self.size = PREFIX_CONFIG['size']
        if 'key' in PREFIX_CONFIG.keys():
            self.key = PREFIX_CONFIG['key']
        if 'tweak' in PREFIX_CONFIG.keys():
            self.tweak = PREFIX_CONFIG['tweak']
                
    def _get_table(self):
        '''
        Get AES table for Prefix.
        '''
        aes_table = AESTable(self.size,self.key)
        if not aes_table.has_table():
            aes_table.construct_table()
            aes_table.store_table()
        if self.tweak != None:
            return aes_table.tweak(self.tweak)
        return aes_table.get_table()
    
    def encrypt(self,plaintext):
        '''
        Use Prefix to encrypt plaintext.
        '''
        self._achieve_config()
        encrypt_table = self._get_table()
        return int(encrypt_table[int(plaintext)])
        
    def decrypt(self,ciphertext):
        '''
        Use Prefix to decrypt ciphertext.
        '''
        self._achieve_config()
        encrypt_table = self._get_table()
        return encrypt_table.index(str(ciphertext))
    
    
class CycleWalking(Encryption):
    '''
    suited set size(bit): 115~128
    suited decimal digits: 34~38
    '''
    def __init__(self):
        '''
        Initialize size and key
        '''
        self.size = 1<<128
        self.key = 'a,igfn/;[ciej37x'
    
    def _achieve_config(self):
        '''
        Achieve Configuration for CycleWalking.
        '''
        if 'size' in CYCLEWALKING_CONFIG.keys():
            self.size = CYCLEWALKING_CONFIG['size']
        if 'key' in CYCLEWALKING_CONFIG.keys():
            self.key = CYCLEWALKING_CONFIG['key']
    
    def _encode_long(self,value):
        '''
        Encode long int value to binary.
        '''
        l,r = split_bin(value,64)
        encode_plaintext = struct.pack('Q'*2,r,l)[::-1]
        return encode_plaintext
    
    def _aes_encrypt(self,encode_plaintext):
        '''
        Use AES to encrypt binary encoded plaintext.
        '''
        obj = AES.new(self.key,AES.MODE_CFB)   
        return obj.encrypt(encode_plaintext)
    
    def _aes_decrypt(self,encode_ciphertext):
        '''
        Use AES to decrypt binary encoded ciphertext.
        '''
        obj = AES.new(self.key,AES.MODE_CFB)   
        return obj.decrypt(encode_ciphertext)
        
    def encrypt(self,plaintext):
        '''
        Use CycleWalking to encrypt plaintext.
        '''
        self._achieve_config()
        encode_plaintext = self._encode_long(int(plaintext))
        ciphertext = self._aes_encrypt(encode_plaintext)
        ciphertext10 = int(ciphertext.encode('hex'),16)
        while ciphertext10>self.size:
            ciphertext = self._aes_encrypt(ciphertext)
            ciphertext10 = int(ciphertext.encode('hex'),16)
        return ciphertext10
        
    def decrypt(self,ciphertext):
        '''
        Use CycleWalking to decrypt ciphertext.
        '''
        self._achieve_config()
        encode_ciphertext = self._encode_long(int(ciphertext))
        plaintext = self._aes_decrypt(encode_ciphertext)
        plaintext10 = int(plaintext.encode('hex'),16)
        while plaintext10>self.size:
            plaintext = self._aes_decrypt(plaintext)
            plaintext10 = int(plaintext.encode('hex'),16)
        return plaintext10


class FeistelCycle(Encryption):
    '''
    suited set size(bit): 40~240
    suited decimal digits: 12~80
    '''
    def __init__(self):
        '''
        Initialize size and key
        '''
        self.size = (1<<129)-1
        self.key = 'a,igfn/;[ciej37x'
    
    def _achieve_config(self):
        '''
        Achieve Configuration for FeistelCycle.
        '''
        if 'size' in FEISTELCYCLE_CONFIG.keys():
            self.size = FEISTELCYCLE_CONFIG['size']
        if 'key' in FEISTELCYCLE_CONFIG.keys():
            self.key = FEISTELCYCLE_CONFIG['key']
    
    def _feistel_encript(self,plaintext):
        '''
        Use BalanceFeistelNet to encrypt plaintext.
        '''
        feistel_net = BalanceFeistelNet(self.size,self.key,16)
        return feistel_net.feistel(plaintext)
    
    def _feistel_decrypt(self,ciphertext):
        '''
        Use BalanceFeistelNet to decrypt ciphertext.
        '''
        feistel_net = BalanceFeistelNet(self.size,self.key,16)
        return feistel_net.re_feistel(ciphertext)
    
    def encrypt(self,plaintext):
        '''
        Use FeistelCycle to encrypt plaintext.
        '''
        self._achieve_config()
        ciphertext = self._feistel_encript(int(plaintext))
        while ciphertext>self.size:
            ciphertext = self._feistel_encript(ciphertext)
        return ciphertext
        
    def decrypt(self,ciphertext):
        '''
        Use FeistelCycle to decrypt ciphertext.
        '''
        self._achieve_config()
        plaintext = self._feistel_decrypt(int(ciphertext))
        while plaintext>self.size:
            plaintext = self._feistel_decrypt(plaintext)
        return plaintext
    

class FFX(Encryption):
    '''
    suited all chars
    '''
    def __init__(self):
        '''
        Initialize key, rounds and chars
        '''
        self.key = 'a,igfn/;[ciej37x' 
        self.rounds = 16
        self.chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']   
        
    def _achieve_config(self):
        '''
        Achieve Configuration for FFX.
        '''
        if 'key' in FFX_CONFIG.keys():
            self.key = FFX_CONFIG['key']
        if 'rounds' in FFX_CONFIG.keys():
            self.rounds = FFX_CONFIG['rounds']
        if 'chars' in FFX_CONFIG.keys():
            self.chars = FFX_CONFIG['chars']
    
    def encrypt(self,plaintext):
        '''
        Use FFX to encrypt plaintext.
        ''' 
        self._achieve_config()
        im_feistel = ImbalanceFeistelNet(self.chars, self.key, self.rounds)
        return im_feistel.feistel(plaintext)
    
    def decrypt(self,ciphertext):
        '''
        Use FFX to decrypt ciphertext.
        '''
        self._achieve_config()
        im_feistel = ImbalanceFeistelNet(self.chars, self.key, self.rounds)
        return im_feistel.re_feistel(ciphertext)
    
class BPS(Encryption):
    '''
    suited all chars
    '''
    def __init__(self):
        '''
        Initialize key, rounds, tweak and chars 
        '''
        self.key = 'a,igfn/;[ciej37x' 
        self.rounds = 16
        self.tweak = 9223372036855207021
        self.chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']   
        
    def _achieve_config(self):
        '''
        Achieve Configuration for BPS.
        '''
        if 'key' in BPS_CONFIG.keys():
            self.key = BPS_CONFIG['key']
        if 'rounds' in BPS_CONFIG.keys():
            self.rounds = BPS_CONFIG['rounds']
        if 'chars' in BPS_CONFIG.keys():
            self.chars = BPS_CONFIG['chars']
        if 'tweak' in BPS_CONFIG.keys():
            self.tweak = BPS_CONFIG['tweak']
    
    def _get_s(self):
        '''
        Get the length of chars
        '''
        return len(self.chars)
    
    def _get_s_integer(self,astring):
        '''
        Map a string to a sum of digits.
        '''
        X = []
        for i in range(0,len(astring)):
            if astring[i] in self.chars:
                X.append(self.chars.index(astring[i]))
            else:
                raise Exception("Input error, the plaintext has some chars not in BPS configuration.")
        return X
    
    def _return_to_string(self,X):
        '''
        Map a sum of digits to a string.
        '''
        astring = ''
        for i in range(0,len(X)):
            astring = astring + self.chars[X[i]]
        return astring
    
    def _subduction(self,c,a,n):
        '''
        For an operation of c=(a+b)%n, we now know c, a and n, get b
        '''
        if c>=a:
            return c-a
        else:
            return c+n-a
        
    def encrypt(self,plaintext):
        '''
        Use BPS to encrypt plaintext.
        ''' 
        self._achieve_config()
        s = self._get_s()
        X = self._get_s_integer(plaintext)
        b = len(X)
        max_b = int(log(1<<96,s))*2
        if b<=max_b:
            bc = BPS_BC(s, self.key, self.rounds, self.tweak)
            Y = bc.encryption(X)
        else:
            rest = b % max_b
            c = 0
            i = 0
            Y = copy.copy(X)
            while b-c>max_b:
                if i!= 0:
                    for j in range(0,max_b):
                        Y[j+c] = (Y[c+j-max_b]+Y[c+j])%s
                bc = BPS_BC(s, self.key, self.rounds, self.tweak^(i*(1<<16))^(i*(1<<48)))
                Y[c:c+max_b] = copy.copy(bc.encryption(Y[c:c+max_b]))
                c = c+max_b
                i = i+1
            if b != c:
                for j in range(1,rest+1):
                    Y[b-j] = (Y[b-j-max_b]+Y[b-j])%s
                bc = BPS_BC(s, self.key, self.rounds, self.tweak^(i*(1<<16))^(i*(1<<48)))
                Y[b-max_b:b] = copy.copy(bc.encryption(Y[b-max_b:b]))
        return self._return_to_string(Y)
                            
    def decrypt(self,ciphertext):
        '''
        Use BPS to decrypt ciphertext.
        '''
        self._achieve_config()
        s = self._get_s()
        X = self._get_s_integer(ciphertext)
        b = len(X)
        max_b = int(log(1<<96,s))*2
        if b<=max_b:
            bc = BPS_BC(s, self.key, self.rounds, self.tweak)
            Y = bc.decryption(X)
        else:
            rest = b % max_b
            c = b - rest
            i = c/max_b
            Y = copy.copy(X)
            if b != c:
                bc = BPS_BC(s, self.key, self.rounds, self.tweak^(i*(1<<16))^(i*(1<<48)))
                Y[b-max_b:b] = copy.copy(bc.decryption(Y[b-max_b:b]))
                for j in range(1,rest+1):
                    Y[b-j] = self._subduction(Y[b-j], Y[b-j-max_b], s)
            while c!=0:
                c = c-max_b
                i = i-1
                bc = BPS_BC(s, self.key, self.rounds, self.tweak^(i*(1<<16))^(i*(1<<48)))
                Y[c:c+max_b] = copy.copy(bc.decryption(Y[c:c+max_b]))
                if i!= 0:
                    for j in range(0,max_b):
                        Y[j+c] = self._subduction(Y[c+j],Y[c+j-max_b],s)
        return self._return_to_string(Y)

class ChaosFeistel(Encryption):
    '''
    suit all chars.
    '''
    def __init__(self):
        '''
        Initialize coefficient, rounds and original 
        '''
        self.cft = 3.8
        self.rounds = 16
        self.original = 0.2873
    
    def _achieve_config(self):
        '''
        Achieve Configuration for ChaosFeistel.
        '''
        if 'cft' in CHAOS_CONFIG.keys():
            self.cft = CHAOS_CONFIG['cft']
        if 'rounds' in CHAOS_CONFIG.keys():
            self.rounds = CHAOS_CONFIG['rounds']
        if 'original' in CHAOS_CONFIG.keys():
            self.original = CHAOS_CONFIG['original']
    
    def encrypt(self,plaintext):
        '''
        Use ChaosFeistel to encrypt plaintext.
        ''' 
        af = ASCII_Feistel(self.cft,self.original,self.rounds)
        return af.feistel(plaintext)
                            
    def decrypt(self,ciphertext):
        '''
        Use ChaosFeistel to decrypt ciphertext.
        '''
        pass
    
        