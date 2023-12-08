from mongoengine import *


class BankAccounts(Document):
    account_id = StringField(max_length=10, unique=True)
    bank_name = StringField(max_length=40)
    routing_number = IntField(max_length=40)
    bank_account_number = StringField(max_length=10)
    user_type = StringField(choices=["customer", "vendor"])
    phone_number = StringField(max_length=10)
    email_id = StringField(max_length=20)
    transaction_limit = StringField(max_length=50)
    user_id=StringField(max_length=50)
