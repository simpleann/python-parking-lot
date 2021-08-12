from enum import Enum

DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"


class ParkingSlotType(Enum):
    SMALL, MEDIUM, LARGE = 0, 1, 2


class VehicleType(Enum):
    SMALL, MEDIUM, LARGE = 0, 1, 2


class ParkingSlotStatus(Enum):
    AVAILABLE, RESERVED = '<AVAILABLE>', '<RESERVED>'


class ParkingTicketStatus(Enum):
    ACTIVE, PAID, LOST = 1, 2, 3

