''' Tests encrypt classes. '''

import unittest
from MocksForTests import *

class TestEncrypt(unittest.TestCase):
    
    def setUp(self):
        self.ENCRYPT_KEY_WORD = {
                "encryption": {"func":"MockEn1","name":"MockEn2"},
                }
        
    def test_encrypt_insert(self):
        obj_pa = ParseSQL("insert into encryption (name,password,func) values ('aa','bb','cc')",
                 "INSERT","encryption",["name","password","func"],[['aa','bb','cc']],
                 "insert into encryption (name,password,func) values %s")
        obj_en = MokeEncrypt(obj_pa,self.ENCRYPT_KEY_WORD,Encryption)
        self.assertEqual(obj_en.get_prased_sql(),"insert into encryption (name,password,func) values ('en2', 'bb', 'en1')")
    
    def test_encrypt_update(self):
        obj_pa = ParseSQL("update encryption set name='aa',password='bb' where func='cc'",
                 "UPDATE","encryption",["name","password","func"],['aa','bb','cc'],
                 "update encryption set %s,%s where %s")
        obj_en = MokeEncrypt(obj_pa,self.ENCRYPT_KEY_WORD,Encryption)
        self.assertEqual(obj_en.get_prased_sql(),'update encryption set name="en2",password="bb" where func="en1"')
        
    def test_encrypt_select(self):
        obj_pa = ParseSQL("select * from encryption where func='cc' and password='bb'",
                 "SELECT","encryption",["func","password"],['cc','bb'],
                 "select * from encryption where %s and %s")
        obj_en = MokeEncrypt(obj_pa,self.ENCRYPT_KEY_WORD,Encryption)
        self.assertEqual(obj_en.get_prased_sql(),'select * from encryption where func="en1" and password="bb"')
    
    def test_encrypt_delete(self):
        obj_pa = ParseSQL("delete from encryption where func='cc' and password='bb'",
                 "DELETE","encryption",["func","password"],['cc','bb'],
                 "delete from encryption where %s and %s")
        obj_en = MokeEncrypt(obj_pa,self.ENCRYPT_KEY_WORD,Encryption)
        self.assertEqual(obj_en.get_prased_sql(),'delete from encryption where func="en1" and password="bb"')
        
    