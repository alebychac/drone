# coding=utf-8


#-------------------------------------------------------------------------------------------------#


import requests

from models.enums import DroneModel, DroneState


#-------------------------------------------------------------------------------------------------#


server_url = "http://127.0.0.1:8000"
base_url = "api/v1"
drones_url = f"{server_url}/{base_url}/drones"
medication_url = f"{server_url}/{base_url}/medications"


#-------------------------------------------------------------------------------------------------#


drone_item_1 = {
    "serial_number": "DR-01",
    "model": DroneModel.light_weight,
    "weight_limit": 125,
    "battery_capacity": 100,
    "state": DroneState.idle,
}


drone_item_2 = {
    "serial_number": "DR-02",
    "model": DroneModel.middle_weight,
    "weight_limit": 250,
    "battery_capacity": 100,
    "state": DroneState.idle,
}

drone_item_3 = {
    "serial_number": "DR-03",
    "model": DroneModel.cruiser_weight,
    "weight_limit": 375,
    "battery_capacity": 100,
    "state": DroneState.idle,
}


drone_item_4 = {
    "serial_number": "DR-04",
    "model": DroneModel.heavy_weight,
    "weight_limit": 500,
    "battery_capacity": 100,
    "state": DroneState.idle,
}


#-------------------------------------------------------------------------------------------------#


medication_item_1 = {
    "name": "metamizol",
    "weight": 50,
    "code": "MET_01",
    "image": "imag met 01",
    # "drone_id": 1,
}


medication_item_2 = {
    "name": "dipirona",
    "weight": 75,
    "code": "DIP_01",
    "image": "imag dip 01",
    # "drone_id": 1,
}


medication_item_3 = {
    "name": "ibuprofeno",
    "weight": 80,
    "code": "IBU_01",
    "image": "imag ibu 01",
    # "drone_id": 1,
}


medication_item_4 = {
    "name": "loratadina",
    "weight": 25,
    "code": "LOR_01",
    "image": "imag lor 01",
    # "drone_id": 1,
}


#-------------------------------------------------------------------------------------------------#


response = requests.post(url=drones_url, json=drone_item_1)
print(response)
print(response.json())
response = requests.post(url=drones_url, json=drone_item_2)
print(response)
print(response.json())
response = requests.post(url=drones_url, json=drone_item_3)
print(response)
print(response.json())
response = requests.post(url=drones_url, json=drone_item_4)
print(response)
print(response.json())


#-------------------------------------------------------------------------------------------------#


response = requests.post(url=medication_url, json=medication_item_1)
print(response)
print(response.json())
response = requests.post(url=medication_url, json=medication_item_2)
print(response)
print(response.json())
response = requests.post(url=medication_url, json=medication_item_3)
print(response)
print(response.json())
response = requests.post(url=medication_url, json=medication_item_4)
print(response)
print(response.json())


#-------------------------------------------------------------------------------------------------#

