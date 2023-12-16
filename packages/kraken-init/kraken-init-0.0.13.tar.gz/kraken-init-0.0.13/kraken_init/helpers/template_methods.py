


def get_filename(name):

    return f'{name}/{name}.py'

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

"""
Notes:
To access files in data directory, use:
new_path = pkg_resources.resource_filename('{name}', old_path)

"""

        
def method1():
    """
    """
    
    return True


def method2():
    """
    """
    
    return True



        

    '''
    
    return content
    