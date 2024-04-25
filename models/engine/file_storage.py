#!/usr/bin/python3
"""
Module for managing file storage operations, utilizing JSON for
serialization and deserialization of instances.
"""
import json
import models


class FileStorage:
    """
    Handles the serialization and deserialization of instances
    to and from a JSON file specified by file_path.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if not cls:
            return self.__objects
        elif type(cls) == str:
            return {k: v for k, v in self.__objects.items()
                    if v.__class__.__name__ == cls}
        else:
            return {k: v for k, v in self.__objects.items()
                    if v.__class__ == cls}

    def new(self, obj):
        """
        Adds a new object to the storage, identified by its class name and ID.
        """
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """
        Updates the JSON file to reflect the current state
        of the objects in storage.
        """
        temp = {}
        for id, obj in self.__objects.items():
            temp[id] = obj.to_dict()
        with open(self.__file_path, "w") as json_file:
            json.dump(temp, json_file)

    def reload(self):
        """
        Restores previously saved objects from the JSON file into the storage.
        """
        try:
            with open(self.__file_path, "r") as json_file:
                temp = json.load(json_file)
            for id, dict in temp.items():
                temp_instance = models.dummy_classes[dict["__class__"]](**dict)
                self.__objects[id] = temp_instance
        except:
            pass

    def close(self):
        """
        Refreshes the storage by reloading objects from the JSON file.
        """
        self.reload()

    def delete(self, obj=None):
        """
        Removes an object from the storage if it exists;
        does nothing if obj is None.
        """
        if (obj):
            self.__objects.pop("{}.{}".format(type(obj).__name__, obj.id))
