#!/usr/bin/python3

'''
    This is where the amenity models tests are all put to use.
'''

import unittest
import pep8
from models.base_model import BaseModel
from models.amenity import Amenity
from os import getenv, remove


storage = getenv("HBNB_TYPE_STORAGE", "fs")


class TestAmenity(unittest.TestCase):
    '''
        Assessing the Amenity class
    '''
    @classmethod
    def setUpClass(cls):
        '''
            Unittest is set up.
        '''
        cls.new_amenity = Amenity()
        cls.new_amenity.name = "wifi"

    @classmethod
    def tearDownClass(cls):
        '''
            Destroys the unittest
        '''
        del cls.new_amenity
        try:
            remove("file.json")
        except FileNotFoundError:
            pass

    def test_pep8_style_check(self):
        '''
            Pep8 style is tested
        '''
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/amenity.py'])
        self.assertEqual(p.total_errors, 0, "pep8 error needs fixing")

    def test_States_dbtable(self):
        '''
            Verify that the tablename is accurate
        '''
        self.assertEqual(self.new_amenity.__tablename__, "amenities")

    def test_Amenity_inheritence(self):
        '''
            Verifies the Amenity class is descended from BaseModel
        '''
        self.assertIsInstance(self.new_amenity, BaseModel)

    def test_Amenity_attributes(self):
        '''
            Verify the name attribute of the Amenity class.
        '''
        self.assertTrue("name" in self.new_amenity.__dir__())

    @unittest.skipIf(storage == "db", "Testing database storage only")
    def test_Amenity_attribute_type(self):
        '''
            Verify type of the name attribute for Amenity class.
        '''
        name_value = getattr(self.new_amenity, "name")
        self.assertIsInstance(name_value, str)
