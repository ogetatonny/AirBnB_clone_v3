#!/usr/bin/python3

'''
    Here is where users of model tests are put into practice.
'''

import unittest
import pep8
from models.base_model import BaseModel
from models.city import City
from os import getenv, remove

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
        cls.new_city = City()
        cls.new_city.state_id = "California"
        cls.new_city.name_id = "San Francisco"

    @classmethod
    def tearDownClass(cls):
        '''
            Destroys the unittest
        '''
        del cls.new_city
        try:
            remove("file.json")
        except FileNotFoundError:
            pass

    def test_City_dbtable(self):
        '''
            Verify that the tablename is accurate
        '''
        self.assertEqual(self.new_city.__tablename__, "cities")

    def test_City_inheritance(self):
        '''
            Verifies the City class is descended from BaseModel
        '''
        self.assertIsInstance(self.new_city, BaseModel)

    def test_User_attributes(self):
        '''
            Existing test user attributes
        '''
        self.assertTrue("state_id" in self.new_city.__dir__())
        self.assertTrue("name" in self.new_city.__dir__())

    @unittest.skipIf(storage == "db", "Testing database storage only")
    def test_type_name(self):
        '''
            Verify the name type
        '''
        name = getattr(self.new_city, "name")
        self.assertIsInstance(name, str)

    @unittest.skipIf(storage == "db", "Testing database storage only")
    def test_type_name(self):
        '''
            Check the name kind
        '''
        name = getattr(self.new_city, "state_id")
        self.assertIsInstance(name, str)
