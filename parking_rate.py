from abc import ABC, abstractmethod
import math

from constants import ParkingSlotType


class ParkingRate:

    def __init__(self, hour_number, rate_per_hour_number):
        self.__hour_number = hour_number
        self.__rate_per_hour_number = rate_per_hour_number

    def get_hour_number(self):
        return self.__hour_number

    def get_rate_per_hour_number(self):
        return self.__rate_per_hour_number


class ParkingRateScheme(ABC):
    @abstractmethod
    def calculate_parking_rate(self, hours_accrued, spot_type):
        pass


class FixedInitialSpotDependentSucceeding(ParkingRateScheme):
    def __init__(self):
        self.__initial_hours_rate = ParkingRate(
            hour_number=3, rate_per_hour_number=40)
        self.__succeeding_hours_rate = dict({
            ParkingSlotType.SMALL: ParkingRate(
                hour_number=1, rate_per_hour_number=20),
            ParkingSlotType.MEDIUM: ParkingRate(
                hour_number=1, rate_per_hour_number=60),
            ParkingSlotType.LARGE: ParkingRate(
                hour_number=1, rate_per_hour_number=100
            )
        })
        self.__more_than_24hours_rate = ParkingRate(
            hour_number=24, rate_per_hour_number=5000
        )

    def calculate_parking_rate(self, total_hours_accrued, spot_type):
        # total hours accrued must always be rounded-up
        total_hours = math.ceil(total_hours_accrued)
        total_amount = 0

        hours_exceeding_24hours = math.floor(total_hours / self.__more_than_24hours_rate.get_hour_number())
        if hours_exceeding_24hours > 0:
            total_amount += hours_exceeding_24hours * self.__more_than_24hours_rate.get_rate_per_hour_number()
            total_hours = total_hours % self.__more_than_24hours_rate.get_hour_number()

        if total_hours <= self.__initial_hours_rate.get_hour_number():
            return total_amount + self.__initial_hours_rate.get_rate_per_hour_number()

        # get the number of succeeding hours after initial hours
        succeeding_hours = total_hours - self.__initial_hours_rate.get_hour_number()
        # get the rate for the succeeding hours which depends on the spot type taken
        succeeding_hours_rate = self.__succeeding_hours_rate[spot_type]

        # calculate the total amount (initial + succeeding)
        total_amount += (
                self.__initial_hours_rate.get_rate_per_hour_number()
                + succeeding_hours_rate.get_rate_per_hour_number()
                * succeeding_hours
        )

        return total_amount
