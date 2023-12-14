

def get_filename(name):

    return f'{name}/flask_routes.py'


def get_content(name=None):
    """
    """

    class_name = name.replace('kraken_', '')

    class_name = class_name.capitalize()
    class_name_collection = class_name + 's'


    
    content = f'''

from flask import Flask
from flask import request
from flask import Response
from flask import redirect
from flask import url_for
from flask import jsonify
from {name}.helpers import json

from {name}.{name} import {class_name}
from {name}.{name} import {class_name_collection}

UPLOAD_FOLDER = '/path/to/the/uploads'

# Initialize flask app
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')
app.secret_key = b'_5#mn"F4Q8z\n\xec]/'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def main_get():

    content = ''
    
    params = request.args.get('key)

    input_data = request.json()

    {class_name.lower()} = {class_name}()
    
    {class_name_collection.lower()} = {class_name_collection}()
    
    return Response(content)

    return jsonify(record)


def run_api():
    app.run(host='0.0.0.0', debug=False)

run_api()




    '''
    return content