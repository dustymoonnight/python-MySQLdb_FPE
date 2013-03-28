'''
Created on 2012-1-5

@author: wanqxu
'''

import sys
from encryption_lib import *

class Encrypt():
    
    def __init__(self,filters,setting,encryption):
        '''
        Initialize filters, setting and encryption.
        '''
        self._parse_sql = filters
        self._parsed_sql = None
        self._encrypt_key_word = setting
        self._encryption = encryption
        
    def _prase_sql(self):
        '''
        Use filters to prase sql.
        '''
        self._parse_sql.filters()
        self._parsed_sql = self._parse_sql.prased_sql
    
    def _get_encrypt_pair(self,filters):
        '''
        Get the key, value pairs which need to be encrypted.
        '''
        encrypt_pair = {}
        if filters.table in self._encrypt_key_word.keys():
            for key in filters.keys:
                if (key in self._encrypt_key_word[filters.table].keys()):
                    encrypt_pair[key] = eval(self._encrypt_key_word[filters.table][key])
        return encrypt_pair
    
    def _do_encryption(self,encrypt_pair,filters):
        '''
        Encrypt the value use different function for different type of sql.
        '''
        if filters.type == "INSERT":
            return self._do_parenthesis_encrypt(encrypt_pair,filters)
        return self._do_equals_encrypt(encrypt_pair,filters)
    
    def _do_parenthesis_encrypt(self,encrypt_pair,filters):
        '''
        Encrypt values, if the keys and values was as format like: (key1,key2,...) values (value1, value2,...)
        '''
        values = filters.values
        ret = []
        encrypt_indexes = encrypt_pair.keys()
        for value in values:
            sub_ret = []
            for index in range(0,len(value)):
                key =  filters.keys[index]
                if key in encrypt_indexes:
                    encrypt_func = encrypt_pair[key]()
                    if isinstance(encrypt_func, self._encryption):
                        sub_ret.append(str(encrypt_func.encrypt(value[index])))
                    else:
                        sys.stderr.write("ERROR: ***" + str(encrypt_pair[key]) +" is not an encryption function class.")
                else:
                    sub_ret.append(value[index])
            ret.append(tuple(sub_ret))
        return tuple(ret)
                    
    def _do_equals_encrypt(self,encrypt_pair,filters):
        '''
        Encrypt values, if the keys and values was as format like: key = value
        '''
        values = filters.values
        ret = []
        encrypt_indexes = encrypt_pair.keys()
        for index in range(0,len(filters.values)):
            key =  filters.keys[index]
            sub_ret = key+"="
            if key in encrypt_indexes:
                encrypt_func = encrypt_pair[key]()
                if isinstance(encrypt_func, self._encryption):
                    sub_ret = sub_ret + self._add_quote(str(encrypt_func.encrypt(values[index])))
                else:
                    sys.stderr.write("ERROR: ***" + str(encrypt_pair[key]) +" is not an encryption function class.")
            else:
                sub_ret = sub_ret + self._add_quote(values[index])
            ret.append(sub_ret)
        return tuple(ret)
    
    def _add_quote(self,s):
        '''
        Add a quote for value
        '''
        s = '"'+s+'"'
        return s
    
    def get_prased_sql(self):
        '''
        Get sql which has already been encrypted.
        '''
        self._prase_sql()
        encrypt_pair = self._get_encrypt_pair(self._parse_sql)
        prased_values = self._do_encryption(encrypt_pair, self._parse_sql)
        if prased_values == None:
            return self._parsed_sql
        else:
            return self._parsed_sql % prased_values


