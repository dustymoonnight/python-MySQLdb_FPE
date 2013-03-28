''' Tests base encryption classes. '''

import unittest
from MySQLdb_Encryption.encryption import Encryption

class TestBaseEncryption(unittest.TestCase):
    
    def test_encrypt(self):
        en_func = Encryption()
        self.assertEqual(en_func.encrypt("value"),"value")