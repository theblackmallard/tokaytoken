import requests
import token_rpc
import time

# price to charge (in USD)
price = 7.77
# time limit for payments
time_limit = 60 * 15

# Needs better handling of different scenarios
def check_address(address, amount, tokenJson):
    start = time.time()
    while time.time() < start + time_limit:
        response = requests.get("https://kmdexplorer.io/insight-api-komodo/addr/{}".format(address))
        if response.status_code == 200:
            data = response.json()
            balance = data['balance']
            if balance >= amount:
                build(tokenJson)
                break
            else:
                time.sleep(30)
        else:
            time.sleep(30)
            print('error code {}, will keep trying'.format(response.status_code))

# generates new address and calculates the price
def receive(tokenJson):
    pubkey, address = token_rpc.genaddress(token_rpc.rpc)
    try:
        value = requests.get("https://api.coinpaprika.com/v1/tickers/kmd-komodo").json()['quotes']['USD']['price']
        amount = price / value
        return "Please send {0} KMD to this address: {1}" \
               "within 15 minutes to finish creating your token".format(amount, address)
    except:
        print("need proper error handling")
    check_address(address, amount, tokenJson)

# actually builds the token
def build(tokenJson):
    name = tokenJson['Name']
    supply = tokenJson['Supply']
    data = tokenJson['Data']
    tokenid = token_rpc.tokencreate(token_rpc.rpc, name, supply, data)
    return tokenid
