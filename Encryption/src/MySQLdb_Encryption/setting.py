'''
Created on 2011-12-30

@author: wanqxu
'''

# Add an table to be encrypted.
# "table name":{"column name":"encryption function","column name":"encryption function",...}
# Attention: encryption function must been defined in encryption_functions module and must be 
#            a subclass of EncryptionFunction.(For more information, see the encryption_functions module.)
# Example:
ENCRYPT_KEY_WORD = {
#        "encryption": {"func":"Prefix","name":"FeistelCycle","password":"BPS"},
#        "test": {"id":"Prefix"},
#        "Person": {"LastName":"Prefix"}
}

#PREFIX_CONFIG: suited size: 1 ~ 1<<20, key is 16 byte 
PREFIX_CONFIG = {
#        'size':100,
#        'key':'d'*16,
#        'tweak':1,
}

#CYCLEWALKING_CONFIG: suited size: 1<<115 ~ 1<<128, key is 16 byte 
CYCLEWALKING_CONFIG = {
#        'size':1<<125,
#        'key':'d'*16,
}

#FEISTELCYCLE_CONFIG: suited size: 1<<40 ~ 1<<240, key is 16 byte 
FEISTELCYCLE_CONFIG = {
#        'size':1<<230,
#        'key':'d'*16,
}

#FFX_CONFIG: suited all chars.
#Put the char you want to the chars parameter.
FFX_COMFIG = {
#        'chars':['0','1','2','3','4','5','6','7','8','9']
#        'key':'d'*16,
#        'rounds':16,
#        'chars':['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'],
}

#BPS_CONFIG: suited all chars.
#Put the char you want to the chars parameter.
BPS_COMFIG = {
        'chars':['0','1','2','3','4','5','6','7','8','9']
#        'key':'d'*16,
#        'rounds':16,
#        'tweak':9223372036855207028,
#        'chars':['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'],
}

#CHAOS_CONFIG: suited all chars.
#Put the char you want to the chars parameter.
#cft in 3.7~4.0, original in 0~1
CHAOS_CONFIG = {
#        'rounds':16,
#        'cft':3.7,
#        'original':0.9125,
}

