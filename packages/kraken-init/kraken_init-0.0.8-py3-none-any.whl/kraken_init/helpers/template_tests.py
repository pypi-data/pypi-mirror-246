def get_filename(name):

    return f'{name}/tests/test_{name}.py'

def get_content(name):

    class_name = name.replace('kraken_', '')
    class_name = class_name.capitalize()

    content = f'''
from {name}.{name} import {class_name}

def test_init():
    """
    """

    i = {class_name}()

    property = 'test_property'
    value = 'test_value'

    expected_result = 'test_value'
    
    i.set(property, value)

    result = i.get(property)

    assert result == expected_result

    '''
    return content