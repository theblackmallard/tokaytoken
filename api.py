# http://127.0.0.1:5000
import flask
from flask import request, redirect, url_for
import token_rpc
import json, re, time
import building


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "Komodod Tokens API Main Menu."


@app.route('/api/v1/test', methods=['GET'])
def api_test():
    return "Looks like the API is working correctly!"


@app.route('/api/v1/submit-form', methods=['POST'])
def api_submit():
    byte_test = len(request.form['data'].encode('utf-8'))
    coin_name = re.sub(r'[\W_]+', '', request.form['name'])
    coin_supply = int(request.form['supply'])
    coin_data = request.form['data']
    if byte_test < 10000:
        token = {
            "Name": coin_name,
            "Supply": coin_supply,
            "Data": coin_data }
        tokenJson = json.dumps(token)
        building.receive(tokenJson)
        return 'Building...'
    else:
        print('Data is {} bytes'.format(byte_test))
        return "Please shorten data"



app.run(host='0.0.0.0', debug=True, port=5000)
