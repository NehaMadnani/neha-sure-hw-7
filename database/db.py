# from mongoengine import *
# from flask import Flask, jsonify, request

# app = Flask(__name__)
# db_name = 'neha_sure_hw_6a'
# db_connection = connect(db_name)
#
#
# if not db_connection:
#     print(f"Creating a new database '{db_name}'")
#     db_connection = connect(db_name)
#     db_connection.drop_database(db_name)

from flask_mongoengine import MongoEngine
# from services.RiderService import init_riders

db = MongoEngine()


def initialize_db(app):
    db.init_app(app)  # Create the db
    # init_riders()  # Populate it with default riders


def fetch_engine():
    return db