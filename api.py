# http://127.0.0.1:5000
import flask
from flask import request, redirect, url_for
import token_rpc
import json, re, time
# import building


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "Komodod Tokens API Main Menu."


@app.route('/api/v1/test', methods=['GET'])
def api_test():
    return "Looks like the API is working correctly!"


# requests should appear as /orderbook?tokenid=<TOKENID>
@app.route('/api/v1/orderbook', methods=['GET'])
def api_orderbook():
    tokenid = request.args.get('tokenid')
    orderbook = token_rpc.tokenOrders(token_rpc.rpc, tokenid)
    Orderbook = json.dumps(orderbook)
    return Orderbook


# requests should appear as /tokeninfo?tokenid=<TOKENID>
@app.route('/api/v1/tokeninfo', methods=['GET'])
def api_tokeninfo():
    tokenid = request.args.get('tokenid')
    info = token_rpc.tokenInfo(token_rpc.rpc, tokenid)
    Info = json.dumps(info)
    return Info


@app.route('/api/v1/tokenlist', methods=['GET'])
def api_tokenlist():
    tokenlist = token_rpc.tokenList(token_rpc.rpc)
    TokenList = json.dumps(tokenlist)
    return TokenList


@app.route('/api/v1/blockcount', methods=['GET'])
def api_blockcount():
    blocks = token_rpc.getblockcount(token_rpc.rpc)
    Block = json.dumps(blocks)
    return Block


# Seems to be a bug in Komodod, orderbook without tokenID returns an error
# @app.route('/api/v1/globalorderbook', methods=['GET'])
# def api_globalorderbook():
#     orders = token_rpc.tokenOrdersGlobal(token_rpc.rpc)
#     return orders


# Don't use this yet, not working properly
# @app.route('/api/v1/submit-form', methods=['POST'])
# def api_submit():
#     byte_test = len(request.form['data'].encode('utf-8'))
#     coin_name = re.sub(r'[\W_]+', '', request.form['name'])
#     coin_supply = int(request.form['supply'])
#     coin_data = request.form['data']
#     if byte_test < 10000:
#         token = {
#             "Name": coin_name,
#             "Supply": coin_supply,
#             "Data": coin_data }
#         tokenJson = json.dumps(token)
#         building.receive(tokenJson)
#         return 'Building...'
#     else:
#         print('Data is {} bytes'.format(byte_test))
#         return "Please shorten data"



app.run(host='0.0.0.0', debug=True, port=5000)
