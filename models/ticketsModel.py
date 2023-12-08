from mongoengine import *

class Ticket(Document):
    ticket_id = StringField(max_length=10, unique=True)
    event_id = StringField(max_length=10)
    host_id = StringField(max_length=10)
    amount_collected = FloatField()
    host_paid = BooleanField(default=False)
    # Add other fields as needed

# You may need to add other fields such as event_id, payment_date, etc., based on your requirements
