# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.


from mongoengine import *
from flask import Flask, jsonify, request
from models import hostModel, eventModel, bankAccount, ticketsModel
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from services.hostManagement import post_create_host, patch_update_phone_number, get_all_hosts, get_host_by_id, soft_delete_host, get_hosts_by_is_deleted, host_login
from services.bankAccountManagement import create_bank_account_for_host, patch_update_bank_account, get_bank_accounts_for_user, create_bank_account, fetch_bank_accounts, get_bank_account_by_id, update_bank_account, get_bank_accounts_by_user_type
from services.eventManagement import *
from services.payoutMangement import calculate_payout_for_host
from models.ticketsModel import Ticket

app = Flask(__name__)
db_name = 'neha_sure_hw_6a'
db_connection = connect(db_name)

app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)


if not db_connection:
    print(f"Creating a new database '{db_name}'")
    db_connection = connect(db_name)
    db_connection.drop_database(db_name)


ADMIN_USERNAME = 'neha'
ADMIN_PASSWORD = 'nehasuresh'

# ... (your existing code)

# Admin login endpoint
@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    if data.get('username') == ADMIN_USERNAME and data.get('password') == ADMIN_PASSWORD:
        # Admin login successful, generate a JWT token
        access_token = create_access_token(identity=ADMIN_USERNAME)
        return jsonify({'access_token': access_token, 'message': 'Admin login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials', 'status': '401'}), 401

@app.route('/hosts/login', methods=['POST'])
def handle_host_login():
    logging.info('Entered request to login a host.')
    try:
        logging.info('Received POST request to login a host.')
        return host_login()
    except Exception as e:
        # Handle other exceptions
        error_message = f'An error occurred: {str(e)}'
        app.logger.error(error_message)
        return jsonify({'error': error_message}), 500


@app.route('/hosts', methods=['POST'])
@jwt_required()
def handle_create_host():
    logging.info('Entered request to create a new host.')
    try:
        logging.info('Received POST request to create a new host.')
        return post_create_host()
    except Exception as e:
        # Handle other exceptions
        error_message = f'An error occurred: {str(e)}'
        app.logger.error(error_message)
        return jsonify({'error': error_message}), 500

@app.route('/hosts/<string:host_id>', methods=['PATCH'])
def handle_update_phone_number(host_id):
    try:
        return patch_update_phone_number(host_id)
    except Exception as e:
        # Handle other exceptions
        error_message = f'An error occurred: {str(e)}'
        app.logger.error(error_message)
        return jsonify({'error': error_message}), 500

@app.route('/hosts', methods=['GET'])
def handle_get_all_hosts():

    is_deleted_param = request.args.get('is_deleted', type=bool, default=False)
    if is_deleted_param:
        # Call a new fn to get hosts based on the 'is_deleted' query parameter
        return get_hosts_by_is_deleted(is_deleted_param)
    else:
        return get_all_hosts()

@app.route('/hosts/<host_id>', methods=['GET'])
def handle_get_host_by_id(host_id):
    return get_host_by_id(host_id)

@app.route('/hosts/<host_id>', methods=['DELETE'])
def handle_soft_delete_host(host_id):
    return soft_delete_host(host_id)

@app.route('/hosts/<host_id>/bankaccounts', methods=['POST'])
def handle_create_bank_account_for_host(host_id):
    return create_bank_account_for_host(host_id)


@app.route('/hosts/<host_id>/bankaccounts/<account_id>', methods=['PATCH'])
def handle_update_bank_account_for_host(host_id, account_id):
    return patch_update_bank_account(host_id, account_id)

@app.route('/hosts/<string:user_id>/bankaccounts', methods=['GET'])
def handle_get_bank_accounts(user_id, user_type="vendor"):
    return get_bank_accounts_for_user(user_id, user_type)

# Event subresource
@app.route('/hosts/<host_id>/events', methods=['POST'])
def handle_create_event_for_host(host_id):
    return create_event_for_host(host_id)

@app.route('/hosts/<host_id>/events', methods=['GET'])
def handle_get_events_for_host(host_id):
    return get_events_for_host(host_id)

# Bank Account
@app.route('/bankaccounts', methods=['POST'])
def handle_create_bank_account():
    return create_bank_account()
@app.route('/bankaccounts', methods=['GET'])
def handle_get_all_bank_accounts():
    user_type = request.args.get('user_type')
    if user_type:
        return get_bank_accounts_by_user_type(user_type)
    else:
        return fetch_bank_accounts()

@app.route('/bankaccounts/<account_id>', methods=['GET'])
def handle_fetch_bank_account(account_id):
    return get_bank_account_by_id(account_id)

@app.route('/bankaccounts/<account_id>', methods=['PATCH'])
def handle_update_bank_account(account_id):
    return update_bank_account(account_id)

@app.route('/tickets', methods=['POST'])
def create_ticket():
    try:


        # Parse JSON data from the request
        request_data = request.get_json()

        # Create a new Ticket document
        new_ticket = Ticket(
            ticket_id=request_data.get('ticket_id'),  # Assuming you provide ticket_id in the request
            event_id=request_data.get('event_id'),
            host_id=request_data.get('host_id'),  # Assign the current host as the host_id
            amount_collected=request_data.get('amount_collected'),
            # Add other fields as needed
        )

        # Save the new ticket to the database
        new_ticket.save()

        return jsonify({
            'message': 'Ticket created successfully!',
            'status': '201',
            'success': 'true'
        }), 201

    except Exception as e:
        # Handle other exceptions
        error_message = f'An error occurred: {str(e)}'
        app.logger.error(error_message)
        return jsonify({'error': error_message}), 500


@app.route('/hosts/payouts', methods=['POST'])
@jwt_required()
def trigger_payouts():
    try:
        # Get the current user (assuming the request is from a host)
        current_user = get_jwt_identity()

        # You might want to validate that the current_user is a host here

        # Call the function to calculate and mark the payout for the host
        result = calculate_payout_for_host(current_user)

        return jsonify(result), 200

    except Exception as e:
        # Handle other exceptions
        error_message = f'An error occurred: {str(e)}'
        app.logger.error(error_message)
        return jsonify({'error': error_message}), 500
@app.route('/events/surgeprice', methods=['PATCH'])
def handle_surge_price_trigger():
    return surge_price()

if __name__ == "__main__":
    app.run()