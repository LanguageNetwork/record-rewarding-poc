import os
import json
import logging
from tempfile import NamedTemporaryFile

import ipfsapi
from eth_utils import to_checksum_address
from flask import Flask, render_template, request
from web3 import HTTPProvider, Web3
from web3.contract import ConciseContract
from web3.exceptions import ValidationError
from web3.middleware import geth_poa_middleware

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
BUILD_PATH = os.path.join(PROJECT_PATH, '../', 'build')

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Change according to your ipfs node setting
try:
    api = ipfsapi.connect('localhost', 5001)
except ipfsapi.exceptions.ConnectionError:
    print("Error: No running ipfs daemon on localhost:5001")
    exit()

logger = app.logger
logger.setLevel(logging.DEBUG)

# Web3py
w3 = Web3(HTTPProvider('https://ropsten.infura.io/'))

w3.middleware_stack.inject(geth_poa_middleware, layer=0)

# BasicToken abi
with open(os.path.join(BUILD_PATH, 'contracts/BasicToken.json'), 'r') as f:
    contract_meta_json = json.loads(f.read())
    contract_abi = contract_meta_json['abi']

# Contract address in ropsten
contract_address = to_checksum_address('0xb5c06482224aeeab84adcbe79574efe135feb4bd')

# Owner address in ropsten
account_address = to_checksum_address('0xa37288ca4E6562045b66fD9482C68a22F3caA6b3')

# private key
private_key = 'd023453ce76a4b3308a5ca755d9b044feb2f0403809d09357d43d6cf5a9598bc'

# Contract obj
contract = w3.eth.contract(abi=contract_abi, address=contract_address)
concise_contract = w3.eth.contract(abi=contract_abi, address=contract_address, ContractFactoryClass=ConciseContract)


@app.route('/')
def index():
    return render_template('index.html')


def validate_voice(voice):
    # Add voice validation with zeroth
    return True


def make_url_html(url):
    return "<a href={}>{}</a>".format(url, url)


def get_balance(wallet_address):
    if wallet_address == 'undefined':
        return 0
    return concise_contract.getBalance(to_checksum_address(wallet_address))


def give_token(wallet_address):
    if wallet_address == 'undefined':
        return None
    func_obj = contract.functions.giveToken(to_checksum_address(wallet_address), 100)
    txn = func_obj.buildTransaction({'nonce': w3.eth.getTransactionCount(account_address)})
    signed = w3.eth.account.signTransaction(txn, private_key=private_key)
    return w3.eth.sendRawTransaction(signed.rawTransaction)


@app.route('/get_token')
def get_token():
    try:
        return get_token(request.args['wallet'])
    except ValidationError:
        return None


@app.route('/balance')
def balance():
    try:
        return str(get_balance(request.args['wallet']))
    except ValidationError:
        return "0"


@app.route('/upload', methods=['POST'])
def upload():
    name = NamedTemporaryFile(delete=False).name
    logger.info("Saved: {}".format(name))
    request.files['voice_file'].save(name)

    # Validate_voice
    if validate_voice(name):  # Validated
        # earn token
        txn_hash = give_token(request.form['wallet_addr'])

    else:  # Failed
        # ignore
        return "Voice wasn't validated"

    # Upload voice
    hash_value = api.add(name)['Hash']

    local_url = "http://localhost:8080/ipfs/{}".format(hash_value)
    ipfsio_url = "https://ipfs.io/ipfs/{}".format(hash_value)

    return "<br>".join([
        make_url_html(local_url),
        make_url_html(ipfsio_url),
        make_url_html('https://ropsten.etherscan.io/tx/{}'.format(txn_hash.hex()))
    ])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
