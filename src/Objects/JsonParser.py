import json
import os


class JsonParser:
    def __init__(self):
        self.filename = 'launch_settings.json'
        if self.filename in os.listdir("."):
            self.file_exists = True
        else:
            self.file_exists = False

    def export_to_json(self, segments, blur=10):
        keys = ["Segments", "Blur"]
        values = [segments, blur]
        dictionary = dict(zip(keys, values))
        with open(self.filename, 'w') as json_file:
            json.dump(dictionary, json_file)

    def import_from_json(self):
        with open(self.filename) as json_file:
            dictionary = json.load(json_file)
        return dictionary["Segments"], dictionary["Blur"]

    def delete_file(self):
        os.remove(self.filename)
