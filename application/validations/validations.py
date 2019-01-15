from datetime import datetime
statuses =('draft', 'rejected', 'under investigation', 'resolved')
ttype = ('red-flag', 'intervention')

def validate_input(createdOn, createdBy, status, _type, location):
    if(createdBy == None or _type == None or status == None or createdOn == None or location == None):
        return {"status":400, 'error':'Please add missing fields; createdBy, createdOn, type, location,and status can not be empty '}
    if type(createdBy) != int:
         return {"status":400, 'error':'createdBy should be of integer type.'}
    try:
        datetime.strptime(createdOn, '%d/%m/%Y')
    except Exception as e:
        return { "status":400, 'error':'Date format should be DD/MM/YYYY for createdOn'}

    if status.lower() not in statuses:
        return {'error':'Incident status should either be draft, or rejected, or under investigation, or resolved'}
    if _type.lower() not in ttype:
        return {"status":400, 'error':'Incident type should either be red-flag or intervention'}

def validate_location(location):
    if (len(str(location))==0 or type(location) != str or location.isspace()):
        return {"status":400, 'error':'The location should be a string and can not be empty'}

def validate_comment(comment):
    if (len(str(comment))<15 or len(str(comment))>50 or type(comment) != str):
        return {"status":400, 'error':'The comment should be a string with a range 30-50 characters'}