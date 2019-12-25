from enum import Enum


class States(Enum):
    S_START = '0'
    S_NEW_USER = '1'
    S_CURRENT_WEATHER = '2'
    S_FORECAST_WEATHER = '3'
    S_STAFF_MODE = '100'
