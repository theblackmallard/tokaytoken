import platform
import os, json, re
from slickrpc import Proxy


# function to define rpc_connection
def def_credentials(chain):
    rpcport = ''
    operating_system = platform.system()
    if operating_system == 'Darwin':
        ac_dir = os.environ['HOME'] + '/Library/Application Support/Komodo'
    elif operating_system == 'Linux':
        ac_dir = os.environ['HOME'] + '/.komodo'
    elif operating_system == 'Windows':
        ac_dir = '{}s/komodo/'.format(os.environ['APPDATA'])
    if chain == 'KMD':
        coin_config_file = str(ac_dir + '/komodo.conf')
    else:
        coin_config_file = str(ac_dir + '/' + chain + '/' + chain + '.conf')
    with open(coin_config_file, 'r') as f:
        for line in f:
            l = line.rstrip()
            if re.search('rpcuser', l):
                rpcuser = l.replace('rpcuser=', '')
            elif re.search('rpcpassword', l):
                rpcpassword = l.replace('rpcpassword=', '')
            elif re.search('rpcport', l):
                rpcport = l.replace('rpcport=', '')
    if len(rpcport) == 0:
        if chain == 'KMD':
            rpcport = 7771
        else:
            print("rpcport not in conf file, exiting")
            print("check " + coin_config_file)
            exit(1)

    return (Proxy("http://{0}:{1}@127.0.0.1:{2}".format(rpcuser, rpcpassword, int(rpcport))))

# Setting chain to RICK, has tokenCC and is test chain
rpc = def_credentials("RICK")

# sets pubkey for the daemon
def setpubkey(rpc_connection, pubkey):
    pubKey = rpc_connection.setpubkey(pubkey)
    return pubKey

# generates a new address and validates the address, returns pubkey and address
def genaddress(rpc_connection):
    address = rpc_connection.getnewaddress()
    validateaddress_result = rpc_connection.validateaddress(address)
    pubKey = validateaddress_result['pubkey']
    address = validateaddress_result['address']
    return pubKey, address

# The tokenList method lists all available tokens on the asset chain.
def tokenList(rpc_connection):
    tokens = rpc_connection.tokenlist()
    return tokens

def tokenAddress(rpc_connection, pubkey):
    results = rpc_connection.tokenaddress(pubkey)
    return results

# The tokenCreate method creates a new token.
def tokenCreate(rpc_connection, name, supply, data):
    result = rpc_connection.tokencreate(name, supply, data)
    rawhex = result['hex']
    tokenid = rpc_connection.sendrawtransaction(rawhex)
    return tokenid

# The tokenInfo method reveals information about any token.
def tokenInfo(rpc_connection, tokenid):
    result = rpc_connection.tokeninfo(tokenid)
    return result

# The tokenBalance method checks the token balance according to a provided pubkey
def tokenBalance(rpc_connection, tokenid):
    result = rpc_connection.tokenbalance(tokenid)
    return result

# The tokentransfer method transfers tokens from one Antara Address to another.
def tokenTransfer(rpc_connection, tokenid, destpubkey, amount):
    #amount = amount - 0.0001   # not sure if fee calculated needed?
    ready = rpc_connection.tokentransfer(tokenid, destpubkey, amount)
    rawhex = ready['hex']
    result = rpc_connection.sendrawtransaction(rawhex)
    return result

# The tokenOrders method displays the public on-chain orderbook for all tokens
def tokenOrdersGlobal(rpc_connection):
    result = rpc_connection.tokenorders()
    return result

# The tokenOrders method displays the public on-chain orderbook for a specific token.
# Information about the funcid property:
# A lowercase b describes an bid offer.
# An uppercase B describes a bid fill.
# A lowercase s describes an ask offer.
# An uppercase S describes the ask fill.

def tokenOrders(rpc_connection, tokenid):
    result = rpc_connection.tokenorders(tokenid)
    return result

# needs pubkey set in params
def MytokenOrders(rpc_connection):
    result = rpc_connection.mytokenorders()
    return result

# SELLING
# numtokens is number of tokens to ask, price is price per token
def tokenAsk(rpc_connection, numtokens, tokenid, price):
    ready = rpc_connection.tokenask(numtokens, tokenid, price)
    rawhex = ready['hex']
    result = rpc_connection.sendrawtransaction(rawhex)
    return result

# BUYING
# numtokens is number of tokens to bid, price is price per token
def tokenBid(rpc_connection, numtokens, tokenid, price):
    ready = rpc_connection.tokenbid(numtokens, tokenid, price)
    rawhex = ready['hex']
    result = rpc_connection.sendrawtransaction(rawhex)
    return result

# asktxid is the txid returned from tokenAsk
def tokenCancelAsk(rpc_connection, tokenid, asktxid):
    ready = rpc_connection.tokencancelask(tokenid, asktxid)
    rawhex = ready['hex']
    result = rpc_connection.sendrawtransaction(rawhex)
    return result

# bidtxid is the txid returned from tokenBid
def tokenCancelBid(rpc_connection, tokenid, bidtxid):
    ready = rpc_connection.tokencancelask(tokenid, bidtxid)
    rawhex = ready['hex']
    result = rpc_connection.sendrawtransaction(rawhex)
    return result

# The tokenFillAsk method fills an existing ask.
def tokenFillAsk(rpc_connection, tokenid, askid, fillamount):
    ready = rpc_connection.tokenfillask(tokenid, askid, fillamount)
    rawhex = ready['hex']
    result = rpc_connection.sendrawtransaction(rawhex)
    return result

# The tokenFillBid method fills an existing bid.
def tokenFillBid(rpc_connection, tokenid, bidid, fillamount):
    ready = rpc_connection.tokenfillask(tokenid, bidid, fillamount)
    rawhex = ready['hex']
    result = rpc_connection.sendrawtransaction(rawhex)
    return result

