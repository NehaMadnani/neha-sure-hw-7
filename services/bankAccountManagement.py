from models.hostModel import Hosts
from models.bankAccount import BankAccounts
from flask import jsonify, request
import logging

def create_bank_account_for_host(host_id):
    try:
        # Retrieve the host by host_id
        host = Hosts.objects(host_id=host_id).first()

        if host:
            # Parse JSON data from the request
            request_data = request.get_json()

            # Create a new BankAccounts document
            new_bank_account = BankAccounts(
                account_id=request_data.get('account_id'),
                bank_name=request_data.get('bank_name'),
                routing_number=request_data.get('routing_number'),
                bank_account_number=request_data.get('bank_account_number'),
                user_type=request_data.get('user_type', 'vendor'),
                user_id=host_id,  # Map user_id to host_id
                phone_number=request_data.get('phone_number'),
                email_id=request_data.get('email_id'),
                transaction_limit=request_data.get('transaction_limit')
            )

            # Save the new bank account to the database
            new_bank_account.save()

            return jsonify({
                'message': 'Bank account created successfully!',
                'status': '201',
                'success': 'true'
            }), 201

        else:
            return jsonify({
                'error': 'Host not found.',
                'status': '404'
            }), 404

    except Exception as e:
        # Handle other exceptions
        logging.error(f'An error occurred: {str(e)}')
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

def patch_update_bank_account(host_id, account_id):
    try:
        # Retrieve the host by host_id
        host = Hosts.objects(host_id=host_id).first()

        if host:
            # Retrieve the bank account by account_id
            bank_account = BankAccounts.objects(account_id=account_id, user_id=host_id).first()

            if bank_account:
                # Parse JSON data from the request
                request_data = request.get_json()

                # Update bank account details
                bank_account.bank_name = request_data.get('bank_name', bank_account.bank_name)
                bank_account.routing_number = request_data.get('routing_number', bank_account.routing_number)
                bank_account.bank_account_number = request_data.get('bank_account_number', bank_account.bank_account_number)
                bank_account.phone_number = request_data.get('phone_number', bank_account.phone_number)
                bank_account.email_id = request_data.get('email_id', bank_account.email_id)
                bank_account.transaction_limit = request_data.get('transaction_limit', bank_account.transaction_limit)

                # Save the updated bank account to the database
                bank_account.save()

                return jsonify({
                    'message': 'Bank account updated successfully!',
                    'status': '200',
                    'success': 'true'
                }), 200

            else:
                return jsonify({
                    'error': 'Bank account not found.',
                    'status': '404'
                }), 404

        else:
            return jsonify({
                'error': 'Host not found.',
                'status': '404'
            }), 404

    except Exception as e:
        # Handle other exceptions
        logging.error(f'An error occurred: {str(e)}')
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

def get_bank_accounts_for_user(user_id, user_type):
    try:
        # Validate user_type
        if user_type not in ["customer", "vendor"]:
            return jsonify({
                'error': 'Invalid user_type. Must be "customer" or "vendor".',
                'status': '400'
            }), 400

        # Retrieve the host by user_id
        host = Hosts.objects(host_id=user_id).first()

        if host:
            # Retrieve all bank accounts with the specified user_id and user_type
            bank_accounts = BankAccounts.objects(user_id=user_id, user_type=user_type)

            # Convert bank accounts to a list of dictionaries
            bank_accounts_list = [
                {
                    'account_id': account.account_id,
                    'bank_name': account.bank_name,
                    'routing_number': account.routing_number,
                    'bank_account_number': account.bank_account_number,
                    'user_type': account.user_type,
                    'user_id': account.user_id,
                    'phone_number': account.phone_number,
                    'email_id': account.email_id,
                    'transaction_limit': account.transaction_limit
                }
                for account in bank_accounts
            ]

            return jsonify({'bank_accounts': bank_accounts_list}), 200

        else:
            return jsonify({
                'error': f'User with ID {user_id} and type {user_type} not found.',
                'status': '404'
            }), 404

    except Exception as e:
        # Handle other exceptions
        logging.error(f'An error occurred: {str(e)}')
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

# need to update to generic methods
def create_bank_account():
    try:
        # Parse JSON data from the request
        request_data = request.get_json()

        # Create a new BankAccounts document
        new_bank_account = BankAccounts(
            account_id=request_data.get('account_id'),
            bank_name=request_data.get('bank_name'),
            routing_number=request_data.get('routing_number'),
            bank_account_number=request_data.get('bank_account_number'),
            user_type=request_data.get('user_type'),
            phone_number=request_data.get('phone_number'),
            email_id=request_data.get('email_id'),
            transaction_limit=request_data.get('transaction_limit'),
            user_id=request_data.get('user_id')
        )

        # Save the new bank account to the database
        new_bank_account.save()

        return jsonify({
            'message': 'Bank account created successfully!',
            'status': '201',
            'success': 'true'
        }), 201

    except Exception as e:
        # Handle other exceptions
        logging.error(f'An error occurred: {str(e)}')
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

def fetch_bank_accounts():
    try:
        # Retrieve all bank accounts
        bank_accounts = BankAccounts.objects()

        # Convert bank accounts to a list of dictionaries
        bank_accounts_list = [
            {
                'account_id': account.account_id,
                'bank_name': account.bank_name,
                'routing_number': account.routing_number,
                'bank_account_number': account.bank_account_number,
                'user_type': account.user_type,
                'phone_number': account.phone_number,
                'email_id': account.email_id,
                'transaction_limit': account.transaction_limit,
                'user_id': account.user_id
            }
            for account in bank_accounts
        ]

        return jsonify({
            'status_code': 200,
            'status': 'success',
            'bank_accounts': bank_accounts_list
        }), 200

    except Exception as e:
        # Handle other exceptions
        logging.error(f'An error occurred: {str(e)}')
        return jsonify({
            'status_code': 500,
            'status': 'error',
            'error': f'An error occurred: {str(e)}'
        }), 500

def get_bank_account_by_id(account_id):
    try:
        # Retrieve the bank account by account_id
        bank_account = BankAccounts.objects(account_id=account_id).first()

        if bank_account:
            # Convert bank account to a dictionary
            bank_account_data = {
                'account_id': bank_account.account_id,
                'bank_name': bank_account.bank_name,
                'routing_number': bank_account.routing_number,
                'bank_account_number': bank_account.bank_account_number,
                'user_type': bank_account.user_type,
                'phone_number': bank_account.phone_number,
                'email_id': bank_account.email_id,
                'transaction_limit': bank_account.transaction_limit,
                'user_id': bank_account.user_id
            }

            return jsonify({
                'status_code': 200,
                'status': 'success',
                'bank_account': bank_account_data
            }), 200

        else:
            return jsonify({
                'status_code': 404,
                'status': 'error',
                'error': 'Bank account not found.'
            }), 404

    except Exception as e:
        # Handle other exceptions
        logging.error(f'An error occurred: {str(e)}')
        return jsonify({
            'status_code': 500,
            'status': 'error',
            'error': f'An error occurred: {str(e)}'
        }), 500

def update_bank_account(account_id):
    try:
        # Retrieve the bank account by account_id
        bank_account = BankAccounts.objects(account_id=account_id).first()

        if bank_account:
            # Parse JSON data from the request
            request_data = request.get_json()

            # Update bank account details if provided in the request
            if 'bank_name' in request_data:
                bank_account.bank_name = request_data['bank_name']

            if 'phone_number' in request_data:
                bank_account.phone_number = request_data['phone_number']

            if 'email_id' in request_data:
                bank_account.email_id = request_data['email_id']

            if 'transaction_limit' in request_data:
                bank_account.transaction_limit = request_data['transaction_limit']

            # Save the updated bank account to the database
            bank_account.save()

            return jsonify({
                'status_code': 200,
                'status': 'success',
                'message': 'Bank account updated successfully!'
            }), 200

        else:
            return jsonify({
                'status_code': 404,
                'status': 'error',
                'error': 'Bank account not found.'
            }), 404

    except Exception as e:
        # Handle other exceptions
        logging.error(f'An error occurred: {str(e)}')
        return jsonify({
            'status_code': 500,
            'status': 'error',
            'error': f'An error occurred: {str(e)}'
        }), 500

def get_bank_accounts_by_user_type(user_type):
    try:
        # Get user_type from the request query parameters
        user_type = request.args.get('user_type')

        # Validate user_type
        if user_type not in ["customer", "host"]:
            return jsonify({
                'status_code': 400,
                'status': 'error',
                'error': 'Invalid user_type. Accepted values: "customer", "host".'
            }), 400

        # Retrieve bank accounts based on user_type
        bank_accounts = BankAccounts.objects(user_type=user_type)

        # Convert bank accounts to a list of dictionaries
        bank_accounts_list = [
            {
                'account_id': account.account_id,
                'bank_name': account.bank_name,
                'routing_number': account.routing_number,
                'bank_account_number': account.bank_account_number,
                'user_type': account.user_type,
                'phone_number': account.phone_number,
                'email_id': account.email_id,
                'transaction_limit': account.transaction_limit,
                'user_id': account.user_id
            }
            for account in bank_accounts
        ]

        return jsonify({
            'status_code': 200,
            'status': 'success',
            'bank_accounts': bank_accounts_list
        }), 200

    except Exception as e:
        # Handle other exceptions
        logging.error(f'An error occurred: {str(e)}')
        return jsonify({
            'status_code': 500,
            'status': 'error',
            'error': f'An error occurred: {str(e)}'
        }), 500