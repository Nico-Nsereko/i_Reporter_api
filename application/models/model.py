import jwt
from uuid import uuid4
from werkzeug.security import generate_password_hash
class Incident:
    def __init__(self, **kwargs):
        
        self.id = kwargs['id']
        self.createdOn = kwargs['createdOn']
        self.createdBy = kwargs['createdBy']
        self.type = kwargs['type']
        self.location = kwargs['location']
        self.status = kwargs['status']
        self.comment = kwargs['comment']

    def getRecord(self):
        return dict(id=self.id, createdOn=self.createdOn, createdBy=self.createdBy, type=self.type, location=self.location, status=self.status, comment=self.comment)


class User:
    def __init__(self, **kwargs):
        self.id = str(uuid4())
        #self.id = kwargs['id']
        self.firstname= kwargs['firstname']
        self.lastname= kwargs['lastname']
        self.othernames= kwargs['othernames']
        self.email = kwargs['email']
        self.phoneNumber = kwargs['phoneNumber']
        self.username = kwargs['username']
        self.password = generate_password_hash(kwargs['password'])
        self.registered = kwargs['registered']
        self.isAdmin = kwargs['isAdmin']

    def to_dict(self):
        return dict(id=self.id, firstname= self.firstname, lastname=self.lastname,othernames=self.othernames,email=self.email,phoneNumber=self.phoneNumber, username=self.username, password=self.password, registered=self.registered, isAdmin=self.isAdmin)
