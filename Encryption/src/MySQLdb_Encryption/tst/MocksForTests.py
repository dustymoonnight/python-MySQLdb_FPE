'''
Created on 2012-1-9

@author: wanqxu
'''

from MySQLdb_Encryption.encryption import Encryption
from MySQLdb_Encryption.engine import Encrypt
from MySQLdb_Encryption.encryption_lib import Prefix

class ParseSQL():
    '''
    mock class ParseSQL
    '''

    def __init__(self,sql,type,table,keys,values,prased_sql):
        self.sql = sql
        self.type = type
        self.table = table
        self.keys = keys
        self.values = values
        self.prased_sql = prased_sql
    
    def filters(self):
        pass
    
class MockEn1(Encryption):
    '''
    mock Encryption Function
    '''
    def encrypt(self,plaintext):
        return "en1"

class MockEn2(Encryption):
    '''
    mock Encryption Function
    '''
    def encrypt(self,plaintext):
        return "en2"
        
class MokeEncrypt(Encrypt):
    def _get_encrypt_pair(self,filters):
        encrypt_pair = {}
        if filters.table in self._encrypt_key_word.keys():
            for key in filters.keys:
                if (key in self._encrypt_key_word[filters.table].keys()):
                    encrypt_pair[key] = eval(self._encrypt_key_word[filters.table][key])
        return encrypt_pair

