#!/usr/bin/python3
'''
    Include assessments for the state module.
'''
import unittest
from models.base_model import BaseModel
from models.state import State
from os import getenv, remove
import pep8

storage = getenv("HBNB_TYPE_STORAGE", "fs")


class TestState(unittest.TestCase):
    '''
        Examine the State course.
    '''

    @classmethod
    def setUpClass(cls):
        '''
            Unittest is set up
        '''
        cls.new_state = State()
        cls.new_state.name = "California"

    @classmethod
    def tearDownClass(cls):
        '''
            Destroys the unittest
        '''
        del cls.new_state
        try:
            remove("file.json")
        except FileNotFoundError:
            pass

    def test_States_dbtable(self):
        '''
            Verify that the tablename is accurate
        '''
        self.assertEqual(self.new_state.__tablename__, "states")

    def test_State_inheritence(self):
        '''
            Verify State class is descended from the BaseModel.
        '''
        self.assertIsInstance(self.new_state, BaseModel)

    def test_State_attributes(self):
        '''
            Verify if the attribute `name` is present in the State class
        '''
        self.assertTrue("name" in self.new_state.__dir__())

    @unittest.skipIf(storage == "db", "Testing database storage only")
    def test_State_attributes_type(self):
        '''
            Verify name of State class attribute is class type str.
        '''
        name = getattr(self.new_state, "name")
        self.assertIsInstance(name, str)
