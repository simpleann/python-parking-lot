from uuid import uuid4
from datetime import datetime

from utils import calculate_time_diff_in_hours
from constants import ParkingTicketStatus


class Terminal:

    def __init__(self):
        self.__id = str(uuid4())[:8]
        self.__parent_parking_lot = None

    def get_id(self):
        return self.__id

    def set_parent_parking_lot(self, parking_lot):
        self.__parent_parking_lot = parking_lot

    def get_parent_parking_lot(self):
        return self.__parent_parking_lot


class EntranceTerminal(Terminal):
    def print_ticket(self, vehicle, issued_dt=None):
        ticket = self.get_parent_parking_lot().get_new_parking_ticket(
            vehicle=vehicle,
            old_ticket=vehicle.get_assigned_ticket(),
            issued_dt=issued_dt)
        ticket.set_issuing_terminal(self.get_id())
        return ticket


class ExitTerminal(Terminal):

    def scan_ticket(self, ticket, scanned_dt=None):
        # get the total hours accrued
        total_hours = calculate_time_diff_in_hours(
            start_dt=ticket.get_issued_dt(),
            end_dt=scanned_dt or datetime.now())
        ticket.set_total_hours_incurred(total_hours)

        # calculate the total amount based on the parking rate
        total_amount = self.get_parent_parking_lot().parking_rate_calculator.calculate_parking_rate(
            total_hours_accrued=total_hours,
            spot_type=ticket.get_assigned_spot().get_type()
        )

        # adjust total amount in case ticket has some remaining credit
        total_amount = total_amount - (ticket.get_credited_amount() or 0)

        return total_amount

    def process_payment(self, ticket, amount_due, paid_dt=None):
        ticket.set_paid_amount(amount_due)
        ticket.set_paid_datetime(paid_dt or datetime.now())
        ticket.set_paying_terminal(self.get_id())
        ticket.set_ticket_status(ParkingTicketStatus.PAID)
        return ticket
