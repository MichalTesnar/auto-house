from os import listdir, makedirs, remove
from os.path import isfile, join
import json


class FileSaver():
    def __init__(self, name: str, profile):
        self.directory = f"secret/{profile.name}/data/{name}"
        makedirs(self.directory, exist_ok=True)
        self.available_files = [f for f in listdir(self.directory) if isfile(join(self.directory, f))]
        
    def has_been_contacted(self, name: str) -> bool:
        return f"{name}.json" in self.available_files
    
    def save_file(self, file_name: str, file_content: dict):
        with open(f"{self.directory}/{file_name}.json", "w") as json_file:
            json.dump(file_content, json_file)
            
    def load_edited_file_and_delete(self, file_name: str):
        with open(f"{self.directory}/{file_name}.json", "r") as json_file:
            file_content = json.load(json_file)
        remove(f"{self.directory}/{file_name}.json")
        return file_content
    
    def print_response(self, file_name: str) -> dict:
        with open(f"{self.directory}/{file_name}.json", "r") as json_file:
            return json.load(json_file)
