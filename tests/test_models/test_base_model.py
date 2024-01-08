#!/usr/bin/python3

'''
    Here is where all of the base_model tests are implemented.
'''

import unittest
import sys
import datetime
from models.base_model import BaseModel
from io import StringIO
from os import getenv

storage = getenv("HBNB_TYPE_STORAGE", "fs")


class TestBase(unittest.TestCase):
    '''
        Examining the model of basic class.
    '''
    def setUp(self):
        '''
            Setting up the instance.
        '''
        self.my_model = BaseModel()
        self.my_model.name = "Binita Rai"
        self.new = BaseModel()

    def TearDown(self):
        '''
            Eliminating the instance.
        '''
        del self.my_model

    def test_id_type(self):
        '''
            Verifies the identity's string type.
        '''
        self.assertEqual("<class 'str'>", str(type(self.my_model.id)))

    def test_ids_differ(self):
        '''
            Verifies the IDs of two instances differ from one another.
        '''
        new_model = BaseModel()
        self.assertNotEqual(new_model.id, self.my_model.id)

    def test_name(self):
        '''
            Verifies if an attribute is addable.
        '''
        self.assertEqual("Binita Rai", self.my_model.name)

    def test_a_updated_created_equal(self):
        '''
            Verify if the two dates are the same.
        '''
        self.assertEqual(self.my_model.updated_at.year,
                         self.my_model.created_at.year)

    def test_str_overide(self):
        '''
            Verifies the correct message is printed.
        '''
        backup = sys.stdout
        inst_id = self.my_model.id
        capture_out = StringIO()
        sys.stdout = capture_out
        print(self.my_model)

        cap = capture_out.getvalue().split(" ")
        self.assertEqual(cap[0], "[BaseModel]")

        self.assertEqual(cap[1], "({})".format(inst_id))
        sys.stdout = backup

    def test_to_dict_type(self):
        '''
            Verifies the return type of the to_dict function.
        '''

        self.assertEqual("<class 'dict'>",
                         str(type(self.my_model.to_dict())))

    def test_to_dict_class(self):
        '''
            Verifies the existence of the __class__ key.
        '''

        self.assertEqual("BaseModel", (self.my_model.to_dict())["__class__"])

    def test_to_dict_type_updated_at(self):
        '''
            Verifies the updated_at value type.
        '''
        self.assertEqual("<class 'str'>",
                         str(type((self.my_model.to_dict())["updated_at"])))

    def test_to_dict_type_created_at(self):
        '''
            Verifies the kind of created_at value.
        '''
        tmp = self.my_model.to_dict()
        self.assertEqual("<class 'str'>", str(type(tmp["created_at"])))

    def test_kwargs_instantiation(self):
        '''
            Verify that the key-value pair is used
            to construct an instance.
        '''
        my_model_dict = self.my_model.to_dict()
        new_model = BaseModel(**my_model_dict)
        self.assertEqual(new_model.id, self.my_model.id)

    def test_type_created_at(self):
        '''
            Verify that the updated_at data type for
            the new_model is datetime.
        '''
        my_model_dict = self.my_model.to_dict()
        new_model = BaseModel(my_model_dict)
        self.assertTrue(isinstance(new_model.created_at, datetime.datetime))

    def test_type_updated_at(self):
        '''
            Verify that the data type for
            the new_model is datetime.
        '''
        my_model_dict = self.my_model.to_dict()
        new_model = BaseModel(my_model_dict)
        self.assertTrue(isinstance(new_model.updated_at, datetime.datetime))

    def test_compare_dict(self):
        '''
            Verify that the dictionary values of the new_model
            and my_model are the same.
        '''
        my_model_dict = self.my_model.to_dict()
        new_model = BaseModel(**my_model_dict)
        new_model_dict = new_model.to_dict()
        self.assertEqual(my_model_dict, new_model_dict)

    def test_instance_diff(self):
        '''
            Verify that the instances of my_model
            and new_model are different.
        '''
        my_model_dict = self.my_model.to_dict()
        new_model = BaseModel(my_model_dict)
        self.assertNotEqual(self.my_model, new_model)

    @unittest.skipIf(storage == "db", "Testing database storage only")
    def test_save(self):
        '''
            Verifies that the dates in the updated_at
            attribute are different after updating the instance.
        '''
        old_update = self.new.updated_at
        self.new.save()
        self.assertNotEqual(self.new.updated_at, old_update)

    @unittest.skipIf(storage != "db", "Testing if using DBStorage")
    def test_basemodel_hasattr(self):
        '''
            Verifies the class attributes
        '''
        self.assertTrue(hasattr(self.new, "id"))
        self.assertTrue(hasattr(self.new, "created_at"))
        self.assertTrue(hasattr(self.new, "updated_at"))

    @unittest.skipIf(storage != "db", "Testing if using DBStorage")
    def test_basemodel_attrtype(self):
        '''
            Examine the characteristics type
        '''
        new2 = BaseModel
        self.assertFalse(isinstance(new2.id, str))
        self.assertFalse(isinstance(new2.created_at, str))
        self.assertFalse(isinstance(new2.updated_at, str))
