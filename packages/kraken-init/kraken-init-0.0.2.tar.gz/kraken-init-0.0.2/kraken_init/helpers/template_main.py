

def get_filename(name):

    return f'main.py'


def get_content(name):
    """
    """

    class_name = name.replace('kraken_', '')
    class_name = class_name.capitalize()
    git_name = name.replace('_', '')

    
    content = f'''
import os
from {name}.{name} import {class_name}

"""
Project structure created by kraken_init

To dos
1. Configure pypi package publishing
- Todo: Configure github pypi publish action - DONE 
- Todo: Create pypi token (https://pypi.org/manage/account/)
- Todo: Add pypi api token to github secret (https://github.com/tactik8/{git_name}/settings/secrets/actions)

2. Configure google cloud
- Todo: Create new cloud run service (https://console.cloud.google.com/run?project=kraken-v2-369412)

3. Add packages 
- Todo: Add required packages to setup.py
- Todo: Add required packages to requirements.txt
"""

def test():
    """Perform tests
    """
    os.system("pip install pytest")
    os.system("python -m pytest {name}* -vv")


test()




    '''
    return content