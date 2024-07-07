# data_storage.py

class DataStorage:
    def __init__(self):
        self.data = {}

    def add_data(self, key, value):
        self.data[key] = value

    def get_data(self):
        return self.data

    def clear_data(self):
        self.data = {}

# Singleton instance
data_storage_instance = DataStorage()
