from flask import Flask
from flask_sslify import SSLify
from flask import request
import logging
from bot import processing_message, processing_callback_query



app = Flask(__name__)
sslify = SSLify(app)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        request_json = request.get_json()
        if request_json.get('message'):

            processing_message(request_json)

        elif request_json.get('callback_query'):

            processing_callback_query(request_json)
        return 'OK', 200

    elif request.method == 'GET':
        return 'OK', 200


if __name__ == '__main__':
    app.run()