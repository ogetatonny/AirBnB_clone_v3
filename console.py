#!/usr/bin/python3
'''
    Constructing the HBnB project console.
'''
import cmd
import json
import shlex
import models
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    '''
        comprising the command interpreter entry point.
    '''
    prompt = ("(hbnb) ")

    def do_quit(self, args):
        '''
            To end the program use the Quit command.
        '''
        return True

    def do_EOF(self, args):
        '''
            Departs upon obtaining the EOF signal.
        '''
        return True

    def do_create(self, args):
        '''
            Make a fresh instance of the BaseModel class
            and store it in a JSON file.
        '''
        if len(args) == 0:
            print("** class name missing **")
            return
        try:
            args = shlex.split(args)
            new_instance = eval(args[0])()
            for i in args[1:]:
                try:
                    key = i.split("=")[0]
                    value = i.split("=")[1]
                    if hasattr(new_instance, key) is True:
                        value = value.replace("_", " ")
                        try:
                            value = eval(value)
                        except:
                            pass
                        setattr(new_instance, key, value)
                except (ValueError, IndexError):
                    pass
            new_instance.save()
            print(new_instance.id)
        except:
            print("** class doesn't exist **")
            return

    def do_show(self, args):
        '''
            With the class name and id provided as arguments, print
            the string representation of an instance of bead.
        '''
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        obj_dict = storage.all(args[0])
        try:
            eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return
        key = args[0] + "." + args[1]
        try:
            value = obj_dict[key]
            print(value)
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, args):
        '''
            Removes an instance by using its id and class name.
        '''
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return
        class_name = args[0]
        class_id = args[1]
        storage.reload()
        obj_dict = storage.all()
        try:
            eval(class_name)
        except NameError:
            print("** class doesn't exist **")
            return
        key = class_name + "." + class_id
        try:
            del obj_dict[key]
        except KeyError:
            print("** no instance found **")
        storage.save()

    def do_all(self, args):
        '''
            outputs every instance string representation
            whether or not the class name is specified.
        '''
        args = args.split(" ")
        obj_list = []
        objects = storage.all(args[0])
        try:
            if args[0] != "":
                models.classes[args[0]]
        except (KeyError, NameError):
            print("** class doesn't exist **")
            return
        try:
            for key, val in objects.items():
                obj_list.append(val)
        except:
            pass
        print(obj_list)

    def do_update(self, args):
        '''
            Using the class name and id supplied as arguments
            update an instance.
        '''
        storage.reload()
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return
        elif len(args) == 2:
            print("** attribute name missing **")
            return
        elif len(args) == 3:
            print("** value missing **")
            return
        try:
            eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return
        key = args[0] + "." + args[1]
        obj_dict = storage.all()
        try:
            obj_value = obj_dict[key]
        except KeyError:
            print("** no instance found **")
            return
        try:
            attr_type = type(getattr(obj_value, args[2]))
            args[3] = attr_type(args[3])
        except AttributeError:
            pass
        setattr(obj_value, args[2], args[3])
        obj_value.save()

    def emptyline(self):
        '''
            stops printing anything when a line is passed that is empty.
        '''
        pass

    def do_count(self, args):
        '''
            Determines or counts the quantity of occurrences.
        '''
        obj_list = []
        storage.reload()
        objects = storage.all()
        try:
            if len(args) != 0:
                eval(args)
        except NameError:
            print("** class doesn't exist **")
            return
        for key, val in objects.items():
            if len(args) != 0:
                if type(val) is eval(args):
                    obj_list.append(val)
            else:
                obj_list.append(val)
        print(len(obj_list))

    def default(self, args):
        '''
            captures all function names that arent stated explicitly.
        '''
        functions = {"all": self.do_all, "update": self.do_update,
                     "show": self.do_show, "count": self.do_count,
                     "destroy": self.do_destroy, "update": self.do_update}
        args = (args.replace("(", ".").replace(")", ".")
                .replace('"', "").replace(",", "").split("."))

        try:
            cmd_arg = args[0] + " " + args[2]
            func = functions[args[1]]
            func(cmd_arg)
        except:
            print("*** Unknown syntax:", args[0])

if __name__ == "__main__":
    '''
        Point of entry into the loop.
    '''
    HBNBCommand().cmdloop()
