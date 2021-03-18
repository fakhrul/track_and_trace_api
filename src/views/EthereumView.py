# /src/views/ActivityView.py
from flask import Flask, request, g, Blueprint, json, Response, send_file
from marshmallow import ValidationError
from ..shared.Authentication import Auth
from ..shared.Ethereum import Ethereum
from ..shared.QrGenerator import QrGenerator
from io import BytesIO

app = Flask(__name__)
etheruem_api = Blueprint('etheruem_api', __name__)


@etheruem_api.route('/', methods=['GET'])
def index():
    return custom_response('etheruem', 200)

@etheruem_api.route('/signin', methods=['POST'])
def signin():
    req_data = request.get_json()
    email = req_data['email'];
    password = req_data['password'];
    profile = Ethereum.get_profile_by_email(email);
    if profile['password'] == password :
        retObj = {
            'status': "success",
            'data' : profile,
            'token': Auth.generate_token(email)
        }
        return custom_response(retObj, 200)

    retObj = {
        'status': 'failed',
    }
    return custom_response(retObj, 200)

@etheruem_api.route('/generateQr/<string:id>')
def generateQr(id):
    img = QrGenerator.generate(id)
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

## ORGANIZATION TYPE

@etheruem_api.route('/organizationType', methods=['GET'])
def get_organization_type_list():
    retObj = {
        'data' : Ethereum.get_organization_type_list()
    }
    return custom_response(retObj, 200)

@etheruem_api.route('/organizationType/<string:id>', methods=['GET'])
def getOrganizationType(id):
    retObj = {
        'data' : Ethereum.get_organization_type(id)
    }
    return custom_response(retObj, 200)

@etheruem_api.route('/organizationType', methods=['POST'])
def createOrganizationType():
    req_data = request.get_json()
    name = req_data['name'];
    custom = req_data['custom'];

    data = Ethereum.create_organization_type(name, custom)
    retObj = {
        'data' : data
    }
    return custom_response(retObj, 201)    

@etheruem_api.route('/organizationType/<string:id>', methods=['PUT'])
def updateOrganizationType(id):
    req_data = request.get_json()
    name = req_data['name'];
    custom = req_data['custom'];

    data = Ethereum.update_organization_type(id, name, custom)
    retObj = {
        'data' : data
    }
    return custom_response(retObj, 201)    

@etheruem_api.route('/organizationType/<string:id>', methods=['DELETE'])
def deleteOrganizationType(id):
    retObj = {
        'data' : Ethereum.delete_organization_type(id)
    }
    return custom_response(retObj, 200)

## ORGANIZATION

@etheruem_api.route('/organization', methods=['GET'])
def getOrganizationList():
    retObj = {
        'data' : Ethereum.get_organization_list()
    }
    return custom_response(retObj, 200)

@etheruem_api.route('/organization/<string:id>', methods=['GET'])
def getOrganization(id):
    retObj = {
        'data' : Ethereum.get_organization(id)
    }
    return custom_response(retObj, 200)

@etheruem_api.route('/organization', methods=['POST'])
def createOrganization():
    req_data = request.get_json()
    name = req_data['name'];
    organizationTypeIdList = req_data['organizationTypeIdList'];
    organizationAddress = req_data['organizationAddress'];
    custom = req_data['customJsonData'];
    
    print(req_data)
    data = Ethereum.create_organization(name, organizationTypeIdList, organizationAddress, custom)
    retObj = {
        'data' : data
    }
    return custom_response(retObj, 201)    

@etheruem_api.route('/organization/<string:id>', methods=['PUT'])
def updateOrganization(id):
    req_data = request.get_json()
    name = req_data['name'];
    organizationTypeIdList = req_data['organizationTypeIdList'];
    organizationAddress = req_data['organizationAddress'];
    custom = req_data['custom'];

    data = Ethereum.update_organization(id, name,organizationTypeIdList, organizationAddress, custom)
    retObj = {
        'data' : data
    }
    return custom_response(retObj, 201)    

@etheruem_api.route('/organization/<string:id>', methods=['DELETE'])
def deleteOrganization(id):
    retObj = {
        'data' : Ethereum.delete_organization(id)
    }
    return custom_response(retObj, 200)

## ACTIVITY

@etheruem_api.route('/activity', methods=['GET'])
def getActivityList():
    retObj = {
        'data' : Ethereum.get_activity_list()
    }
    return custom_response(retObj, 200)

@etheruem_api.route('/activity/<string:id>', methods=['GET'])
def getActivity(id):
    retObj = {
        'data' : Ethereum.get_activity(id)
    }
    return custom_response(retObj, 200)

@etheruem_api.route('/activityByOrganization/<string:id>', methods=['GET'])
def getActivityByOrganization(id):
    retObj = {
        'data' : Ethereum.get_activity_list_by_organization(id)
    }
    return custom_response(retObj, 200)


@etheruem_api.route('/activity', methods=['POST'])
def createActivity():
    req_data = request.get_json()
    name = req_data['name']
    organizationType = req_data['organizationType']
    custom = req_data['customJsonData']

    data = Ethereum.create_activity(name, organizationType, custom)
    retObj = {
        'data' : data
    }
    return custom_response(retObj, 201)    

@etheruem_api.route('/activity/<string:id>', methods=['PUT'])
def updateActivity(id):
    req_data = request.get_json()
    name = req_data['name']
    organizationType = req_data['organizationType']
    custom = req_data['custom']

    data = Ethereum.update_activity(id, name,organizationType, custom)
    retObj = {
        'data' : data
    }
    return custom_response(retObj, 201)    

@etheruem_api.route('/activity/<string:id>', methods=['DELETE'])
def deleteActivity(id):
    retObj = {
        'data' : Ethereum.delete_activity(id)
    }
    return custom_response(retObj, 200)

## AREA

@etheruem_api.route('/area', methods=['GET'])
def getAreaList():
    retObj = {
        'data' : Ethereum.get_area_list()
    }
    return custom_response(retObj, 200)

@etheruem_api.route('/area/<string:id>', methods=['GET'])
def getArea(id):
    retObj = {
        'data' : Ethereum.get_area(id)
    }
    return custom_response(retObj, 200)

@etheruem_api.route('/areaByOrganization/<string:id>', methods=['GET'])
def getAreaByOrganization(id):
    retObj = {
        'data' : Ethereum.get_area_list_by_organization(id)
    }
    return custom_response(retObj, 200)


@etheruem_api.route('/area', methods=['POST'])
def createArea():
    req_data = request.get_json()
    name = req_data['name']
    organization = req_data['organization']
    custom = req_data['customJsonData']

    data = Ethereum.create_area(name, organization, custom)
    retObj = {
        'data' : data
    }
    return custom_response(retObj, 201)    

@etheruem_api.route('/area/<string:id>', methods=['PUT'])
def updateArea(id):
    req_data = request.get_json()
    name = req_data['name']
    organization = req_data['organization']
    custom = req_data['custom']

    data = Ethereum.update_area(id, name,organization, custom)
    retObj = {
        'data' : data
    }
    return custom_response(retObj, 201)    

@etheruem_api.route('/area/<string:id>', methods=['DELETE'])
def deleteArea(id):
    retObj = {
        'data' : Ethereum.delete_area(id)
    }
    return custom_response(retObj, 200)


## category

@etheruem_api.route('/category', methods=['GET'])
def getCategoryList():
    retObj = {
        'data' : Ethereum.get_category_list()
    }
    return custom_response(retObj, 200)

@etheruem_api.route('/category/<string:id>', methods=['GET'])
def getCategory(id):
    retObj = {
        'data' : Ethereum.get_category(id)
    }
    return custom_response(retObj, 200)

@etheruem_api.route('/category', methods=['POST'])
def createCategory():
    req_data = request.get_json()
    name = req_data['name']
    custom = req_data['customJsonData']

    data = Ethereum.create_category(name, custom)
    retObj = {
        'data' : data
    }
    return custom_response(retObj, 201)    

@etheruem_api.route('/category/<string:id>', methods=['PUT'])
def updateCategory(id):
    req_data = request.get_json()
    name = req_data['name']
    custom = req_data['custom']

    data = Ethereum.update_category(id, name, custom)
    retObj = {
        'data' : data
    }
    return custom_response(retObj, 201)    

@etheruem_api.route('/category/<string:id>', methods=['DELETE'])
def deleteCategory(id):
    retObj = {
        'data' : Ethereum.delete_category(id)
    }
    return custom_response(retObj, 200)


## certification

@etheruem_api.route('/certification', methods=['GET'])
def getCertificationList():
    retObj = {
        'data' : Ethereum.get_certification_list()
    }
    return custom_response(retObj, 200)

@etheruem_api.route('/certification/<string:id>', methods=['GET'])
def getCertification(id):
    retObj = {
        'data' : Ethereum.get_certification(id)
    }
    return custom_response(retObj, 200)

@etheruem_api.route('/certification', methods=['POST'])
def createCertification():
    req_data = request.get_json()
    name = req_data['name']
    certificateUrl = req_data['certificateUrl']
    custom = req_data['customJsonData']

    data = Ethereum.create_certification(name, certificateUrl, custom)
    retObj = {
        'data' : data
    }
    return custom_response(retObj, 201)    

@etheruem_api.route('/certification/<string:id>', methods=['PUT'])
def updateCertification(id):
    req_data = request.get_json()
    name = req_data['name']
    certificateUrl = req_data['certificateUrl']
    custom = req_data['custom']

    data = Ethereum.update_certification(id, name,certificateUrl, custom)
    retObj = {
        'data' : data
    }
    return custom_response(retObj, 201)    

@etheruem_api.route('/certification/<string:id>', methods=['DELETE'])
def deleteCertification(id):
    retObj = {
        'data' : Ethereum.delete_certification(id)
    }
    return custom_response(retObj, 200)

## product

@etheruem_api.route('/product', methods=['GET'])
def getProductList():
    retObj = {
        'data' : Ethereum.get_product_list()
    }
    return custom_response(retObj, 200)

@etheruem_api.route('/product/<string:id>', methods=['GET'])
def getProduct(id):
    retObj = {
        'data' : Ethereum.get_product(id)
    }
    return custom_response(retObj, 200)

@etheruem_api.route('/product', methods=['POST'])
def createProduct():
    req_data = request.get_json()
    name = req_data['name']
    category = req_data['category']
    description = req_data['description']
    certificationList = req_data['certificationList']
    custom = req_data['customJsonData']

    data = Ethereum.create_product(name, category, description, certificationList ,  custom)
    retObj = {
        'data' : data
    }
    return custom_response(retObj, 201)    

@etheruem_api.route('/product/<string:id>', methods=['PUT'])
def updateProduct(id):
    req_data = request.get_json()
    name = req_data['name']
    category = req_data['category']
    description = req_data['description']
    certificationList = req_data['certificationList']
    custom = req_data['custom']

    data = Ethereum.update_product(id, name, category, description, certificationList, custom)
    retObj = {
        'data' : data
    }
    return custom_response(retObj, 201)    

@etheruem_api.route('/product/<string:id>', methods=['DELETE'])
def deleteProduct(id):
    retObj = {
        'data' : Ethereum.delete_product(id)
    }
    return custom_response(retObj, 200)

## profile

@etheruem_api.route('/profile', methods=['GET'])
def getProfileList():
    retObj = {
        'data' : Ethereum.get_profile_list()
    }
    return custom_response(retObj, 200)

@etheruem_api.route('/profileByOrganization/<string:id>', methods=['GET'])
def getProfileByOrganization(id):
    retObj = {
        'data' : Ethereum.get_profile_list_by_organization(id)
    }
    return custom_response(retObj, 200)


@etheruem_api.route('/profile/<string:id>', methods=['GET'])
def getProfile(id):
    retObj = {
        'data' : Ethereum.get_profile(id)
    }
    return custom_response(retObj, 200)

@etheruem_api.route('/profile', methods=['POST'])
def createProfile():
    req_data = request.get_json()
    name = req_data['name']
    email = req_data['email']
    password = req_data['password']
    phone = req_data['phone']
    roleList = req_data['roleList']
    organization = req_data['organization']
    custom = req_data['customJsonData']

    data = Ethereum.create_profile(name, email, password,  phone, roleList, organization, custom)
    retObj = {
        'data' : data
    }
    return custom_response(retObj, 201)    

@etheruem_api.route('/profile/<string:id>', methods=['PUT'])
def updateProfile(id):
    req_data = request.get_json()
    name = req_data['name']
    email = req_data['email']
    password = req_data['password']
    phone = req_data['phone']
    roleList = req_data['roleList']
    organization = req_data['organization']
    custom = req_data['custom']

    data = Ethereum.update_profile(id, name, email, password,
     phone, roleList, organization, custom)
    retObj = {
        'data' : data
    }
    return custom_response(retObj, 201)    

@etheruem_api.route('/profile/<string:id>', methods=['DELETE'])
def deleteProfile(id):
    retObj = {
        'data' : Ethereum.delete_profile(id)
    }
    return custom_response(retObj, 200)

## role

@etheruem_api.route('/role', methods=['GET'])
def getRoleList():
    retObj = {
        'data' : Ethereum.get_role_list()
    }
    return custom_response(retObj, 200)

@etheruem_api.route('/role/<string:id>', methods=['GET'])
def getRole(id):
    retObj = {
        'data' : Ethereum.get_role(id)
    }
    return custom_response(retObj, 200)

@etheruem_api.route('/role', methods=['POST'])
def createRole():
    req_data = request.get_json()
    name = req_data['name']
    custom = req_data['customJsonData']

    data = Ethereum.create_role(name, custom)
    retObj = {
        'data' : data
    }
    return custom_response(retObj, 201)    

@etheruem_api.route('/role/<string:id>', methods=['PUT'])
def updateRole(id):
    req_data = request.get_json()
    name = req_data['name']
    custom = req_data['custom']

    data = Ethereum.update_role(id, name, custom)
    retObj = {
        'data' : data
    }
    return custom_response(retObj, 201)    

@etheruem_api.route('/role/<string:id>', methods=['DELETE'])
def deleteRole(id):
    retObj = {
        'data' : Ethereum.delete_role(id)
    }
    return custom_response(retObj, 200)


## trail

@etheruem_api.route('/trail', methods=['GET'])
def getProductTrailList():
    retObj = {
        'data' : Ethereum.get_product_trail_list()
    }
    return custom_response(retObj, 200)

@etheruem_api.route('/trail/<string:id>', methods=['GET'])
def getProductTrail(id):
    retObj = {
        'data' : Ethereum.get_product_trail(id)
    }
    return custom_response(retObj, 200)

@etheruem_api.route('/trail', methods=['POST'])
def createTrail():
    req_data = request.get_json()
    product = req_data['product']
    activity = req_data['activity']
    profile = req_data['profile']
    area = req_data['area']
    gps = req_data['gps']
    remarks = req_data['remarks']
    custom = req_data['customJsonData']

    data = Ethereum.create_trail(product, activity, profile, area, gps, remarks, custom)
    retObj = {
        'data' : data
    }
    return custom_response(retObj, 201)    

def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
