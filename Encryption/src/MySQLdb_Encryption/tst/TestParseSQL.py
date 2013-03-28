''' Tests prase_sql functions. '''

import unittest
from MySQLdb_Encryption.filters import ParseSQL

class TestParseSQL(unittest.TestCase):
    
    def test_prase_insert_with_keys(self):
        sql = 'insert into test (name,value) values ("me","ok")'
        obj_pa = ParseSQL(sql)
        obj_pa.filters()
        self.assertEqual(obj_pa.keys,["name","value"])
        self.assertEqual(obj_pa.values,[["me","ok"]])
        self.assertEqual(obj_pa.table,"test")
        self.assertEqual(obj_pa.prased_sql,"insert into test (name,value) values %s")
        self.assertEqual(obj_pa.type,"INSERT")
    
    def test_prase_insert_without_keys(self):
        sql = 'insert into test values ("me","ok")'
        obj_pa = ParseSQL(sql)
        obj_pa.filters()
        self.assertEqual(obj_pa.keys,[])
        self.assertEqual(obj_pa.values,[])
        self.assertEqual(obj_pa.table,"test")
        self.assertEqual(obj_pa.prased_sql,'insert into test values ("me","ok")')
        self.assertEqual(obj_pa.type,"INSERT")
    
    def test_prase_update(self):
        sql = 'update test set name="me" , value="ok" where id="1" and password="000000"'
        obj_pa = ParseSQL(sql)
        obj_pa.filters()
        self.assertEqual(obj_pa.keys,["name","value","id","password"])
        self.assertEqual(obj_pa.values,["me","ok","1","000000"])
        self.assertEqual(obj_pa.table,"test")
        self.assertEqual(obj_pa.prased_sql,"update test set %s , %s where %s and %s")
        self.assertEqual(obj_pa.type,"UPDATE")
        
    def test_prase_select(self):
        sql = 'select * from test where name="me" and value="ok"'
        obj_pa = ParseSQL(sql)
        obj_pa.filters()
        self.assertEqual(obj_pa.keys,["name","value"])
        self.assertEqual(obj_pa.values,["me","ok"])
        self.assertEqual(obj_pa.table,"test")
        self.assertEqual(obj_pa.prased_sql,"select * from test where %s and %s")
        self.assertEqual(obj_pa.type,"SELECT")
        
    def test_prase_delete(self):
        sql = 'delete from test where name="me" and value="ok"'
        obj_pa = ParseSQL(sql)
        obj_pa.filters()
        self.assertEqual(obj_pa.keys,["name","value"])
        self.assertEqual(obj_pa.values,["me","ok"])
        self.assertEqual(obj_pa.table,"test")
        self.assertEqual(obj_pa.prased_sql,"delete from test where %s and %s")
        self.assertEqual(obj_pa.type,"DELETE")





