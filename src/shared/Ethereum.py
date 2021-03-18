import os
import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
from .Encryptor import Encryptor
from datetime import datetime
from .QrGenerator import QrGenerator

geth_url = os.getenv('ETHEREUM_ENDPOINT_URI')
contract_path = os.getenv('ETHEREUM_CONTRACT_PATH')

abi_lib = {}
contract_address_lib = {}
for filename in os.listdir(contract_path):
    try:
        if filename.endswith('.json'):
            fullPath = os.path.join(contract_path, filename)
            with open(fullPath, 'r') as f:
                datastore = json.load(f)
                filenameNoExt = os.path.splitext(filename)[0]
                abi_lib[filenameNoExt] = datastore["abi"]
                contract_address_lib[filenameNoExt] = datastore["contract_address"]
                print('Load Contract Success', filenameNoExt)

    except Exception as e:
        print(e)


class Ethereum():
    @staticmethod
    def create_organization_type(name, custom):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'OrganizationTypeContract'

        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        tx_hash = contract.functions.create(name, custom).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Created().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def update_organization_type(id, name, custom):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'OrganizationTypeContract'

        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        tx_hash = contract.functions.update(id, name, custom, True).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Updated().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def get_organization_type(id):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'OrganizationTypeContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        objId, name, isActive, custom = contract.functions.getById(id).call()
        data = {
            'id': Web3.toHex(objId),
            'name': name,
            'custom': custom,
            'isActive': isActive
        }
        return data

    @staticmethod
    def delete_organization_type(id):
        print(id)
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'OrganizationTypeContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        tx_hash = contract.functions.activate(id, False).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Updated().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def get_organization_type_list():
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'OrganizationTypeContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        datas = contract.functions.getAll().call()
        dataInHex = []
        for data in datas:
            retObj = Ethereum.get_organization_type(Web3.toHex(data))
            if retObj['isActive']:
                dataInHex.append(retObj)
            # dataInHex.append(Web3.toHex(data))

        return dataInHex

# ORGANIZATION

    @staticmethod
    def create_organization(name, organizationTypeIdList, organizationAddress, custom):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'OrganizationContract'
        organizationTypeIdListInBytes = []
        for organizationTypeId in organizationTypeIdList:
            organizationTypeIdListInBytes.append(organizationTypeId["id"])

        # print(organizationTypeIdListInBytes)
        # return 'a'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        tx_hash = contract.functions.create(
            name, organizationTypeIdListInBytes, organizationAddress, custom).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Created().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def update_organization(id, name, organizationTypeIdList, organizationAddress, custom):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'OrganizationContract'

        organizationTypeIdListInBytes = []
        for organizationTypeId in organizationTypeIdList:
            organizationTypeIdListInBytes.append(organizationTypeId["id"])

        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        tx_hash = contract.functions.update(
            id, name, organizationTypeIdListInBytes, organizationAddress, custom, True).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Updated().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def get_organization(id):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'OrganizationContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        objId, name, organizationTypeIdList, organizationAddress, isActive, custom = contract.functions.getById(
            id).call()

        organizationType = []
        for data in organizationTypeIdList:
            orgTypeInfo = Ethereum.get_organization_type(Web3.toHex(data))
            organizationType.append(orgTypeInfo)

        data = {
            'id': Web3.toHex(objId),
            'name': name,
            'organizationTypeIdList': organizationType,
            'organizationAddress': organizationAddress,
            'custom': custom,
            'isActive': isActive
        }
        return data

    @staticmethod
    def delete_organization(id):
        print(id)
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'OrganizationContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        tx_hash = contract.functions.activate(id, False).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Updated().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def get_organization_list():
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'OrganizationContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        datas = contract.functions.getAll().call()
        dataInHex = []
        for data in datas:
            retObj = Ethereum.get_organization(Web3.toHex(data))
            if retObj['isActive']:
                dataInHex.append(retObj)
        # for data in datas:
        #     dataInHex.append(Web3.toHex(data))

        return dataInHex

# ACTIVITY

    @staticmethod
    def create_activity(name, organizationType, custom):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'ActivityContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        organizationTypeId = organizationType["id"]
        tx_hash = contract.functions.create(
            name, organizationTypeId, custom).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Created().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def update_activity(id, name, organizationType, custom):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'ActivityContract'

        organizationTypeId = organizationType["id"]

        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        tx_hash = contract.functions.update(
            id, name, organizationTypeId, custom, True).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Updated().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def get_activity(id):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'ActivityContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        objId, name, organizationTypeId, isActive, custom = contract.functions.getById(
            id).call()

        organizationType = Ethereum.get_organization_type(Web3.toHex(organizationTypeId))

        data = {
            'id': Web3.toHex(objId),
            'name': name,
            'organizationType': organizationType,
            'organizationType_name': organizationType['name'],
            'custom': custom,
            'isActive': isActive
        }
        return data

    @staticmethod
    def delete_activity(id):
        print(id)
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'ActivityContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        tx_hash = contract.functions.activate(id, False).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Updated().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def get_activity_list():
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'ActivityContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        datas = contract.functions.getAll().call()
        dataInHex = []
        for data in datas:
            retObj = Ethereum.get_activity(Web3.toHex(data))
            if retObj['isActive']:
                dataInHex.append(retObj)

        return dataInHex

    @staticmethod
    def get_activity_list_by_organization(id):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'ActivityContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        organization = Ethereum.get_organization(id);
        organizationTypeIdList = organization["organizationTypeIdList"]
        organizationTypeIds = []
        for data in organizationTypeIdList:
            organizationTypeIds.append(data['id'])

        datas = contract.functions.getAll().call()
        dataInHex = []
        for data in datas:
            retObj = Ethereum.get_activity(Web3.toHex(data))
            if retObj['isActive']:
                for organizationTypeId in organizationTypeIds:
                    if retObj["organizationType"]["id"] == organizationTypeId:
                        dataInHex.append(retObj)

        return dataInHex


# AREA

    @staticmethod
    def create_area(name, organization, custom):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'AreaContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        organizationId = organization["id"]
        tx_hash = contract.functions.create(
            name, organizationId, custom).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Created().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def update_area(id, name, organization, custom):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'AreaContract'

        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        organizationId = organization["id"]

        tx_hash = contract.functions.update(
            id, name, organizationId, custom, True).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Updated().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def get_area(id):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'AreaContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        objId, name, organizationId, isActive, custom = contract.functions.getById(
            id).call()

        organization = Ethereum.get_organization(Web3.toHex(organizationId))

        data = {
            'id': Web3.toHex(objId),
            'name': name,
            'organization': organization,
            'organization_name': organization["name"],
            'custom': custom,
            'isActive': isActive
        }
        return data

    @staticmethod
    def delete_area(id):
        print(id)
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'AreaContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        tx_hash = contract.functions.activate(id, False).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Updated().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def get_area_list():
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'AreaContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        datas = contract.functions.getAll().call()
        dataInHex = []
        for data in datas:
            retObj = Ethereum.get_area(Web3.toHex(data))
            if retObj['isActive']:
                dataInHex.append(retObj)

        return dataInHex

    @staticmethod
    def get_area_list_by_organization(id):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'AreaContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        datas = contract.functions.getAll().call()
        dataInHex = []
        for data in datas:
            retObj = Ethereum.get_area(Web3.toHex(data))
            if retObj['isActive']:
                if retObj['organization']['id'] == id: 
                    dataInHex.append(retObj)

        # datas = contract.functions.getAll().call()
        # dataInHex = []
        # for data in datas:
        #     retObj = Ethereum.get_profile(Web3.toHex(data))
        #     if retObj['isActive']:
        #         if retObj['organization']['id'] == id: 
        #             dataInHex.append(retObj)


        return dataInHex


# category

    @staticmethod
    def create_category(name, custom):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'CategoryContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        tx_hash = contract.functions.create(
            name,custom).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Created().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def update_category(id, name, custom):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'CategoryContract'

        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        tx_hash = contract.functions.update(
            id, name,  custom, True).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Updated().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def get_category(id):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'CategoryContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        objId, name, isActive, custom = contract.functions.getById(
            id).call()

        data = {
            'id': Web3.toHex(objId),
            'name': name,
            'custom': custom,
            'isActive': isActive
        }
        return data

    @staticmethod
    def delete_category(id):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'CategoryContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        tx_hash = contract.functions.activate(id, False).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Updated().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def get_category_list():
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'CategoryContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        datas = contract.functions.getAll().call()
        dataInHex = []
        for data in datas:
            retObj = Ethereum.get_category(Web3.toHex(data))
            if retObj['isActive']:
                dataInHex.append(retObj)

        return dataInHex


# certification

    @staticmethod
    def create_certification(name, certificateUrl, custom):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'CertificationContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        tx_hash = contract.functions.create(
            name,certificateUrl, custom).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Created().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def update_certification(id, name,certificateUrl, custom):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'CertificationContract'

        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        tx_hash = contract.functions.update(
            id, name, certificateUrl, custom, True).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Updated().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def get_certification(id):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'CertificationContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        objId, name, certificateUrl, isActive, custom = contract.functions.getById(
            id).call()

        data = {
            'id': Web3.toHex(objId),
            'name': name,
            'certificateUrl': certificateUrl,
            'custom': custom,
            'isActive': isActive
        }
        return data

    @staticmethod
    def delete_certification(id):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'CertificationContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        tx_hash = contract.functions.activate(id, False).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Updated().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def get_certification_list():
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'CertificationContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        datas = contract.functions.getAll().call()
        dataInHex = []
        for data in datas:
            retObj = Ethereum.get_certification(Web3.toHex(data))
            if retObj['isActive']:
                dataInHex.append(retObj)

        return dataInHex

# product

    @staticmethod
    def create_product(name, category, description,certificationList, custom):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'ProductContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        categoryId = category["id"]
        certificationIdListInBytes = []
        for certification in certificationList:
            certificationIdListInBytes.append(certification["id"])

        tx_hash = contract.functions.create(
            name,categoryId, description, certificationIdListInBytes, custom).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Created().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def update_product(id, name, category,description, certificationList, custom):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'ProductContract'
        categoryId = category["id"]
        certificationIdListInBytes = []
        for certification in certificationList:
            certificationIdListInBytes.append(certification["id"])

        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        tx_hash = contract.functions.update(
            id, name, categoryId, description, certificationIdListInBytes, custom, True).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Updated().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def get_product(id):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'ProductContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        objId, categoryId, name, description, certificationIdList, isActive, custom = contract.functions.getById(
            id).call()

        category = Ethereum.get_category(Web3.toHex(categoryId))

        certificationList = []
        for data in certificationIdList:
            certification = Ethereum.get_certification(Web3.toHex(data))
            certificationList.append(certification)

        data = {
            'id': Web3.toHex(objId),
            'name': name,
            'category' : category,
            'categoryName' : category['name'],
            'description' : description,
            'certificationList' : certificationList,
            'custom': custom,
            'isActive': isActive,
            'qrUrl' : QrGenerator.get_url(Web3.toHex(objId))
        }
        return data

    @staticmethod
    def delete_product(id):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'ProductContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        tx_hash = contract.functions.activate(id, False).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Updated().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def get_product_list():
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'ProductContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        datas = contract.functions.getAll().call()
        dataInHex = []
        for data in datas:
            retObj = Ethereum.get_product(Web3.toHex(data))
            if retObj['isActive']:
                dataInHex.append(retObj)

        return dataInHex

# profile

    @staticmethod
    def create_profile(name, email, password, phone, roleList, organization, custom):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'ProfileContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        organizationId = organization["id"]
        roleIdListInBytes = []
        for role in roleList:
            roleIdListInBytes.append(role["id"])
        passwordHash = Encryptor.encrypt(password)

        tx_hash = contract.functions.create(
            name, email, passwordHash, phone, roleIdListInBytes, organizationId, custom).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Created().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def update_profile(id, name, email,password, phone, roleList, organization, custom):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'ProfileContract'
        
        organizationId = organization["id"]
        roleIdListInBytes = []
        for role in roleList:
            roleIdListInBytes.append(role["id"])
        passwordHash = Encryptor.encrypt(password)

        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        tx_hash = contract.functions.update(
            id, name, email, passwordHash, phone, roleIdListInBytes, organizationId,custom,  True ).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Updated().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId


    @staticmethod
    def get_profile_by_email(email):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'ProfileContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        profileId = contract.functions.emailMap(email).call()
        profile = Ethereum.get_profile(profileId)

        return profile
        
    @staticmethod
    def get_profile(id):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'ProfileContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        objId, name, email, passwordHash, phone, roleIdList, organizationId, isActive, custom = contract.functions.getById(
            id).call()

        organization = Ethereum.get_organization(Web3.toHex(organizationId))

        roleList = []
        for data in roleIdList:
            role = Ethereum.get_role(Web3.toHex(data))
            roleList.append(role)
        password = Encryptor.decrypt(passwordHash)
        data = {
            'id': Web3.toHex(objId),
            'name': name,
            'email' : email,
            'password' : password,
            'phone' : phone,
            'roleList' : roleList,
            'organization' : organization,
            'custom': custom,
            'isActive': isActive
        }
        return data

    @staticmethod
    def delete_profile(id):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'ProfileContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        tx_hash = contract.functions.activate(id, False).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Updated().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def get_profile_list():
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'ProfileContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        datas = contract.functions.getAll().call()
        dataInHex = []
        for data in datas:
            retObj = Ethereum.get_profile(Web3.toHex(data))
            if retObj['isActive']:
                dataInHex.append(retObj)

        return dataInHex

    @staticmethod
    def get_profile_list_by_organization(id):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'ProfileContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        datas = contract.functions.getAll().call()
        dataInHex = []
        for data in datas:
            retObj = Ethereum.get_profile(Web3.toHex(data))
            if retObj['isActive']:
                if retObj['organization']['id'] == id: 
                    dataInHex.append(retObj)

        return dataInHex

# role

    @staticmethod
    def create_role(name, custom):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'RoleContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        tx_hash = contract.functions.create(name, custom).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Created().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def update_role(id, name, custom):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'RoleContract'
        

        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        tx_hash = contract.functions.update(
            id, name, custom, True).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Updated().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def get_role(id):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'RoleContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        objId, name, isActive, custom = contract.functions.getById(
            id).call()

        data = {
            'id': Web3.toHex(objId),
            'name': name,
            'custom': custom,
            'isActive': isActive
        }
        return data

    @staticmethod
    def delete_role(id):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'RoleContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        tx_hash = contract.functions.activate(id, False).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Updated().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    @staticmethod
    def get_role_list():
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'RoleContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        datas = contract.functions.getAll().call()
        dataInHex = []
        for data in datas:
            retObj = Ethereum.get_role(Web3.toHex(data))
            if retObj['isActive']:
                dataInHex.append(retObj)

        return dataInHex


# trail

    # @staticmethod
    # def create_trail(product, activity,  profile,  area, gps, remarks, custom):
    #     web3 = Web3(Web3.HTTPProvider(geth_url))
    #     web3.eth.defaultAccount = web3.eth.accounts[0]
    #     contractName = 'TrailInfoContract'
    #     contract = web3.eth.contract(
    #         address=contract_address_lib[contractName], abi=abi_lib[contractName])
    #     web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    #     productId = product["id"]
    #     activityId = activity["id"]
    #     profileId = profile["id"]
    #     areaId = area["id"]
    #     return areaId
    #     # tx_hash = contract.functions.addProductTrail( productId, activityId, profileId, areaId, gps, remarks, custom).transact()
    #     tx_hash = contract.functions.addProductTrail( 
    #         0x56ceec9805cac5fa712309bf1b049b1386911c300e5c5b387cefe9cb95610243, 
    #         0x56ceec9805cac5fa712309bf1b049b1386911c300e5c5b387cefe9cb95610243, 
    #         0x56ceec9805cac5fa712309bf1b049b1386911c300e5c5b387cefe9cb95610243, 
    #         0x56ceec9805cac5fa712309bf1b049b1386911c300e5c5b387cefe9cb95610243, "gps", "gps", "gps").transact()

    #     receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    #     logs = contract.events.Created().processReceipt(receipt)
    #     objId = Web3.toHex(logs[0]['args']['objId'])
    #     return objId

    @staticmethod
    def create_trail(product, activity,  profile,  area, gps, remarks, custom):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'TrailInfoContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        productId = product["id"]
        activityId = activity["id"]
        profileId = profile["id"]
        areaId = area["id"]

        tx_hash = contract.functions.addProductTrail(productId, activityId, profileId, areaId, gps, remarks, custom).transact()
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logs = contract.events.Created().processReceipt(receipt)
        objId = Web3.toHex(logs[0]['args']['objId'])
        return objId

    # @staticmethod
    # def update_trail(id, product, activity,  profile,  area, gps, remarks,  custom):
    #     web3 = Web3(Web3.HTTPProvider(geth_url))
    #     web3.eth.defaultAccount = web3.eth.accounts[0]
    #     contractName = 'TrailInfoContract'
        
    #     productId = product["id"]
    #     activityId = activity["id"]
    #     profileId = profile["id"]
    #     areaId = area["id"]

    #     contract = web3.eth.contract(
    #         address=contract_address_lib[contractName], abi=abi_lib[contractName])
    #     web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    #     tx_hash = contract.functions.update(
    #         id, productId, activityId, profileId, area, gps, remarks, custom, True).transact()
    #     receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    #     logs = contract.events.Updated().processReceipt(receipt)
    #     objId = Web3.toHex(logs[0]['args']['objId'])
    #     return objId

    @staticmethod
    def get_trail(productId, trailId):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'TrailInfoContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        pId, activityId, profileId, areaId, gps, remarks, isActive, custom, createdDate = contract.functions.getProductTrail(productId, trailId).call()

        product = Ethereum.get_product(productId)
        activity = Ethereum.get_activity(activityId)
        profile = Ethereum.get_profile(profileId)
        area = Ethereum.get_area(areaId)

        createdDateInText = datetime.fromtimestamp(createdDate).strftime('%Y-%m-%d %H:%M:%S')

        data = {
            'id': trailId,
            'product': product,
            'product_name' : product['name'],
            'activity' : activity,
            'activity_name' : activity['name'],
            'profile' : profile,
            'organization': profile['organization'],
            'organization_name': profile['organization']['name'],
            'area' : area,
            'area_name' : area['name'],
            'gps' : gps,
            'remarks' : remarks,
            'custom': custom,
            'isActive': isActive,
            'createdDate': createdDate,
            'createdDateInText': createdDateInText
        }
        return data

    @staticmethod
    def get_product_trail(id):
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'TrailInfoContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        datas = contract.functions.getProductTrailList(id).call()

        trailInfo = []
        for data in datas:
            retObj = Ethereum.get_trail(id, Web3.toHex(data))
            if retObj['isActive']:
                trailInfo.append(retObj)

        data = {
            'id': id,
            'trailInfoList': trailInfo
        }
        return data


    @staticmethod
    def get_product_trail_list():
        web3 = Web3(Web3.HTTPProvider(geth_url))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        contractName = 'TrailInfoContract'
        contract = web3.eth.contract(
            address=contract_address_lib[contractName], abi=abi_lib[contractName])
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        datas = contract.functions.getProductList().call()
        productInfo = []
        for data in datas:
            retObj = Ethereum.get_product(Web3.toHex(data))
            productInfo.append(retObj)


        # data = {
        #     'productList':productInfo
        # }
        return productInfo

    # @staticmethod
    # def delete_trail(id):
    #     web3 = Web3(Web3.HTTPProvider(geth_url))
    #     web3.eth.defaultAccount = web3.eth.accounts[0]
    #     contractName = 'TrailInfoContract'
    #     contract = web3.eth.contract(
    #         address=contract_address_lib[contractName], abi=abi_lib[contractName])
    #     web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    #     tx_hash = contract.functions.activate(id, False).transact()
    #     receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    #     logs = contract.events.Updated().processReceipt(receipt)
    #     objId = Web3.toHex(logs[0]['args']['objId'])
    #     return objId

    # @staticmethod
    # def get_trail_list():
    #     web3 = Web3(Web3.HTTPProvider(geth_url))
    #     web3.eth.defaultAccount = web3.eth.accounts[0]
    #     contractName = 'TrailInfoContract'
    #     contract = web3.eth.contract(
    #         address=contract_address_lib[contractName], abi=abi_lib[contractName])
    #     web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    #     datas = contract.functions.getAll().call()
    #     dataInHex = []
    #     for data in datas:
    #         retObj = Ethereum.get_trail(Web3.toHex(data))
    #         if retObj['isActive']:
    #             dataInHex.append(retObj)

    #     return dataInHex
