from abc import ABC
from uuid import uuid4

from constants import ParkingSlotType


class ParkingSlot(ABC):
    __distance_to_entrance_panels = {}

    def __init__(self, parking_slot_type):
        self.__id = str(uuid4())[:8]
        self.__free = True
        self.__vehicle = None
        self.__parking_slot_type = parking_slot_type

    def __repr__(self):
        return ('<ParkingSlot (id=%r, size=%r, is_free=%r, vehicle_assigned=%r)>'
                % (self.__id, self.__parking_slot_type.name,
                   self.__free, self.__vehicle))

    def is_free(self):
        return self.__free

    def assign_vehicle(self, vehicle):
        self.__vehicle = vehicle
        self.__free = False

    def remove_vehicle(self):
        self.__vehicle = None
        self.__free = True

    def get_id(self):
        return self.__id

    def get_type(self):
        return self.__parking_slot_type

    def get_distance(self, entrance_terminal_id):
        return self.__distance_to_entrance_panels.get(entrance_terminal_id)

    def set_distance_matrix(self, distance_matrix):
        self.__distance_to_entrance_panels = distance_matrix


class SmallSlot(ParkingSlot):
    def __init__(self):
        super().__init__(ParkingSlotType.SMALL)


class MediumSlot(ParkingSlot):
    def __init__(self):
        super().__init__(ParkingSlotType.MEDIUM)


class LargeSlot(ParkingSlot):
    def __init__(self):
        super().__init__(ParkingSlotType.LARGE)


class ParkingSlotFactory:
    @staticmethod
    def create_parking_slot(slot_size, slot_distance_matrix):
        if slot_size == ParkingSlotType.SMALL:
            slot = SmallSlot()
            slot.set_distance_matrix(slot_distance_matrix)
            return slot
        elif slot_size == ParkingSlotType.MEDIUM:
            slot = MediumSlot()
            slot.set_distance_matrix(slot_distance_matrix)
            return slot
        elif slot_size == ParkingSlotType.LARGE:
            slot = LargeSlot()
            slot.set_distance_matrix(slot_distance_matrix)
            return slot
        else:
            raise Exception('Invalid parking slot size')
