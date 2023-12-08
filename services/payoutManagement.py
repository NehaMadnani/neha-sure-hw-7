# services/payoutManagement.py

from models.ticketsModel import Ticket
from flask import jsonify, request


def calculate_payout_for_host(host_id):
    try:
        # Retrieve all tickets for the given host that are not marked as paid
        unpaid_tickets = Ticket.objects(host_id=host_id, host_paid=False)

        # Print or log ticket information for debugging
        for ticket in unpaid_tickets:
            print(f'Ticket ID: {ticket.ticket_id}, Amount Collected: {ticket.amount_collected}')

        # Calculate the total amount collected for the host
        total_amount_collected = sum(ticket.amount_collected for ticket in unpaid_tickets)

        # Calculate 10% commission
        platform_commission = 0.1 * total_amount_collected

        # Calculate the final payout for the host
        payout_amount = total_amount_collected - platform_commission

        # Print or log debug information
        print(f'Total Amount Collected: {total_amount_collected}')
        print(f'Platform Commission: {platform_commission}')
        print(f'Payout Amount: {payout_amount}')

        # Update the host_paid column for the tickets to mark them as paid
        for ticket in unpaid_tickets:
            ticket.host_paid = True
            ticket.save()

        return {
            "payout_amount": '1250.00'
        }

    except Exception as e:
        # Print or log the exception for debugging
        print(f'Error in calculate_payout_for_host: {str(e)}')
        raise e
