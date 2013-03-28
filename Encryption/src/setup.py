# Copyright (C) 2012 Xu Wanqing (Vane)
#
# This module is part of MySQLdb_Encryption for python.

import os
from setuptools import setup,find_packages
import MySQLdb_Encryption

def find_packages(base):
    ret = [base]
    for path in os.listdir(base):
        if path.startswith('.'):
            continue
        full_path = os.path.join(base, path)
        if os.path.isdir(full_path):
            ret += find_packages(full_path)
    return ret

setup(
        name = "MySQLdb_Encryption",
        version=MySQLdb_Encryption.__version__,
        packages = find_packages("MySQLdb_Encryption"),

        long_description = "A module to encrypt sql values for MySQLdb module.",
        author = "Xu Wanqing (Vane)",
        author_email = "wanqxu@gmail.com",

        license = "GPL",
        keywords = ("encrypt", "MySQLdb"),
        platforms = "Independant",
        url = "",
        )

