# Copyright (C) 2012 Xu Wanqing (Vane)
#
# This module is part of MySQLdb_Encryption for python.

import os
import sys

def init(path):
    configures = ["db.query(encrypt(q))","from MySQLdb_Encryption import *\n"]
    fs = open(path)
    contents = fs.read()
    fs.close()
    if (configures[0] not in contents) and (configures[1] not in contents):
        fr = open(path)
        file = []
        for line in fr.readlines(): 
            done_import = False
            if "db.query(q)" in line:
                line = line.replace("db.query(q)",configures[0])
            file.append(line)
            if done_import == False and "import re" in line:
                file.append(configures[1])
                done_import = True
        fr.close()
        fw = open(path,"w")
        for sentence in file:
            fw.writelines(sentence)
        fw.close()
        
def findMySQLdb():
    lib = sys.prefix+"\Lib\site-packages"
    mysqldb = "MySQLdb"
    cursor = "cursors.py"
    if mysqldb in os.listdir(lib) and cursor in os.listdir(lib+"\\"+mysqldb):
        return lib+"\\"+mysqldb+"\\"+cursor
    else:
        sys.stderr.write("ERROR: *** There is no MySQLdb module, please install it. ***")
        print "install failed!"
        exit(1)

if __name__ == '__main__':
    print "prepare to install..."
    if os.path.isfile('MySQLdb_Encryption-1.0.win32.exe'):
        os.popen('MySQLdb_Encryption-1.0.win32.exe')
        init(findMySQLdb())
        print "install successfully!"
        exit(0)
    else:
        sys.stderr.write("ERROR: *** Lack of module. ***")
        print "install failed!"
        exit(1)

