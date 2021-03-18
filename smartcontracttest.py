import json
from web3 import Web3
from web3.middleware import geth_poa_middleware

geth_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(geth_url))
web3.eth.defaultAccount = web3.eth.accounts[0]
# abi = json.loads('[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"objectCode","type":"string"},{"indexed":false,"internalType":"bytes32","name":"objId","type":"bytes32"}],"name":"OrganizationCreated","type":"event"},{"inputs":[{"internalType":"string","name":"_code","type":"string"},{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_organization_address","type":"string"}],"name":"createOrganization","outputs":[{"internalType":"bytes32","name":"objId","type":"bytes32"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getInfo","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"objId","type":"bytes32"}],"name":"getOrganizationById","outputs":[{"internalType":"bytes32","name":"id","type":"bytes32"},{"internalType":"string","name":"code","type":"string"},{"internalType":"string","name":"ame","type":"string"},{"internalType":"string","name":"organization_address","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"organizationIds","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"organizationMap","outputs":[{"internalType":"bytes32","name":"objId","type":"bytes32"},{"internalType":"string","name":"code","type":"string"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"organization_address","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_info","type":"string"}],"name":"setInfo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"testId","outputs":[{"internalType":"bytes32","name":"objId","type":"bytes32"}],"stateMutability":"payable","type":"function"}]')
# address = web3.toChecksumAddress('0xb5952Bc0fa0517539A7F17ef304c8A875fB18f2B') # FILL IN YOUR ACTUAL ADDRESS


PATH_TRUFFLE_WK = 'D:\GitHub\supplychain_blockchain\\tat_api\\flasksvr\src\shared\contracts'
truffleFile = json.load(open(PATH_TRUFFLE_WK + '\OrganizationType.json'))
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']
address = web3.toChecksumAddress('0xF89174D477A81a6A2c581e46a98B056AE69e1248') # FILL IN YOUR ACTUAL ADDRESS

contract = web3.eth.contract(address=address, abi=abi)

web3.middleware_onion.inject(geth_poa_middleware, layer=0)

tx_hash = contract.functions.createOrganizationType('Farm','{phone:0192563019}').transact()

receipt =web3.eth.waitForTransactionReceipt(tx_hash)
logs = contract.events.OrganizationTypeCreated().processReceipt(receipt)

returnObj = logs[0]['args']['objId'];

print(Web3.toHex(returnObj) )

print('Updated contract info: {}'.format(
    contract.functions.getOrganizationTypeById(Web3.toHex(returnObj)).call()
))

print('contract List: {}'.format(
    contract.functions.getOrganizationTypeById(Web3.toHex(returnObj)).call()
))


# print('Is Connected {}'.format(web3.isConnected()))
# print('Client Version {}'.format(web3.clientVersion))

# print('Previous contract info: {}'.format(
#     contract.functions.getInfo().call()
# ))
# # Set info
# tx_hash = contract.functions.setInfo('HEELLLLOOOOOO!!!').transact()
# # Wait for transaction to be mined
# web3.eth.waitForTransactionReceipt(tx_hash)
# # Display the new greeting value
# print('Updated contract info: {}'.format(
#     contract.functions.getInfo().call()
# ))