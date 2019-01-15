from flask import Flask, request, jsonify
from application.models.model import Incident, User
from application.validations.validations import validate_input, validate_comment, validate_location

app = Flask(__name__)

all_redflags= []

@app.route('/',methods=['GET'])
def home():
    return jsonify({'message':"Welcome to iReporter"}), 200

@app.route('/api/v1/red-flags', methods=['GET'])
def get_redflags():
    return jsonify({
        'status': 200,
        "data": all_redflags }), 200
   

@app.route('/api/v1/red-flags/<int:red_flag_id>', methods=['GET'])
def get_redflag(red_flag_id):
    specific = []
    for redflag in all_redflags:
        if redflag['id'] == red_flag_id:
            specific.append(redflag['id'])
            return jsonify({
                'status':200,
                'data': [redflag]}),200
    return jsonify({"status":400, 'error': 'Red-flag not available'}),404

@app.route('/api/v1/red-flags', methods=['POST'])
def create_redflag():
    data_request = request.get_json()
    
    _id = len(all_redflags)+1
    createdOn = data_request.get('createdOn')
    createdBy = data_request.get('createdBy')
    _type = data_request.get('type')
    location = data_request.get('location')
    status = data_request.get('status')
    comment = data_request.get('comment')

    myObject = Incident(**{'id':_id,'createdOn':createdOn, 'createdBy':createdBy, 'type':_type, 'location':location, 'status':status, 'comment':comment})
    input_error = validate_input(myObject.createdOn, myObject.createdBy, myObject.status, myObject.type,myObject.location)
    comment_error = validate_comment(myObject.comment)
    location_error = validate_location(myObject.location)
    if input_error:
        return jsonify(input_error), 400
    elif comment_error:
        return jsonify(comment_error), 400
    elif location_error:
        return jsonify(location_error), 400

    redflag_exist= [ redflag for redflag in all_redflags if myObject.createdBy == redflag['createdBy'] and myObject.createdOn == redflag['createdOn'] and myObject.location == redflag['location']]
    if redflag_exist:
        return jsonify({ "status":400, 'error':'Red-flag already exists. Please create a new Red-flag'}), 400
    all_redflags.append(myObject.getRecord())
    return jsonify({
                'status':201,
                "data": [{ 'id': myObject.getRecord()['id'], "message": "Created red-flag record" }]    
            }), 201

@app.route('/api/v1/red-flags/<int:red_flag_id>/location', methods=['PATCH'])
def edit_location(red_flag_id):
    for redflag in all_redflags:
        if redflag['id'] == red_flag_id:
            redflag['location'] = request.get_json().get('location')
            location_error = validate_location(redflag['location'])
            if location_error:
                return jsonify(location_error),400
            return jsonify({
                'status':200,
                'data': [{'id':redflag['id'], 'message':"Updated red-flag record's location" }] }),200
    return jsonify({'status':404, 'error': 'Red-flag not available'}),404

@app.route('/api/v1/red-flags/<int:red_flag_id>/comment', methods=['PATCH'])
def edit_comment(red_flag_id):
    for redflag in all_redflags:
        if redflag['id'] == red_flag_id:
            redflag['comment'] = request.get_json().get('comment')
            comment_error = validate_comment(redflag['comment'])
            if comment_error:
                return jsonify(comment_error),400

            return jsonify({
                'status':200,
                'data': [{'id':redflag['id'], 'message':"Updated red-flag record's comment" }] }),200
    return jsonify({'status':404, 'error': 'Red-flag not available'}),404

@app.route('/api/v1/red-flags/<int:red_flag_id>', methods=['DELETE'])
def delete_red(red_flag_id):
    for redflag in all_redflags:
        if redflag['id'] == red_flag_id:
            all_redflags.remove(redflag)
            return jsonify({
                    'status': 200,
                    'data': [{'id':redflag['id'], 'message':'Red-flag record has been deleted'}] 
                }),200
    return jsonify({'status':404, 'error': 'Red-flag not available'}),404 
