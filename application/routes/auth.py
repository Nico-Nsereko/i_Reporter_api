
from functools import wraps
from flask import Blueprint, request, jsonify, make_response
import jwt
from os import environ
from datetime import datetime, timedelta
from application.models.model import User
from werkzeug.security import check_password_hash


secret_key = environ.get('SECRET_KEY', 'This is secret')
auth_blueprint = Blueprint('auth_blueprint', __name__)

users=[]

def validate_token(request, isAdmin=False):
    try:
        auth_header = request.headers.get('Authorization')
        header_data = auth_header.split(' ')
        if not auth_header or 'Bearer ' not in auth_header or len(header_data) != 2:
            return {'message': 'Bad authorization header!'}

        decode_data = jwt.decode(header_data[1], secret_key)
        user = [u for u in users if decode_data.get('id')== u['id']]

        if not user:
            return {'message': 'User not found'}
        if isAdmin and not user[0]['isAdmin']:
            return {'message': 'Not an admin token'}
        return {'user': user}

    except Exception as e:
        return {'message': 'Invalid token!'}
    

def token_required(isAdmin=False):
    def token_required_inner(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            res = validate_token(request, isAdmin )
            if not res.get('user'):
                return jsonify(res.get('message')),401
            return f(res.get('user'),*args, **kwargs)
        return decorated
    return token_required_inner
        
@auth_blueprint.route('/users',methods=['GET'])
@token_required(isAdmin=True)
def get_users(current_user):
    return jsonify({'users':users}), 200

@auth_blueprint.route('/register',methods=['POST'])
def register_user():
    data_request = request.get_json()    
    #_id = len(users)+1
    firstname = data_request.get("firstname")
    lastname = data_request.get("lastname")
    othernames = data_request.get("othernames")
    email = data_request.get("email")
    phoneNumber = data_request.get("phoneNumber")
    username = data_request.get("username")
    password = data_request.get("password")
    registered = datetime.now().strftime("%Y-%m-%d")
    isAdmin = data_request.get('isAdmin')

    user = [u for u in users if u['email']==email]
    
    if not user:
        myObject = User(**{'firstname':firstname, 'lastname':lastname, 'othernames':othernames, 'email':email, 'phoneNumber':phoneNumber, 'username':username, 'password':password, 'registered':registered, 'isAdmin':isAdmin})
        users.append(myObject.to_dict())
        responseObject = {
            'status': 'success',
            'message': 'Successfully registered.',
            'id': myObject.id,
        }
        return make_response(jsonify(responseObject)), 201
    else:
        responseObject = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return make_response(jsonify(responseObject)), 202

@auth_blueprint.route('/login',methods=['POST'])
def login_user():
    """log in a user"""  
    try:
        req = request.get_json()
        email = req.get('email')
        password = req.get('password')
        if not req or not email or not password: 
            return jsonify({'message':'No login data found'})

        user = [u for u in users if u["email"] == email]
        if user and check_password_hash(user[0]['password'], password):
            token_data = {
                'id': user[0]['id'],
                "exp": datetime.utcnow() + timedelta(minutes=30),
                'isAdmin': user[0]['isAdmin']
                }
            token = jwt.encode(token_data, secret_key)
            return jsonify({'token': token.decode('UTF-8')})
        return jsonify({'message':'Invalid login'}),401
    except Exception as e:
        return jsonify({'Error': 'Something wrong happened'})
