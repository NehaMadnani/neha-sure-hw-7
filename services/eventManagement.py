from models.hostModel import Hosts
from models.eventModel import Events
from flask import jsonify, request
import logging

def create_event_for_host(host_id):
    try:
        # Retrieve the host by host_id
        host = Hosts.objects(host_id=host_id).first()

        if host:
            # Parse JSON data from the request
            request_data = request.get_json()

            # Create a new Events document
            new_event = Events(
                event_id=request_data.get('event_id'),
                event_date=request_data.get('event_date'),
                event_name=request_data.get('event_name'),
                event_host_name=request_data.get('event_host_name'),
                event_address=request_data.get('event_address'),
                email=request_data.get('email'),
                phone_number=request_data.get('phone_number'),
                no_of_seats=request_data.get('no_of_seats'),
                seat_categories=request_data.get('seat_categories'),
                event_host=host,  # Map event_host to the retrieved host
                is_deleted=request_data.get('is_deleted', False)
            )

            # Save the new event to the database
            new_event.save()

            return jsonify({
                'message': 'Event created successfully!',
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

def get_events_for_host(host_id):
    try:
        # Retrieve the host by host_id
        host = Hosts.objects(host_id=host_id).first()

        if host:
            # Retrieve all events associated with the host
            events = Events.objects(event_host=host)

            # Convert events to a list of dictionaries
            events_list = [
                {
                    'event_id': event.event_id,
                    'event_date': str(event.event_date),
                    'event_name': event.event_name,
                    'event_host_name': event.event_host_name,
                    'event_address': event.event_address,
                    'email': event.email,
                    'phone_number': event.phone_number,
                    'no_of_seats': event.no_of_seats,
                    'seat_categories': event.seat_categories,
                    'is_deleted': event.is_deleted
                }
                for event in events
            ]

            return jsonify({'events': events_list}), 200

        else:
            return jsonify({
                'error': 'Host not found.',
                'status': '404'
            }), 404

    except Exception as e:
        # Handle other exceptions
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

def surge_price():
    try:
        # Parse JSON data from the request
        request_data = request.get_json()

        # Validate that the required fields are present in the request
        if 'event_id' not in request_data or 'surge_percent' not in request_data:
            return jsonify({'error': 'Event ID and surge_percent are required in the request.'}), 400

        # Retrieve the event from the database by event_id
        event = Events.objects(event_id=request_data['event_id']).first()

        if event:
            # Increase the seat_categories prices by surge_percent
            surge_percent = float(request_data['surge_percent']) / 100.0  # Convert percentage to decimal
            for category in event.seat_categories:
                # Assuming each category is a dictionary with keys like 'basic' and 'special'
                for key in category:
                    if key in ['basic', 'special']:  # Add other categories as needed
                        category[key] = round(category[key] * (1 + surge_percent), 2)

            # Save the updated event to the database
            event.save()

            return jsonify({
                'message': 'Surge pricing applied successfully!',
                'status': '200',
                'success': 'true'
            }), 200

        else:
            return jsonify({
                'error': 'Event not found.',
                'status': '404'
            }), 404

    except Exception as e:
        # Handle other exceptions
        error_message = f'An error occurred: {str(e)}'
        return jsonify({'error': error_message}), 500