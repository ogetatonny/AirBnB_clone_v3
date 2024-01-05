#!/usr/bin/python3
'''
    The file_storage module is being tested.
'''

import os
import time
import json
import unittest
import models
from models import storage
from models.base_model import BaseModel
from models.state import State
<<<<<<< HEAD
from models.user import User
import json
import os
import pep8
import unittest
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get(self):
        """ Tests method to get instance file storage"""
        storage = FileStorage()
        dic = {"name": "Vecindad"}
        instance = State(**dic)
        storage.new(instance)
        storage.save()
        storage = FileStorage()
        get_instance = storage.get(State, instance.id)
        self.assertEqual(get_instance, instance)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count(self):
        """ Tests count method file storage """
        storage = FileStorage()
        dic = {"name": "Vecindad"}
        state = State(**dic)
        storage.new(state)
        dic = {"name": "Mexico"}
        city = City(**dic)
        storag.new(city)
        storage.save()
        c = storage.count()
        self.assertEqual(len(storage.all()), c)
=======
from models.engine.file_storage import FileStorage

db = os.getenv("HBNB_TYPE_STORAGE")


@unittest.skipIf(db == 'db', "Testing DBstorage only")
class testFileStorage(unittest.TestCase):
    '''
        Putting the FileStorage class to the test.
    '''

    def setUp(self):
        '''
            Class initialization
        '''
        self.storage = FileStorage()
        self.my_model = BaseModel()

    def tearDown(self):
        '''
            Cleaning is being done.
        '''

        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_all_return_type(self):
        '''
            Validates data type of all method and return value.
        '''
        storage_all = self.storage.all()
        self.assertIsInstance(storage_all, dict)

    def test_new_method(self):
        '''
            Sets correct key and pair in FileStorage.__object attribute.
        '''
        self.storage.new(self.my_model)
        key = str(self.my_model.__class__.__name__ + "." + self.my_model.id)
        self.assertTrue(key in self.storage._FileStorage__objects)

    def test_objects_value_type(self):
        '''
            Value stored in FileStorage.__object is obj.__class__.__name__.
        '''
        self.storage.new(self.my_model)
        key = str(self.my_model.__class__.__name__ + "." + self.my_model.id)
        val = self.storage._FileStorage__objects[key]
        self.assertIsInstance(self.my_model, type(val))

    def test_save_file_exists(self):
        '''
            Ensures that a file with the name file is created.json
        '''
        self.storage.save()
        self.assertTrue(os.path.isfile("file.json"))

    def test_save_file_read(self):
        '''
            Examining contents of files contained within the file.json
        '''
        self.storage.save()
        self.storage.new(self.my_model)

        with open("file.json", encoding="UTF8") as fd:
            content = json.load(fd)

        self.assertTrue(type(content) is dict)

    def test_the_type_file_content(self):
        '''
            Examining the kind of information contained in the file.
        '''
        self.storage.save()
        self.storage.new(self.my_model)

        with open("file.json", encoding="UTF8") as fd:
            content = fd.read()

        self.assertIsInstance(content, str)

    def test_reaload_without_file(self):
        '''
            Nothing occurs upon file.JSON is not present.
        '''

        try:
            self.storage.reload()
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_delete(self):
        '''
            Test the remove technique.
        '''
        fs = FileStorage()
        new_state = State()
        fs.new(new_state)
        state_id = new_state.id
        fs.save()
        fs.delete(new_state)
        with open("file.json", encoding="UTF-8") as fd:
            state_dict = json.load(fd)
        for k, v in state_dict.items():
            self.assertFalse(state_id == k.split('.')[1])

    def test_model_storage(self):
        '''
            Check the Filestorage tests State Model
        '''
        self.assertTrue(isinstance(storage, FileStorage))

    def test_get(self):
        '''
            Check that method returns the requested object.
        '''
        new_state = State(name="NewYork")
        storage.new(new_state)
        key = "State.{}".format(new_state.id)
        result = storage.get("State", new_state.id)
        self.assertTrue(result.id, new_state.id)
        self.assertIsInstance(result, State)

    def test_count(self):
        '''
            Verify that count method yields number of items.
        '''
        old_count = storage.count("State")
        new_state1 = State(name="NewYork")
        storage.new(new_state1)
        new_state2 = State(name="Virginia")
        storage.new(new_state2)
        new_state3 = State(name="California")
        storage.new(new_state3)
        self.assertEqual(old_count + 3, storage.count("State"))
>>>>>>> 32f971af754391d0ddcb1a44afeabc3364a8eed4
