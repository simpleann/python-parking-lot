from abc import ABC

from constants import VehicleType


class Vehicle(ABC):
    def __init__(self, plate_number, vehicle_type, ticket=None):
        self.__plate_number = plate_number
        self.__type = vehicle_type
        self.__ticket = ticket

    def __repr__(self):
        return ('<Vehicle (plate_number=%r, type=%r)>'
                % (self.__plate_number, self.__type.name))

    def assign_ticket(self, ticket):
        self.__ticket = ticket

    def get_assigned_ticket(self):
        return self.__ticket

    def get_type(self):
        return self.__type


class SmallVehicle(Vehicle):
    def __init__(self, license_number, ticket=None):
        super().__init__(license_number, VehicleType.SMALL, ticket)


class MediumVehicle(Vehicle):
    def __init__(self, license_number, ticket=None):
        super().__init__(license_number, VehicleType.MEDIUM, ticket)


class LargeVehicle(Vehicle):
    def __init__(self, license_number, ticket=None):
        super().__init__(license_number, VehicleType.LARGE, ticket)


# implements the factory patter for creating the Vehicle objects
class VehicleFactory:
    @staticmethod
    def create_vehicle(plate_number, vehicle_size):
        if vehicle_size == VehicleType.SMALL:
            return SmallVehicle(plate_number)
        elif vehicle_size == VehicleType.MEDIUM:
            return MediumVehicle(plate_number)
        elif vehicle_size == VehicleType.LARGE:
            return LargeVehicle(plate_number)
        else:
            raise Exception('Invalid Vehicle Size!')

