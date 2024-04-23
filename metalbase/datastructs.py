import os
import json


class DataBase:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}
        # Create json file if it doesn't already exist
        if not os.path.exists(filename):
            with open(filename, mode='w', encoding='utf-8') as new_json:
                json.dump({}, new_json)
        # Load file's data into self.data if it does already exist
        else:
            with open(filename, mode='r', encoding='utf-8') as json_data:
                self.data = json_data



    def create_entry(self, entry_id):
        self.data[entry_id] = {}

    def add(self, entry_id, *args, **kwargs):
        pass