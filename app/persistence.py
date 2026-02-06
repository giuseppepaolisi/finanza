import json
import os
from abc import ABC, abstractmethod

class StorageInterface(ABC):
    @abstractmethod
    def save(self, data):
        pass

    @abstractmethod
    def load(self):
        pass

class JSONStorage(StorageInterface):
    def __init__(self, filename="portfolio.json"):
        self.filename = filename

    def save(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load(self):
        if not os.path.exists(self.filename):
            return {}
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}