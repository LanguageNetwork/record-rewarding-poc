import json

from eth_utils import to_checksum_address
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

# Solidity source code

# web3.py instance
# w3 = Web3(HTTPProvider('http://localhost:8545'))  # ganache or
w3 = Web3(HTTPProvider('https://ropsten.infura.io/'))

w3.middleware_stack.inject(geth_poa_middleware, layer=0)

# BasicToken abi
with open('build/contracts/BasicToken.json', 'r') as f:
    contract_meta_json = json.loads(f.read())
    contract_abi = contract_meta_json['abi']
    contract_bin = contract_meta_json['bytecode']

contract_address = to_checksum_address('0xFb294910d8193DeB9a294B51F22D8878ad15f2E8')
account_address = to_checksum_address('0xa37288ca4E6562045b66fD9482C68a22F3caA6b3')

private_key = 'd023453ce76a4b3308a5ca755d9b044feb2f0403809d09357d43d6cf5a9598bc'
nonce = w3.eth.getTransactionCount(account_address)
print("Nonce: ", nonce)

contract = w3.eth.contract(abi=contract_abi, address=contract_address)
func_obj = contract.functions.giveToken("0xa37288ca4E6562045b66fD9482C68a22F3caA6b3", 100)
txn = func_obj.buildTransaction({'nonce': nonce})
signed = w3.eth.account.signTransaction(txn, private_key=private_key)
txn_hash = w3.eth.sendRawTransaction(signed.rawTransaction)

print("Transaction: ", txn_hash.hex())


print()
