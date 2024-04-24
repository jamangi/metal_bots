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

    def save(self):
        """Saves the data in self.data to the database's json file, replacing all data in the file."""
        with open(self.filename, mode='w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)

    def find_entries_where_nested(self, *args, all_in_one=False, **kwargs):
        """

        Example:
        --- Testdb.data
        {'e1': {'subentry': {'instrument': 'flute', 'food': 'tacos'}, 'name': 'Monica', 'id': 1},
         'e2': {},
         'e3': {'sub1': {'instrument': 'flute'}, 'sub2': {'food': 'tacos'}}}
        --- Testdb.Testdb.find_entries_where_nested(instrument='flute', food='tacos')
        ['e1', 'e3']
        --- Testdb.find_entries_where_nested(all_in_one=True, instrument='flute', food='tacos')
        ['e1']

        :param args: (tuple of strings) the arguments together constitute the path to the dict that holds the
        nested dicts that are being searched through.
        :param all_in_one: (
        :param kwargs: (dict) each kwarg represents a key/value pair that is being checked for. If all these key/value
        pairs are present inside at least one dictionary nested inside the dictionary specified by the args, the entry
        they're in will be part of the returned list.
        :return: (list) the list of entries that contain the key/value pairs specified in the kwargs at the location
        specified by the args.
        """
        entries_list = []
        for entry_id in self.data:
            # Create a view for self.data at the specified dictionary
            dict_view = self.data[entry_id]
            for path_element in args:
                dict_view = dict_view[path_element]

            # If all key/value pairs specified need to be in the same dict, then the search is simple
            if all_in_one:
                for nested_dict_key in dict_view:
                    if isinstance(dict_view[nested_dict_key], dict):
                        if all(target_key in dict_view[nested_dict_key] for target_key in kwargs):
                            if all(dict_view[nested_dict_key][target_key] == target_value
                                   for target_key, target_value in kwargs.items()):
                                entries_list.append(entry_id)
                                break
            else:
                # Go from subdict to subdict searching for the specified key/value pairs. As each is found, it's removed
                # from pairs_to_find. If pairs_to_find is empty, we know the entry qualifies so it's appended to the list
                pairs_to_find = kwargs.copy()  # A copy of kwargs where we can cross out any key/value pairs we've found
                for nested_dict_key in dict_view:
                    if not pairs_to_find:
                        break
                    for target_key, target_value in kwargs.items():
                        if isinstance(dict_view[nested_dict_key], dict):
                            if target_key in dict_view[nested_dict_key]:
                                if dict_view[nested_dict_key][target_key] == target_value:
                                    del pairs_to_find[target_key]
                                    if not pairs_to_find:
                                        entries_list.append(entry_id)
                                        break


        return entries_list


if __name__ == "__main__":
    Testdb = DataBase('test.json')
    Testdb.create_entry('e1')
    Testdb.create_entry('e2')
    Testdb.create_entry('e3')
    Testdb.add('e1', subentry={}, name='Monica', id=1)
    Testdb.add('e1', 'subentry', instrument='flute', food='tacos')
    Testdb.add('e3', sub1={}, sub2={})
    Testdb.add('e3', 'sub1', instrument='flute')
    Testdb.add('e3', 'sub2', food='tacos')
    print(Testdb.find_entries_where_nested(all_in_one=True, instrument='flute', food='tacos'))
    print(Testdb.data)