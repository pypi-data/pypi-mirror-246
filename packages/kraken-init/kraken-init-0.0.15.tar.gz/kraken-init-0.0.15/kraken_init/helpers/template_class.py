


def get_filename(name):

    
    return f'{name}/Class_{name}.py'

def get_content(name):
    """
    """
    
    class_name = name.replace('kraken_', '')
    
    class_name = class_name.capitalize()

    record_value = {}
    content = f'''
    
import copy
from {name}.helpers import json
import os
import pkg_resources
from {name} import {name} as m

"""
Notes:
To access files in data directory, use:
new_path = pkg_resources.resource_filename('{name}', old_path)

"""
    
class {class_name}:
    """
    The Vehicle object contains a lot of vehicles

    Args:
        arg1 (str): The arg is used for...
        arg2 (str): The arg is used for...
        arg3 (str): The arg is used for...

    Attributes:
        record (dict): This is where we store attributes
        json (str): Record in json format
        
    """

    def __init__(self):
        self._record = {record_value}
        

    def __str__(self):
        """
        """
        return str(self._record)

    
    def __repr__(self):
        """
        """
        return str(self._record)

    
    def __eq__(self, other):
        """
        """
        if type(self) != type(other):
            return False
            
        if self._record == other._record:
            return True
        return False

    def __gt__(self, other):
        """
        """
        return True

        
    def set(self, property, value):
        """
        """
        self._record[property] = value
        return True

    
    def get(self, property):
        """
        """
        return self._record.get(property, None)

    
    def load(self, value):
        """
        """
        self._record = value
        return True


    def dump(self): 
        """
        """
        return copy.deepcopy(self._record)
        

    def set_json(self, value):
        """
        """
        record = json.loads(value)
        self.load(record)
        return True

    def get_json(self):
        """
        """
        return json.dumps(self.dump())

    @property
    def record(self):
        return self.dump()

    @record.setter
    def record(self, value):
        return self.load(value)
    
    @property
    def json(self):
        return self.get_json()

    @json.setter
    def json(self, value):
        return self.set_json(value)
        

    '''
    
    return content
    