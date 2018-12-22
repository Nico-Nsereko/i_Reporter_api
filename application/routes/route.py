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

