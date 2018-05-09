import json
import time

from eth_utils import to_checksum_address
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
from web3.middleware import geth_poa_middleware

# Solidity source code

# web3.py instance
# w3 = Web3(HTTPProvider('http://localhost:8545'))  # ganache or
w3 = Web3(HTTPProvider('https://ropsten.infura.io/NiFrWVGDUTero8xrCJF8'))


w3.middleware_stack.inject(geth_poa_middleware, layer=0)

# BasicToken abi
with open('build/contracts/BasicToken.json', 'r') as f:
    contract_meta_json = json.loads(f.read())
    contract_abi = contract_meta_json['abi']
    contract_bin = contract_meta_json['bytecode']

contract = w3.eth.contract(abi=contract_abi, bytecode=contract_bin)

# # Get contract address
# tx_hash = contract.deploy(transaction={'from': '0x8F8d1bc97E8939e3932BfBeb923A1B2B972D5A9A', 'gas': 41000})
#
# while True:
#     tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
#     if tx_receipt is not None:
#         break
#     else:
#         time.sleep(1)
#         print("Wait...")
#
# contract_address = tx_receipt['contractAddress']

# or you can use a fixed address of contract
#
# $ NETWORK=dev
# $ TOKEN_NAME=BasicToken
# Use `$ truffle migrate --network $NETWORK --reset | grep "$TOKEN_NAME: 0x" | awk '{print $2}'`
#

from eth_utils import to_checksum_address
contract_address = to_checksum_address('0xFb294910d8193DeB9a294B51F22D8878ad15f2E8')

# Instantiate and deploy contract
contract_instance = w3.eth.contract(abi=contract_abi, address=contract_address, ContractFactoryClass=ConciseContract)

account_a = "0xCa2d22Cb8ff54f2D1DCfDBb75DD6411a5A0ee6f1"
account_b = "0x8F8d1bc97E8939e3932BfBeb923A1B2B972D5A9A"

# Unlock account
w3.personal.unlockAccount(account_a, input("Password: "))

print("Contract: {}".format(contract_address))

print("Before give token")
print('My Balance: {}'.format(contract_instance.myBalance()))
print('{} Balance: {}'.format(account_a, contract_instance.getBalance(account_a)))
print('{} Balance: {}'.format(account_b, contract_instance.getBalance(account_b)))

token_amount = 1000

contract_instance.giveToken(account_b, token_amount, transact={'from': account_a})

try:
    assert contract_instance.getBalance(account_b) == token_amount
except AssertionError as e:
    print("Test Error: {}".format(e))
    print("Amount: {}\t Expected: {}".format(contract_instance.getBalance(account_b), token_amount))

else:
    print("After give token")
    print('My Balance: {}'.format(contract_instance.myBalance()))
    print('{} Balance: {}'.format(account_a, contract_instance.getBalance(account_a)))
    print('{} Balance: {}'.format(account_b, contract_instance.getBalance(account_b)))

finally:
    print('Done')
