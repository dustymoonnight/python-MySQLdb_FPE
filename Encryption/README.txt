Powered by Xu Wanqing.
Email: wanqxu@gmail.com.
---------------------------------------------------------------------------------------

Pack to windows execution file:
	python setup.py bdist_wininst
---------------------------------------------------------------------------------------

Installation:
	1.put the setup_win.py file in the same folder with execution file.
	2.run command: python setup_win.py
---------------------------------------------------------------------------------------

Test:
	python <path>\Lib\site-packages\MySQLdb_Encryption\tst\RunAllTests.py
---------------------------------------------------------------------------------------

Setting:
	1.open <path>\Lib\site-packages\MySQLdb_Encryption\setting.py
	2.Add an table to be encrypted.
		ENCRYPT_KEY_WORD = {
			"table name1":{"column name":"encryption function","column name":"encryption function",...},
			"table name2":{"column name":"encryption function","column name":"encryption function",...},
			...
		}
	3.Config encryption function.
		<encryption function>_CONFIG = {
	        key:value,
	        key:value,
	        ...
		}
---------------------------------------------------------------------------------------

Example:

	1.without setting:
		>>import MySQLdb
		>>conn = MySQLdb.connect(host="localhost",user="root",password="root",db="encryption",port=3306)
		>>cur = conn.cursor()
		>>cur.execute("insert into encryption (name,password) values ('hello',22)")
		
	  In db:encryption:
	  	name = hello, password = 22.
	  	
	2.setting:
		ENCRYPT_KEY_WORD = {
			"encryption":{"password":"Prefix"}
		}
		PREFIX_CONFIG = {
	        'size':100,
	        'key':'d'*16,
	        'tweak':1,
		}
		
		>>import MySQLdb
		>>conn = MySQLdb.connect(host="localhost",user="root",password="root",db="encryption",port=3306)
		>>cur = conn.cursor()
		>>cur.execute("insert into encryption (name,password) values ('hello',22)")
	  
	  In db:encryption:
	  	name = hello, password = 89.
---------------------------------------------------------------------------------------
	