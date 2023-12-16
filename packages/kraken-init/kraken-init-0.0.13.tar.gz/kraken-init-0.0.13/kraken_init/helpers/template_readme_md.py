

def get_filename(name):

    return f'README.md'


def get_content(name=None):
    """
    """
    content = f'''
    # {name}
    <definition>


    ## How to use

    ```
    from {name} import {name}

    

    ```


    
    '''
    return content