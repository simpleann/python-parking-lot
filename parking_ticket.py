import uuid
import datetime

from constants import ParkingTicketStatus


class ParkingTicket:

    def __init__(self):
        self.__ticket_number = str(uuid.uuid4())[:8]
        self.__ticket_status = ParkingTicketStatus.ACTIVE
        self.__spot_assigned = None
        self.__issued_at = datetime.datetime.now()
        self.__issuing_terminal_id = None
        self.__paid_at = None
        self.__total_credited_amount = None
        self.__total_paid_amount = None
        self.__total_hours_incurred = None
        self.__paying_terminal_id = None

    def __repr__(self):
        return (
            '<ParkingTicket ('
            'number=%r, status=%r, issued_dt=%r, issuing_terminal=%r, spot_assigned=%r, '
            'paid_dt=%r, paying_terminal=%r, total_hours=%r, total_paid=%r, total_credited=%r'
            ')>'
            % (self.__ticket_number, self.__ticket_status.name,
               self.__issued_at, self.__issuing_terminal_id, self.__spot_assigned,
               self.__paid_at, self.__paying_terminal_id, self.__total_hours_incurred,
               self.__total_paid_amount, self.__total_credited_amount))

    def get_ticket_number(self):
        return self.__ticket_number

    def set_assigned_spot(self, spot):
        self.__spot_assigned = spot

    def get_assigned_spot(self):
        return self.__spot_assigned

    def get_issued_dt(self):
        return self.__issued_at

    def set_issued_datetime(self, issued_dt):
        self.__issued_at = issued_dt

    def set_paid_datetime(self, paid_dt):
        self.__paid_at = paid_dt

    def get_paid_datetime(self):
        return self.__paid_at

    def get_paid_amount(self):
        return self.__total_paid_amount

    def set_paid_amount(self, amount_due):
        # in case this ticket has already been paid with some amount before,
        # we add the old paid amount with the new amount paid
        if self.__total_paid_amount is not None:
            self.__total_paid_amount += amount_due
        # else, we just set the current amount paid
        else:
            self.__total_paid_amount = amount_due

    def set_paying_terminal(self, exit_terminal_id):
        self.__paying_terminal_id = exit_terminal_id

    def set_issuing_terminal(self, entrance_terminal_id):
        self.__issuing_terminal_id = entrance_terminal_id

    def set_ticket_status(self, status):
        self.__ticket_status = status

    def get_ticket_status(self):
        return self.__ticket_status

    def set_total_hours_incurred(self, total_hours):
        self.__total_hours_incurred = total_hours

    def get_credited_amount(self):
        return self.__total_credited_amount

    def set_credited_amount(self, amount):
        self.__total_credited_amount = amount
