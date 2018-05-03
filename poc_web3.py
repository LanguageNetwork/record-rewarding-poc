import json
import time

from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
from web3.middleware import geth_poa_middleware

# Solidity source code

# web3.py instance
w3 = Web3(HTTPProvider('http://localhost:8545'))  # ganache or

w3.middleware_stack.inject(geth_poa_middleware, layer=0)

# BasicToken abi
with open('build/contracts/BasicToken.json', 'r') as f:
    contract_meta_json = json.loads(f.read())
    contract_abi = contract_meta_json['abi']
    contract_bin = contract_meta_json['bytecode']

contract = w3.eth.contract(abi=contract_abi, bytecode=contract_bin)

# Get contract address
tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[0], 'gas': 410000})

while True:
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    if tx_receipt is not None:
        break
    else:
        time.sleep(1)
        print("Wait...")

contract_address = tx_receipt['contractAddress']

# or you can use a fixed address of contract

# $ NETWORK=dev
# $ TOKEN_NAME=BasicToken
# Use `$ truffle migrate --network $NETWORK --reset | grep "$TOKEN_NAME: 0x" | awk '{print $2}'`


# from eth_utils import to_checksum_address
# contract_address = to_checksum_address('0xaccfca461819407de89a19aec6e622df7e1040ea')


# Instantiate and deploy contract
contract_instance = w3.eth.contract(abi=contract_abi, address=contract_address, ContractFactoryClass=ConciseContract)


print("Contract: {}".format(contract_address))

print("Before give token")
print('My Balance: {}'.format(contract_instance.myBalance()))
print('{} Balance: {}'.format(w3.eth.accounts[0], contract_instance.getBalance(w3.eth.accounts[0])))
print('{} Balance: {}'.format(w3.eth.accounts[1], contract_instance.getBalance(w3.eth.accounts[1])))

token_amount = 1000

contract_instance.giveToken(w3.eth.accounts[1], token_amount, transact={'from': w3.eth.accounts[0]})

try:
    assert contract_instance.getBalance(w3.eth.accounts[1]) == token_amount
except AssertionError as e:
    print("Test Error: {}".format(e))
    print("Amount: {}\t Expected: {}".format(contract_instance.getBalance(w3.eth.accounts[1]), token_amount))

else:
    print("After give token")
    print('My Balance: {}'.format(contract_instance.myBalance()))
    print('{} Balance: {}'.format(w3.eth.accounts[0], contract_instance.getBalance(w3.eth.accounts[0])))
    print('{} Balance: {}'.format(w3.eth.accounts[1], contract_instance.getBalance(w3.eth.accounts[1])))

finally:
    print('Done')
