from abc import ABC, abstractmethod
import heapq

from constants import VehicleType, ParkingSlotType, ParkingSlotStatus


class ParkingSlotAssignment(ABC):

    @abstractmethod
    def __init__(self, terminals):
        pass

    @abstractmethod
    def register_parking_slot(self, slot):
        pass

    @abstractmethod
    def get_parking_slot(self, terminal, vehicle_type):
        pass

    @abstractmethod
    def release_parking_slot(self, slot):
        pass

    @abstractmethod
    def get_allowed_slot_types(self, vehicle_type):
        pass


class ParkingSlotAssignmentNearest(ParkingSlotAssignment):
    __terminal_spots_reserved = {}
    __terminal_spots_available = {}
    __terminal_spots_heap = {}

    def __init__(self, terminals):
        for terminal in terminals:
            self.__terminal_spots_reserved[terminal.get_id()] = {}
            self.__terminal_spots_available[terminal.get_id()] = {}
            self.__terminal_spots_heap[terminal.get_id()] = dict({
                VehicleType.SMALL: [],      # will contain small, medium and large slots
                VehicleType.MEDIUM: [],     # will contain medium and large slots only
                VehicleType.LARGE: []       # will contain large slots only
            })

    def register_parking_slot(self, slot):
        for terminal_id in self.__terminal_spots_heap.keys():
            # extract the slot distance relative to each entrance terminals
            slot_distance = slot.get_distance(terminal_id)
            # prepare the slot entry to be inserted into the min-heap on each entrance terminal
            slot_entry = [slot_distance, slot, ParkingSlotStatus.AVAILABLE]
            # insert the slot entry to the available slots map of each terminal
            self.__terminal_spots_available[terminal_id][slot.get_id()] = slot_entry
            # push the slot entry to each entrance terminal
            self.__push_slot_entry_to_terminal_heap(terminal_id, slot_entry)

    def get_parking_slot(self, entrance_terminal, vehicle_type):
        terminal_id = entrance_terminal.get_id()
        while self.__terminal_spots_heap[terminal_id][vehicle_type]:
            slot_distance, slot, status = heapq.heappop(
                self.__terminal_spots_heap[terminal_id][vehicle_type])

            if status is not ParkingSlotStatus.RESERVED:
                self.__mark_slot_as_reserved(slot)
                return slot

        raise KeyError("Pop from an empty list of slots")

    def release_parking_slot(self, slot):
        for terminal_id in self.__terminal_spots_heap.keys():
            # remove the slot from the reserved slots map of each terminal
            slot_entry = self.__terminal_spots_reserved[terminal_id].pop(slot.get_id())
            # change the status of the slot back to available
            slot_entry[-1] = ParkingSlotStatus.AVAILABLE
            # re-insert slot back to the available slots map
            self.__terminal_spots_available[terminal_id][slot.get_id()] = slot_entry
            # rehash the min heap across all terminals
            self.__push_slot_entry_to_terminal_heap(terminal_id, slot_entry)

    def get_allowed_slot_types(self, vehicle_type):
        if vehicle_type == VehicleType.SMALL:
            return [ParkingSlotType.SMALL, ParkingSlotType.MEDIUM, ParkingSlotType.LARGE]
        elif vehicle_type == VehicleType.MEDIUM:
            return [ParkingSlotType.MEDIUM, ParkingSlotType.LARGE]
        elif vehicle_type == VehicleType.LARGE:
            return [ParkingSlotType.LARGE]
        else:
            raise Exception('Invalid Vehicle Type!')

    def __mark_slot_as_reserved(self, slot):
        for terminal_id in self.__terminal_spots_available.keys():
            # remove the slot from the available slots on each terminal
            slot_entry = self.__terminal_spots_available[terminal_id].pop(slot.get_id())
            # mark the slot entry as RESERVED so it will be skipped on each terminals heap map
            slot_entry[-1] = ParkingSlotStatus.RESERVED
            # move the slot entry to the reserved slots of each terminal
            self.__terminal_spots_reserved[terminal_id][slot.get_id()] = slot_entry

    def __push_slot_entry_to_terminal_heap(self, terminal_id, slot_entry):
        slot = slot_entry[1]  # second item on the list which is the slot object
        slot_type = slot.get_type()
        if slot_type == ParkingSlotType.SMALL:
            heapq.heappush(self.__terminal_spots_heap[terminal_id][VehicleType.SMALL], slot_entry)
        elif slot_type == ParkingSlotType.MEDIUM:
            heapq.heappush(self.__terminal_spots_heap[terminal_id][VehicleType.SMALL], slot_entry)
            heapq.heappush(self.__terminal_spots_heap[terminal_id][VehicleType.MEDIUM], slot_entry)
        elif slot_type == ParkingSlotType.LARGE:
            heapq.heappush(self.__terminal_spots_heap[terminal_id][VehicleType.SMALL], slot_entry)
            heapq.heappush(self.__terminal_spots_heap[terminal_id][VehicleType.MEDIUM], slot_entry)
            heapq.heappush(self.__terminal_spots_heap[terminal_id][VehicleType.LARGE], slot_entry)
        else:
            raise Exception("Invalid Slot Type!")
