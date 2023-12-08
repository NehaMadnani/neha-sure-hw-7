from mongoengine import *
from models.hostModel import Hosts
from flask import jsonify, request
from flask_jwt_extended import create_access_token
import logging

def host_login():
    try:
        # Parse JSON data from the request
        request_data = request.get_json()

        # Find the host by user_id
        host = Hosts.objects(user_id=request_data.get('user_id')).first()

        if host and request_data.get('password') == host.password:
            # Password is matched, generate a JWT token
            access_token = create_access_token(identity=host.user_id)
            return jsonify({
                'access_token': access_token,
                'message': 'Host login successful!',
                'status': '200',
                'success': 'true'
            }), 200
        else:
            return jsonify({
                'error': 'Invalid credentials.',
                'status': '401'
            }), 401

    except Exception as e:
        # Handle other exceptions
        logging.error(f'An error occurred: {str(e)}')
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

def post_create_host():
    try:
        # Parse JSON data from the request
        request_data = request.get_json()

        # Create a new Hosts document
        new_host = Hosts(
            host_id=request_data.get('host_id'),
            first_name=request_data.get('first_name'),
            last_name=request_data.get('last_name'),
            user_id=request_data.get('user_id'),
            org_type=request_data.get('org_type'),
            is_tax_registered=request_data.get('is_tax_registered', False),
            phone_number=request_data.get('phone_number'),
            email_id=request_data.get('email_id'),
            business_name=request_data.get('business_name'),
            business_address=request_data.get('business_address')
        )

        # Save the new host to the database
        new_host.save()

        return jsonify({
            'message': 'Host created successfully!',
            'status': '201',
            'success': 'true'
        }), 201

    except Exception as e:
        # Handle other exceptions
        logging.error(f'An error occurred: {str(e)}')
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

def patch_update_phone_number(host_id):
    try:
        # Parse JSON data from the request
        request_data = request.get_json()

        # Find the host by host_id
        host = Hosts.objects(host_id=host_id).first()

        if host:
            # Update the phone number if provided in the request
            new_phone_number = request_data.get('phone_number')
            if new_phone_number:
                host.phone_number = new_phone_number
                host.save()

                return jsonify({
                    'message': 'Phone number updated successfully!',
                    'status': '200',
                    'success': 'true'
                }), 200
            else:
                return jsonify({
                    'error': 'Phone number not provided in the request.',
                    'status': '400'
                }), 400

        else:
            return jsonify({
                'error': 'Host not found.',
                'status': '404'
            }), 404

    except Exception as e:
        # Handle other exceptions
        logging.error(f'An error occurred: {str(e)}')
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

def get_all_hosts():
    try:
        # Retrieve all hosts from the database
        all_hosts = Hosts.objects()

        # Convert hosts to a list of dictionaries
        hosts_list = [
            {
                'host_id': host.host_id,
                'first_name': host.first_name,
                'last_name': host.last_name,
                'user_id': host.user_id,
                'org_type': host.org_type,
                'is_tax_registered': host.is_tax_registered,
                'phone_number': host.phone_number,
                'email_id': host.email_id,
                'business_name': host.business_name,
                'business_address': host.business_address,
            }
            for host in all_hosts
        ]

        return jsonify({'hosts': hosts_list}), 200

    except Exception as e:
        # Handle other exceptions
        logging.error(f'An error occurred: {str(e)}')
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

def get_host_by_id(host_id):
    try:
        # Retrieve the host from the database by host_id
        host = Hosts.objects(host_id=host_id).first()

        if host:
            # Convert host to a dictionary
            host_data = {
                'host_id': host.host_id,
                'first_name': host.first_name,
                'last_name': host.last_name,
                'user_id': host.user_id,
                'org_type': host.org_type,
                'is_tax_registered': host.is_tax_registered,
                'phone_number': host.phone_number,
                'email_id': host.email_id,
                'business_name': host.business_name,
                'business_address': host.business_address,
            }

            return jsonify({'host': host_data}), 200

        else:
            return jsonify({
                'error': 'Host not found.',
                'status': '404'
            }), 404

    except Exception as e:
        # Handle other exceptions
        logging.error(f'An error occurred: {str(e)}')
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

def soft_delete_host(host_id):
    try:
        # Retrieve the host from the database by host_id
        host = Hosts.objects(host_id=host_id).first()

        if host:
            # Soft delete the host by setting is_deleted to True
            host.is_deleted = True
            host.save()

            return jsonify({
                'message': 'Host soft deleted successfully!',
                'status': '200',
                'success': 'true'
            }), 200

        else:
            return jsonify({
                'error': 'Host not found.',
                'status': '404'
            }), 404

    except Exception as e:
        # Handle other exceptions
        logging.error(f'An error occurred: {str(e)}')
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

# resources/host_resources.py
def get_hosts_by_is_deleted(is_deleted_param):
    try:
        # Retrieve hosts based on the is_deleted query parameter
        hosts = Hosts.objects(is_deleted=is_deleted_param)

        # Convert hosts to a list of dictionaries
        hosts_list = [
            {
                'host_id': host.host_id,
                'first_name': host.first_name,
                'last_name': host.last_name,
                'user_id': host.user_id,
                'org_type': host.org_type,
                'is_tax_registered': host.is_tax_registered,
                'phone_number': host.phone_number,
                'email_id': host.email_id,
                'business_name': host.business_name,
                'business_address': host.business_address,
                'is_deleted': host.is_deleted,
            }
            for host in hosts
        ]

        return jsonify({'hosts': hosts_list}), 200

    except Exception as e:
        # Handle other exceptions
        logging.error(f'An error occurred: {str(e)}')
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
