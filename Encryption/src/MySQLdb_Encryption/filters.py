'''
Created on 2012-1-4

@author: wanqxu
'''

'''This module contains class parsing representing syntactical elements of SQL.'''

import sqlparse

class ParseSQL():
    '''
    parse sql to get keys and value. | keys: column name | value: column value |
    '''

    def __init__(self,sql):
        '''
        Initialize sql.
        '''
        self.sql = sql
        self.type = None
        self.table = None
        self.keys = []
        self.values = []
        self.prased_sql = sql
        
    def filters(self):
        '''
        Use different function to parse sql with different type of sql.
        '''
        parsed = sqlparse.parse(self.sql)
        stmt = parsed[0]
        self.type = stmt.get_type()
        if self.type == "INSERT":
            self._parse_insert(stmt)
        elif self.type == "UPDATE":
            self._parse_update(stmt)
        self._parse_where(stmt)
    
    def _parse_where(self,stmt):
        '''
        Parse where statements for sql sentence
        '''
        start_id = stmt.token_index(stmt.token_first())
        if self.table == None:
            self.table = str(stmt.token_next_by_instance(start_id,sqlparse.sql.Identifier))
        where_obj = stmt.token_next_by_instance(start_id,sqlparse.sql.Where)
        if where_obj == None:
            return
        else:
            where_list = str(where_obj)[5:].split("and")
            for where_element in where_list:
                key,value = self._parse_equals(where_element.strip())
                self.keys.append(key)
                self.values.append(value)
    
    def _parse_update(self,stmt):
        '''
        Parse update sql sentence
        '''
        start_id = stmt.token_index(stmt.token_first())
        iden = stmt.token_next_by_instance(start_id,sqlparse.sql.Identifier)
        if iden != None:
            self.table = str(iden)
            key_value_list = stmt.token_next_by_instance(start_id,sqlparse.sql.IdentifierList)
            if key_value_list == None:
                key_value = stmt.token_next_by_instance(stmt.token_index(iden)+1,sqlparse.sql.Comparison)
                key,value = self._parse_equals(key_value)
                self.keys.append(key)
                self.values.append(value)
            else:
                for key_value in key_value_list.get_identifiers():
                    key,value = self._parse_equals(key_value)
                    self.keys.append(key)
                    self.values.append(value)
        else:
            return
            
    def _parse_insert(self,stmt):
        '''
        Parse insert sql sentence
        '''
        start_id = stmt.token_index(stmt.token_first())
        func = stmt.token_next_by_instance(start_id,sqlparse.sql.Function)
        if func != None:
            self.table = str(func).split("(")[0].strip()
            key_list = func.get_parameters()
            for key in key_list:
                self.keys.append(str(key))
            has_next = True
            id = start_id
            while has_next:
                item = stmt.token_next_by_instance(id,sqlparse.sql.Parenthesis)
                if item == None:
                    has_next = False
                else:
                    id = stmt.token_index(item)+1
                    if stmt.token_index(func) < id:
                        self.values.append(self._parse_parenthesis(item))
                    else:
                        return
        else:
            return
    
    def _parse_parenthesis(self,item):
        '''
        Parse parenthesis for insert parameters
        '''
        pa = str(item)
        self.prased_sql = self.prased_sql.replace(pa, "%s")
        paras = []
        for para in pa.replace("(", "").replace(")","").split(","):
            para = self._delete_quote(para)
            paras.append(para)
        return paras
    
    def _parse_equals(self,key_value):
        '''
        Parse equals for update parameters
        '''
        pa = str(key_value)
        self.prased_sql = self.prased_sql.replace(pa, "%s")
        key,value = pa.strip().split("=")
        return self._delete_quote(key.strip()),self._delete_quote(value.strip())
    
    def _delete_quote(self,s):
        '''
        Delete quote for value
        '''
        if s[0] == '"' or s[0]=="'":
            s = s[1:len(s)-1]
        return s



