'''
Created on 2012-1-9

@author: wanqxu
'''

'''This module contains basic class to encrypt value.'''

class Encryption():
    '''
    Base function for encrypt value, just return the value itself.
    '''
    def __init__(self):
        '''
        Initialize for Encryption
        '''
        pass
        
    def _achieve_config(self):
        '''
        Achieve Configuration for Encryption.
        '''
        pass
    
    def encrypt(self,plaintext):
        '''
        Encrypt plaintext.
        '''
        return plaintext

    def decrypt(self,ciphertext):
        '''
        Decrypt ciphertext.
        '''
        return ciphertext