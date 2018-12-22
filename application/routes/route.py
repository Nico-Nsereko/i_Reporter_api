from flask import Flask, request, jsonify
import datetime
from application.models.model import Incident

app = Flask(__name__)

statuses =('draft', 'rejected', 'under investigation', 'resolved')
ttype = ('red-flag', 'intervention')
all_redflags= [
    #   {
    #       "id": 0,
    #       "createdOn": datetime.datetime.utcnow(),
    #       "createdBy" : 1,
    #       "type" : 1,
    #       "location" : "lat 0.00333 long 1.3456",
    #       "status" : "Draft",
    #       "comment" : "This is my comment."
    #   }
]

@app.route('/')
def home():
    return jsonify({'message':"Welcome to iReporter"}),200



@app.route('/api/v1/red-flags', methods=['POST'])
def create_redflag():
    data_request = request.get_json()
    id = len(all_redflags)+1
    createdOn = data_request.get('createdOn')
    createdBy = data_request.get('createdBy')
    incident_type = data_request.get('incident_type')
    location = data_request.get('location')
    incident_status = data_request.get('incident_status')
    comment = data_request.get('comment')

    myObject = Incident(**{'id':id,'createdOn':createdOn, 'createdBy':createdBy, 'incident_type':incident_type, 'location':location, 'incident_status':incident_status, 'comment':comment})
    if(createdBy == None or myObject.incident_type == '' or myObject.incident_status == ''):
        return jsonify({'error':'Please add missing fields'}),400
    if incident_status not in statuses:
        return jsonify({'error':'Incident status should either be draft, or rejected, or under investigation, or resolved'}), 400
    if incident_type not in ttype:
        return jsonify({'error':'Incident type should either be red-flag or intervention'}), 400
    if (len(myObject.comment)>30):
        return jsonify({'error':'Do not exceed 30 characters'}),400
    
    all_redflags.append(myObject.getRecord())
    return jsonify({
                'status':201,
                "data": [{
                    'id': myObject.getRecord()['id'],
                    "message": "Created red-flag record"
                }]    
            }), 201

@app.route('/api/v1/red-flags', methods=['GET'])
def get_redflags():
    if len(all_redflags)>0:
        return jsonify({
            'status': 200,
            "data": [all_redflags] }), 200
    return jsonify({"message": "No red flags detected"}), 400

@app.route('/api/v1/red-flags/<int:red_flag_id>', methods=['GET'])
def get_redflag(red_flag_id):
    specific = []
    for redflag in all_redflags:
        if redflag['id'] == red_flag_id:
            specific.append(redflag['id'])
            return jsonify({
                'status':redflag['id'],
                'data': [redflag]}),200
    return jsonify({'error': 'Red-flag not available'}),404

@app.route('/api/v1/red-flags/<int:red_flag_id>/location', methods=['PATCH'])
def edit_location(red_flag_id):
    for redflag in all_redflags:
        if redflag['id'] == red_flag_id:
            redflag['location'] = request.get_json().get('location')
            if(len(redflag['location'])==0):
                return jsonify({'error':"Location can't be empty"}),404
            return jsonify({
                'status':200,
                'data': [{
                    'id':redflag['id'],
                    'message':"Updated red-flag record's location"
                }]}),200
    return jsonify({'error': 'Red-flag not available'}),400 

@app.route('/api/v1/red-flags/<int:red_flag_id>/comment', methods=['PATCH'])
def edit_comment(red_flag_id):
    for redflag in all_redflags:
        if redflag['id'] == red_flag_id:
            redflag['comment'] = request.get_json().get('comment')
            if(len(redflag['comment'])==0):
                return jsonify({'error':"Comment can't be empty"}),404
            return jsonify({
                'status':200,
                'data': [{
                    'id':redflag['id'],
                    'message':"Updated red-flag record's comment"
                }]}),200
    return jsonify({'error': 'Red-flag not available'}),400 

@app.route('/api/v1/red-flags/<int:red_flag_id>', methods=['DELETE'])
def delete_red(red_flag_id):
    for redflag in all_redflags:
        if redflag['id'] == red_flag_id:
            all_redflags.remove(redflag)
            return jsonify(
                {
                    'status': 200,
                    'data': [{'id':redflag['id'],
                    'message':'Red-flag record has been deleted'
                    }]
                    }
                ),200
    return jsonify({'error': 'Red-flag not available'}),400 

