from collections import OrderedDict

import config

from utils import calculate_time_diff_in_hours
from parking_exceptions import ParkingFullException
from parking_slot import ParkingSlotFactory, ParkingSlotType
from parking_spot_assignment import ParkingSlotAssignmentNearest
from parking_rate import FixedInitialSpotDependentSucceeding
from terminal import EntranceTerminal, ExitTerminal
from parking_ticket import ParkingTicket, ParkingTicketStatus


class Singleton:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class ParkingLot(Singleton):
    __spot_assignment = None
    __parking_rate_calculator = None

    __parking_slots = {}

    __parking_slots_stats_total = {slot_type: 0 for slot_type in ParkingSlotType}
    __parking_slots_stats_available = {slot_type: 0 for slot_type in ParkingSlotType}
    
    __entrance_panels = OrderedDict()  # we want to preserve the order
    __exit_terminals = {}

    __active_tickets = {}

    def __init__(self, name):
        Singleton.__init__(self)
        self.__name = name
        self.parking_rate_calculator = FixedInitialSpotDependentSucceeding()
        self.__generate_terminals(config.INITIAL_NUMBER_OF_ENTRANCES)
        self.__generate_parking_slots(config.INITIAL_PARKING_SLOTS_AND_DISTANCES)
        self.__configure_slot_assignments()

    def __str__(self): return self.__name

    @property
    def spot_assignment(self):
        return self.__spot_assignment

    @spot_assignment.setter
    def spot_assignment(self, spot_assignment):
        self.__spot_assignment = spot_assignment

    @property
    def parking_rate_calculator(self):
        return self.__parking_rate_calculator

    @parking_rate_calculator.setter
    def parking_rate_calculator(self, parking_rate_calculator):
        self.__parking_rate_calculator = parking_rate_calculator

    def __generate_terminals(self, num_of_entrances):
        for i in range(0, num_of_entrances):
            entrance_panel = EntranceTerminal()
            self.add_entrance_panel(entrance_panel)
            exit_terminal = ExitTerminal()
            self.add_exit_terminal(exit_terminal)

    def __generate_parking_slots(self, slots_list):
        # get the list of id's of entrances panels sorted by order of insertion
        entrance_panel_list = [panel[0] for panel in list(self.__entrance_panels.items())]
        for slot_type, slot_distances in slots_list:
            slot = ParkingSlotFactory.create_parking_slot(
                slot_size=ParkingSlotType(slot_type),
                slot_distance_matrix=dict(zip(entrance_panel_list, slot_distances)))
            self.add_parking_slot(slot)

    def __configure_slot_assignments(self):
        self.spot_assignment = ParkingSlotAssignmentNearest(
            terminals=[panel[1] for panel in list(self.__entrance_panels.items())]
        )
        for slot_id, slot_obj in self.__parking_slots.items():
            self.spot_assignment.register_parking_slot(slot_obj)

    def is_full(self, vehicle):
        allowed_slots = self.spot_assignment.get_allowed_slot_types(vehicle.get_type())
        for slot_type, current_stat in list(self.__parking_slots_stats_available.items()):
            if slot_type in allowed_slots and current_stat > 0:
                # there are still available slots for this particular vehicle type
                return False
        # there are no more available slot for this particular vehicle type
        return True

    def get_name(self):
        return self.__name

    def get_entrance_terminals(self):
        # return the list of entrance terminals sorted by order of insertion
        return [panel[1] for panel in list(self.__entrance_panels.items())]

    def get_exit_terminals(self):
        return [terminal[1] for terminal in list(self.__exit_terminals.items())]

    def get_new_parking_ticket(self, vehicle, old_ticket=None, issued_dt=None):
        if self.is_full(vehicle):
            raise ParkingFullException('There are no more available slot for specified vehicle size')

        ticket = ParkingTicket()
        if issued_dt is not None:
            ticket.set_issued_datetime(issued_dt)

        if (old_ticket is not None
                and old_ticket.get_ticket_status() == ParkingTicketStatus.PAID):
            time_interval = calculate_time_diff_in_hours(
                start_dt=old_ticket.get_paid_datetime(),
                end_dt=issued_dt or ticket.get_issued_dt())
            if time_interval < 1:
                ticket.set_issued_datetime(old_ticket.get_issued_dt())
                ticket.set_credited_amount(old_ticket.get_paid_amount() + (old_ticket.get_credited_amount() or 0))

        vehicle.assign_ticket(ticket)
        self.__active_tickets.update({ticket.get_ticket_number(): ticket})
        return ticket

    def release_paid_parking_spot(self, ticket):
        if ticket.get_ticket_status() != ParkingTicketStatus.PAID:
            raise Exception('Attempting to release unpaid spot. Pay ticket amount due first!')
        # get the assigned spot to this ticket
        spot = ticket.get_assigned_spot()
        # remove the vehicle from the spot, making it available again
        spot.remove_vehicle()
        # clear the spot reference in the ticket
        ticket.set_assigned_spot(None)
        # return the spot onto the heap queue for spot assignment
        self.spot_assignment.release_parking_slot(spot)
        # update the parking spots stats
        self.__parking_slots_stats_available[spot.get_type()] += 1

    def park_vehicle(self, terminal, vehicle, timein_dt=None):
        try:
            # print or generate the parking ticket for this vehicle
            ticket = terminal.print_ticket(vehicle, timein_dt)
        except ParkingFullException:
            return print('No more available spots for Vehicle type!')
        # get the assigned spot for the vehicle
        spot = self.spot_assignment.get_parking_slot(terminal, vehicle.get_type())
        # assign the vehicle to the spot (this changes the status of the spot)
        spot.assign_vehicle(vehicle)
        # record the spot assigned to the vehicle in the ticket
        ticket.set_assigned_spot(spot)
        # decrease the number of spots available
        self.__parking_slots_stats_available[spot.get_type()] -= 1
        # return the generated ticket back to the vehicle owner
        return ticket

    def unpark_vehicle(self, terminal, vehicle, timeout_dt=None):
        # get the unpaid ticket from the vehicle owner
        unpaid_ticket = vehicle.get_assigned_ticket()
        # scan the ticket to get the total amount due to be paid
        total_amount_due = terminal.scan_ticket(unpaid_ticket, timeout_dt)
        # pay the total amount due and get the paid ticket (receipt)
        paid_ticket = terminal.process_payment(unpaid_ticket, total_amount_due, paid_dt=timeout_dt)
        # release the spot previously assigned to the paid ticket
        self.release_paid_parking_spot(ticket=paid_ticket)
        return paid_ticket

    def add_entrance_panel(self, entrance_panel):
        entrance_panel.set_parent_parking_lot(self)
        self.__entrance_panels.update({entrance_panel.get_id(): entrance_panel})

    def add_exit_terminal(self, exit_terminal):
        exit_terminal.set_parent_parking_lot(self)
        self.__exit_terminals.update({exit_terminal.get_id(): exit_terminal})

    def add_parking_slot(self, slot):
        # update or insert the slot into the parking slot map
        self.__parking_slots.update({slot.get_id(): slot})
        # update the parking slot stats
        self.__parking_slots_stats_total[slot.get_type()] += 1
        if slot.is_free():
            self.__parking_slots_stats_available[slot.get_type()] += 1

