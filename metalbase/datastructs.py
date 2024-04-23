import os
import json


class DataBase:
    def __init__(self, filename):
        # Define self.filename and self.data. self.data will hold all the data within the json file
        self.filename = filename
        self.data = {}
        # Create json file if it doesn't already exist
        if not os.path.exists(filename):
            with open(filename, mode='w', encoding='utf-8') as new_json:
                json.dump({}, new_json, indent=4)
        # Load file's data into self.data if it does already exist
        else:
            with open(filename, mode='r', encoding='utf-8') as json_data:
                self.data = json.load(json_data)

    def create_entry(self, entry_id):
        """Adds a new dict at the root of the json database. The dict will have the key entry_id.

        :param entry_id: (str) the key you would like to assign to the entry.
        """
        # Load data from json file
        with open(self.filename, mode='r', encoding='utf-8') as f:
            json_data = json.load(f)

        # Create the new entry in the json data and in self.data
        json_data[entry_id] = {}
        self.data[entry_id] = {}

        # Save the data (with the change) to the json file. self.data has already been changed
        with open(self.filename, mode='w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4)

    def add(self, entry_id, *args, **kwargs):
        """Adds a new dict element to the dict at the specified location.
        Usage: Specify the id of the entry containing the dict being added to, then the positional arguments should
        form a path to the dict that will gain an element. The keyword arguments are the key/value pairs that will be
        added.
        Example: to add {'name': 'Clarisse', 'job': 'Magical girl'} to ["id319472632493768705"]["participants"]:
        add("319472632493768705", "participants", name='Clarisse', job='Magical girl')
        This change is made to both the json and self.data independently. self.data and the json file are otherwise
        unchanged. If any differences existed between self.data and the json, these are unaffected in either file.

        :param entry_id: (str) the key for the entry in that contains the dict that's being changed (including if
        the entry itself is the dict being changed)
        :param args: (tuple of strings) the arguments together constitute the path to the dict that is being added to.
        :param kwargs: (dict) the entries that are being added to the dict in question.
        """
        # Load data from json file
        with open(self.filename, mode='r', encoding='utf-8') as f:
            json_data = json.load(f)

        # Create views for the json file's data and self.data, then move them to the target dict
        view_for_file = json_data[entry_id]
        view_for_attr = self.data[entry_id]
        for path_element in args:
            view_for_file = view_for_file[path_element]
            view_for_attr = view_for_attr[path_element]

        # Merge the kwargs into the views, effectively adding them to the originals (json_data and self.data), too
        view_for_file.update(kwargs)
        view_for_attr.update(kwargs)

        # Save the data (with the change) to the json file. self.data is changed automatically
        with open(self.filename, mode='w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4)

    def save(self, status=False):
        """Saves the data in self.data to the database's json file, replacing all data in the file."""
        with open(self.filename, mode='w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)



