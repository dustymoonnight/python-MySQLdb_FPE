# Copyright (C) 2012 Xu Wanqing (Vane)
#
# This module is test of MySQLdb_Encryption for python.

''' Run all tests for MySQLdb_Encryption '''

import glob
import unittest
import sys
import os

def run_all_tests():
    dir = os.getcwd()
    test_file_strings = glob.glob(dir+'\\'+'Test*.py')
    
    module_strings = [str[len(dir)+1:len(str)-3] for str in test_file_strings]
    suites = [unittest.defaultTestLoader.loadTestsFromName(str) for str
              in module_strings]
    testSuite = unittest.TestSuite(suites)
    text_runner = unittest.TextTestRunner(verbosity=2).run(testSuite)
    
    if text_runner.wasSuccessful():
        pass
    else:
        sys.exit(-1)

run_all_tests()
