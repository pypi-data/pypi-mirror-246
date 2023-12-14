

from flask import Flask
from flask import request
from flask import Response
from flask import redirect
from flask import url_for
from flask import jsonify
from kraken_etl.helpers import json

from kraken_etl.kraken_etl import Etl
from kraken_etl.kraken_etls import Etls

UPLOAD_FOLDER = '/path/to/the/uploads'

# Initialize flask app
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')
app.secret_key = b'_5#mn"F4Q8znxec]/'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/', methods=['GET', 'POST'])
def main_get():

    content = 'test'

    param1 = request.args.get('param1')

    data = None
    if request.content_type == 'application/json':
        data = request.get_json()

    thing = Thing()

    things = Things()

    return Response(content)

    return jsonify(record)


def run_api():
    app.run(host='0.0.0.0', debug=False)

#run_api()


    