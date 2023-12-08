from mongoengine import *

class Hosts(Document):
    host_id = StringField(max_length=10, unique=True)
    first_name = StringField(max_length=40)
    last_name = StringField(max_length=40)
    user_id = StringField(max_length=10)
    org_type = StringField(max_length=40)
    is_tax_registered = BooleanField(Default=False)
    phone_number = StringField(max_length=10)
    email_id=StringField(max_length=20)
    business_name=StringField(max_length=50)
    business_address=StringField(max_length=100)
    is_deleted=BooleanField(Default=False)
