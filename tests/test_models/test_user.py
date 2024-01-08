#!/usr/bin/python3

'''
    Here is where all user model tests are put into practice.
'''

import unittest
from models.base_model import BaseModel
from models.user import User
from os import getenv, remove
from io import StringIO
import sys
import datetime
import pep8


storage = getenv("HBNB_TYPE_STORAGE", "fs")


class TestUser(unittest.TestCase):
    '''
        User class testing
    '''
    @classmethod
    def setUpClass(cls):
        '''
            Unittest is set up
        '''
        cls.new_user = User()
        cls.new_user.email = "email@gmail.com"
        cls.new_user.password = "password"
        cls.new_user.firt_name = "Mel"
        cls.new_user.last_name = "Ng"

    @classmethod
    def tearDownClass(cls):
        '''
            Destroys the unittest
        '''
        del cls.new_user
        try:
            remove("file.json")
        except FileNotFoundError:
            pass

    def test_User_dbtable(self):
        '''
            Verify that the tablename is accurate
        '''
        self.assertEqual(self.new_user.__tablename__, "users")

    def test_User_inheritance(self):
        '''
            Verifies the User class is descended from BaseModel
        '''
        self.assertIsInstance(self.new_user, BaseModel)

    def test_User_attributes(self):
        '''
            Verify the existence of the user characteristics
        '''
        self.assertTrue("email" in self.new_user.__dir__())
        self.assertTrue("first_name" in self.new_user.__dir__())
        self.assertTrue("last_name" in self.new_user.__dir__())
        self.assertTrue("password" in self.new_user.__dir__())

    @unittest.skipIf(storage == "db", "Testing database storage only")
    def test_type_email(self):
        '''
            Verify the name type
        '''
        name = getattr(self.new_user, "email")
        self.assertIsInstance(name, str)

    @unittest.skipIf(storage == "db", "Testing database storage only")
    def test_type_first_name(self):
        '''
            Check the name kind
        '''
        name = getattr(self.new_user, "first_name")
        self.assertIsInstance(name, str)

    @unittest.skipIf(storage == "db", "Testing database storage only")
    def test_type_last_name(self):
        '''
            Verify the last_name type
        '''
        name = getattr(self.new_user, "last_name")
        self.assertIsInstance(name, str)

    @unittest.skipIf(storage == "db", "Testing database storage only")
    def test_type_password(self):
        '''
            Verify the password type
        '''
        name = getattr(self.new_user, "password")
        self.assertIsInstance(name, str)
