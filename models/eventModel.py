from mongoengine import *
from models.hostModel import Hosts
class Events(Document):
    event_id = StringField(max_length=10, unique=True)
    event_date = DateField()
    event_name = StringField(max_length=40)
    event_host_name=StringField(max_length=40)
    event_address = StringField(max_length=100)
    email = StringField(max_length=40)
    phone_number = StringField(max_length=10)
    no_of_seats=IntField(max_length=4)
    seat_categories=ListField(DictField())
    event_host = ReferenceField(Hosts)
    is_deleted=BooleanField(Default=False)
