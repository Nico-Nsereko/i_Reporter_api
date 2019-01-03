class Incident:
    def __init__(self, **kwargs):
        
        self.id = kwargs['id']
        self.createdOn = kwargs['createdOn']
        self.createdBy = kwargs['createdBy']
        self.incident_type = kwargs['incident_type']
        self.location = kwargs['location']
        self.incident_status = kwargs['incident_status']
        self.comment = kwargs['comment']

    def getRecord(self):
        return dict(id=self.id, createdOn=self.createdOn, createdBy=self.createdBy, incident_type=self.incident_type, location=self.location, incident_status=self.incident_status, comment=self.comment)
    