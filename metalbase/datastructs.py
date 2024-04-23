import os


class DataBase:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}
        if not os.path.exists(filename):
            with open(filename, mode='w', encoding='utf-8'):
                pass
        # will load from file


    def create_entry(self, entry_id):
        self.data[entry_id] = {}

    def add(self, entry_id, *args, **kwargs):
        pass