

def get_filename(name):

    return f'{name}/__init__.py'


def get_content(name=None):
    """
    """

    class_name = name.replace('kraken_', '')

    class_name = class_name.capitalize()
    class_name_collection = class_name + 's'


    
    content = f'''
from {name}.{name} import {class_name}
from {name}.{name + 's'} import {class_name_collection}
    '''
    return content