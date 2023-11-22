#-------------------------------------------------------------------------------------------------#

# coding=utf-8


#-------------------------------------------------------------------------------------------------#


from enum import Enum


#-------------------------------------------------------------------------------------------------#


class DroneModel(str, Enum):
    light_weight = "Lightweight"
    middle_weight = "Middleweight"
    cruiser_weight = "Cruiserweight"
    heavy_weight = "Heavyweight"


class DroneState(str, Enum):
    idle = "IDLE"
    loading = "LOADING"
    loaded = "LOADED"
    delivering = "DELIVERING"
    delivered = "DELIVERED"
    returning = "RETURNING"


#-------------------------------------------------------------------------------------------------#

