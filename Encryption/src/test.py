'''
Created on 2012-3-17

@author: wanqxu
'''

from MySQLdb_Encryption import encrypt
from MySQLdb_Encryption.encryption_lib import Prefix,CycleWalking,FeistelCycle,FFX,BPS
from MySQLdb_Encryption import setting

sql = '''
insert into encryption (func,name,password) values    
(22,1,"helloa"),
(33,2,"hellob"),
(44,3,"helloc"),
(55,4,"hellod")
'''

print "SQL: "+sql
print "setting: "
print "ENCRYPT_KEY_WORD="
print setting.ENCRYPT_KEY_WORD
print 
print "Encrypted SQL: "+encrypt(sql)
    
    