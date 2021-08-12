from datetime import datetime

from constants import DATETIME_FORMAT
from vehicle import VehicleFactory, VehicleType
from parking_lot import ParkingLot


def print_ticket_details(ticket):
    pass


if __name__ == "__main__":

    # create the parking lot object
    parking_lot_obj = ParkingLot(name='OOP-Parking-Lot')

    print('\nList of Parking Entrance Terminals:')
    # list of entrances first terminal is [0], [1], ...
    entrance_terminals = parking_lot_obj.get_entrance_terminals()
    for idx, val in enumerate(entrance_terminals):
        print('Entrance Terminal {idx}: <{val}>'.format(idx=idx, val=val.get_id()))

    print('\nList of Parking Exit Terminals:')
    # list of exits first terminal is [0], [1], ...
    exit_terminals = parking_lot_obj.get_exit_terminals()
    for idx, val in enumerate(exit_terminals):
        print('Exit Terminal {idx}: <{val}>'.format(idx=idx, val=val.get_id()))

    # # Use-Case 01: Terminal (Entrance|Exit Point) no less than 3
    # print('\n\nUse-Case 01: Terminal Entrance|Exit Point no less than 3')
    # case01_vL_02 = VehicleFactory.create_vehicle('DAM6943', VehicleType(2))
    # case01_vL_02_unpaid_ticket_01 = parking_lot_obj.park_vehicle(
    #     terminal=entrance_terminals[0],
    #     vehicle=case01_vL_02,
    #     timein_dt=datetime.strptime('10/08/2021 08:30:00', DATETIME_FORMAT))
    # print('\ncase01_vL_02_unpaid_ticket_01 -> {0}'.format(case01_vL_02_unpaid_ticket_01))
    #
    # # case01_vL_02_paid_ticket_01 = parking_lot_obj.unpark_vehicle(
    # #     terminal=exit_terminals[0],
    # #     vehicle=case01_vL_01,
    # #     timeout_dt=datetime.strptime('10/08/2021 9:45:00', DATETIME_FORMAT))
    # # print('\case01_vL_02_paid_ticket_01 -> {0}'.format(case01_vL_02_paid_ticket_01))
    #
    # case01_vL_01 = VehicleFactory.create_vehicle('ABC1234', VehicleType(1))
    # case01_vL_01_unpaid_ticket_02 = parking_lot_obj.park_vehicle(
    #     terminal=entrance_terminals[1],
    #     vehicle=case01_vL_01,
    #     timein_dt=datetime.strptime('10/08/2021 08:30:00', DATETIME_FORMAT))
    # print('\ncase01_vL_01_unpaid_ticket_02 -> {0}'.format(case01_vL_01_unpaid_ticket_02))
    #
    # # case01_vL_01_paid_ticket_02 = parking_lot_obj.unpark_vehicle(
    # #     terminal=exit_terminals[0],
    # #     vehicle=case01_vL_02,
    # #     timeout_dt=datetime.strptime('10/08/2021 10:45:00', DATETIME_FORMAT))
    # # print('\case01_vL_01_paid_ticket_02 -> {0}'.format(case01_vL_01_paid_ticket_02))
    #
    #
    # case01_vL_00 = VehicleFactory.create_vehicle('DEF4567', VehicleType(0))
    # case01_vL_00_unpaid_ticket_03 = parking_lot_obj.park_vehicle(
    #     terminal=entrance_terminals[2],
    #     vehicle=case01_vL_00,
    #     timein_dt=datetime.strptime('10/08/2021 08:30:00', DATETIME_FORMAT))
    # print('\ncase03_vL_00_unpaid_ticket_03 -> {0}'.format(case01_vL_00_unpaid_ticket_03))
    #
    # # case01_vL_00_paid_ticket_03 = parking_lot_obj.unpark_vehicle(
    # #     terminal=exit_terminals[2],
    # #     vehicle=case01_vL_03,
    # #     timeout_dt=datetime.strptime('10/08/2021 12:45:00', DATETIME_FORMAT))
    # # print('\case01_vL_00_paid_ticket_03 -> {0}'.format(case01_vL_00_paid_ticket_03))
    # pass
    #
    # # Use-Case 02: Vehicle parks and then unparks within the initial fixed period
    # print('\n\nCase02: Small Vehicle parks in Medium Slot and then unparks within the initial fixed period')
    # case02_vL_00 = VehicleFactory.create_vehicle('GHI9012', VehicleType(0))
    # case02_vL_00_unpaid_ticket_01 = parking_lot_obj.park_vehicle(
    #     terminal=entrance_terminals[0],
    #     vehicle=case02_vL_00,
    #     timein_dt=datetime.strptime('11/08/2021 10:00:00', DATETIME_FORMAT))
    # print('\ncase02_vL_00_unpaid_ticket_01 -> {0}'.format(case02_vL_00_unpaid_ticket_01))
    #
    # case02_vL_00_paid_ticket_01 = parking_lot_obj.unpark_vehicle(
    #     terminal=exit_terminals[0],
    #     vehicle=case02_vL_00,
    #     timeout_dt=datetime.strptime('11/08/2021 12:45:00', DATETIME_FORMAT))
    # print('\ncase02_vL_00_paid_ticket_01 -> {0}'.format(case02_vL_00_paid_ticket_01))
    # pass

    # Use-Case 03: Vehicle parks and then unparks within the continuous rate and 24 hours
    print('\n\nCase03: Small Vehicle parks in Medium Spot and then unparks with the continuous rate & 24hrs')
    case03_vL_00 = VehicleFactory.create_vehicle('GHI9012', VehicleType(0))
    case03_vL_00_unpaid_ticket_01 = parking_lot_obj.park_vehicle(
        terminal=entrance_terminals[2],
        vehicle=case03_vL_00,
        timein_dt=datetime.strptime('10/08/2021 08:30:00', DATETIME_FORMAT))
    print('\ncase03_vL_00_unpaid_ticket_01 -> {0}'.format(case03_vL_00_unpaid_ticket_01))

    case03_vL_00_paid_ticket_01 = parking_lot_obj.unpark_vehicle(
        terminal=exit_terminals[0],
        vehicle=case03_vL_00,
        timeout_dt=datetime.strptime('10/08/2021 13:45:00', DATETIME_FORMAT))
    print('\ncase03_vL_00_paid_ticket_01 -> {0}'.format(case03_vL_00_unpaid_ticket_01))

    case03_vL_00_unpaid_ticket_02 = parking_lot_obj.park_vehicle(
        terminal=entrance_terminals[1],
        vehicle=case03_vL_00,
        timein_dt=datetime.strptime('10/08/2021 14:30:00', DATETIME_FORMAT))
    print('\ncase03_vL_00_unpaid_ticket_02 -> {0}'.format(case03_vL_00_unpaid_ticket_02))

    case03_vL_00_paid_ticket_02 = parking_lot_obj.unpark_vehicle(
        terminal=exit_terminals[0],
        vehicle=case03_vL_00,
        timeout_dt=datetime.strptime('10/08/2021 17:30:00', DATETIME_FORMAT))
    print('\ncase03_vL_00_paid_ticket_02 -> {0}'.format(case03_vL_00_paid_ticket_02))
    #
    # case03_vL_00_unpaid_ticket_03 = parking_lot_obj.park_vehicle(
    #     terminal=entrance_terminals[2],
    #     vehicle=case03_vL_00,
    #     timein_dt=datetime.strptime('10/08/2021 18:20:00', DATETIME_FORMAT))
    # print('\ncase03_vL_00_unpaid_ticket_03 -> {0}'.format(case03_vL_00_unpaid_ticket_03))
    #
    # case03_vL_00_paid_ticket_03 = parking_lot_obj.unpark_vehicle(
    #     terminal=exit_terminals[0],
    #     vehicle=case03_vL_00,
    #     timeout_dt=datetime.strptime('11/08/2021 13:30:00', DATETIME_FORMAT))
    # print('\ncase03_vL_00_paid_ticket_03 -> {0}'.format(case03_vL_00_paid_ticket_03))

    # case03_vL_00_unpaid_ticket_04 = parking_lot_obj.park_vehicle(
    #     terminal=entrance_terminals[2],
    #     vehicle=case03_vL_00,
    #     timein_dt=datetime.strptime('11/08/2021 15:30:00', DATETIME_FORMAT))
    # print('\ncase03_vL_00_unpaid_ticket_04 -> {0}'.format(case03_vL_00_unpaid_ticket_04))
    #
    # case03_vL_00_paid_ticket_04 = parking_lot_obj.unpark_vehicle(
    #     terminal=exit_terminals[0],
    #     vehicle=case03_vL_00,
    #     timeout_dt=datetime.strptime('11/08/2021 17:30:00', DATETIME_FORMAT))
    # print('\ncase03_vL_00_paid_ticket_04 -> {0}'.format(case03_vL_00_paid_ticket_04))
    pass
    #
    # # Use-Case 04: Full Parking
    # print('\n\nCase04: Full Parking')
    # case04_vL_01 = VehicleFactory.create_vehicle('JKL3456', VehicleType(1))
    # case04_vL_01_unpaid_ticket_01 = parking_lot_obj.park_vehicle(
    #     terminal=entrance_terminals[1],
    #     vehicle=case04_vL_01,
    #     timein_dt=datetime.strptime('10/08/2021 08:30:00', DATETIME_FORMAT))
    # print('\ncase04_vL_01_unpaid_ticket_01 -> {0}'.format(case04_vL_01_unpaid_ticket_01))
    # pass

    # # Use-Case 05: Small vehicles can park in Medium Spot parking spaces;
    # print('\n\nCase05: Small vehicles can park in Medium Size Spot')
    # case05_vL_00 = VehicleFactory.create_vehicle('MNO7890', VehicleType(0))
    # case05_vL_00_unpaid_ticket_01 = parking_lot_obj.park_vehicle(
    #     terminal=entrance_terminals[1],
    #     vehicle=case05_vL_00,
    #     timein_dt=datetime.strptime('10/08/2021 08:30:00', DATETIME_FORMAT))
    # print('\ncase05_vL_00_unpaid_ticket_01 -> {0}'.format(case05_vL_00_unpaid_ticket_01))
    # pass
    #
    # # Use-Case 06: Small vehicles can park in Large Spot parking spaces;
    # print('\n\nCase06: Small vehicles can park in Large Size Spot')
    # case06_vL_00 = VehicleFactory.create_vehicle('PQR1234', VehicleType(0))
    # case06_vL_00_unpaid_ticket_01 = parking_lot_obj.park_vehicle(
    #     terminal=entrance_terminals[1],
    #     vehicle=case06_vL_00,
    #     timein_dt=datetime.strptime('10/08/2021 09:30:00', DATETIME_FORMAT))
    # print('\ncase06_vL_00_unpaid_ticket_01 -> {0}'.format(case06_vL_00_unpaid_ticket_01))
    # pass
    #
    # # Use-Case 07: Medium vehicles can park in Large Spot parking spaces;
    # print('\n\nCase07: Medium vehicles can park in Large Size Spot')
    # case07_vL_01 = VehicleFactory.create_vehicle('STU5678', VehicleType(1))
    # case07_vL_01_unpaid_ticket_01 = parking_lot_obj.park_vehicle(
    #     terminal=entrance_terminals[1],
    #     vehicle=case07_vL_01,
    #     timein_dt=datetime.strptime('10/08/2021 10:30:00', DATETIME_FORMAT))
    # print('\ncase07_vL_01_unpaid_ticket_01 -> {0}'.format(case07_vL_01_unpaid_ticket_01))
    # pass