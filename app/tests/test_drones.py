# coding=utf-8


#-------------------------------------------------------------------------------------------------#


from app.models import DroneModel, DroneState
from app.tests.config_for_tests import *


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
    "model": DroneModel.light_weight,
    "weight_limit": 125,
    "battery_capacity": 100,
    "state": DroneState.loading,
}


drone_item_3 = {
    "serial_number": "DR-03",
    "model": DroneModel.cruiser_weight,
    "weight_limit": 375,
    "battery_capacity": 100,
    "state": DroneState.loaded,
}


drone_item_4 = {
    "serial_number": "DR-04",
    "model": DroneModel.heavy_weight,
    "weight_limit": 500,
    "battery_capacity": 100,
    "state": DroneState.idle,
}



drone_item_incomplete = {
    "model": DroneModel.light_weight,
    "weight_limit": 125,
    "battery_capacity": 100,
    "state": DroneState.idle,
}


#-------------------------------------------------------------------------------------------------#


def test_get_drone_models(client: TestClient):
    
    response = client.get(f"{base_url}/{drones_url}/models")
    print(response.url)
    assert response.status_code == 200
    assert response.json() == {"drone_models": [model.value for model in DroneModel]}


def test_get_drone_states(client: TestClient):
    
    response = client.get(f"{base_url}/{drones_url}/states")
    print(response.url)
    assert response.status_code == 200
    assert response.json() == {"drone_states": [model.value for model in DroneState]}


#-------------------------------------------------------------------------------------------------#


def test_get_idle_drones(session: Session, client: TestClient):
    
    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    assert response.status_code == 200

    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_2)
    assert response.status_code == 200

    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_3)
    assert response.status_code == 200
    
    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_4)
    assert response.status_code == 200

    response = client.get(f"{base_url}/{drones_url}/")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 4

    
    response = client.get(f"{base_url}/{drones_url}/idle-drones")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["serial_number"] == "DR-01"
    assert data[0]["model"] == DroneModel.light_weight
    assert data[0]["weight_limit"] == 125
    assert data[0]["battery_capacity"] == 100
    assert data[0]["state"] == DroneState.idle

    assert data[1]["serial_number"] == "DR-04"
    assert data[1]["model"] == DroneModel.heavy_weight
    assert data[1]["weight_limit"] == 500
    assert data[1]["battery_capacity"] == 100
    assert data[1]["state"] == DroneState.idle

#-------------------------------------------------------------------------------------------------#


def test_read_drone(session: Session, client: TestClient):
    
    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    assert response.status_code == 200
    data = response.json()


    response = client.get(f"{base_url}/{drones_url}/{data['id']}")

    assert response.status_code == 200
    assert data["serial_number"] == drone_item_1["serial_number"]
    assert data["model"] == drone_item_1["model"]
    assert data["weight_limit"] == drone_item_1["weight_limit"]
    assert data["battery_capacity"] == drone_item_1["battery_capacity"]
    assert data["state"] == drone_item_1["state"]


def test_read_drone_that_doesnt_exists(session: Session, client: TestClient):
    
    response = client.get(f"{base_url}/{drones_url}/{1}")

    assert response.status_code == 404


def test_read_drones(session: Session, client: TestClient):
    
    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    assert response.status_code == 200

    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_2)
    assert response.status_code == 200

    response = client.get(f"{base_url}/{drones_url}/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 2

    assert data[0]["serial_number"] == drone_item_1["serial_number"]
    assert data[0]["model"] == drone_item_1["model"]
    assert data[0]["weight_limit"] == drone_item_1["weight_limit"]
    assert data[0]["battery_capacity"] == drone_item_1["battery_capacity"]
    assert data[0]["state"] == drone_item_1["state"]

    assert data[1]["serial_number"] == drone_item_2["serial_number"]
    assert data[1]["model"] == drone_item_2["model"]
    assert data[1]["weight_limit"] == drone_item_2["weight_limit"]
    assert data[1]["battery_capacity"] == drone_item_2["battery_capacity"]
    assert data[1]["state"] == drone_item_2["state"]


#-------------------------------------------------------------------------------------------------#


def test_update_drone(session: Session, client: TestClient):

    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    data = response.json()
    assert response.status_code == 200
    drone_id = data['id']
    response = client.patch(f"{base_url}/{drones_url}/{drone_id}", json={"weight_limit": 300})

    data = response.json()

    assert response.status_code == 200
    assert data["serial_number"] == drone_item_1["serial_number"]
    assert data["model"] == drone_item_1["model"]
    assert data["weight_limit"] == 300
    assert data["battery_capacity"] == drone_item_1["battery_capacity"]
    assert data["state"] == drone_item_1["state"]
    assert data["id"] == drone_id


def test_update_drone_that_doesnt_exists(session: Session, client: TestClient):
    response = client.patch(f"{base_url}/{drones_url}/{1}", json={"weight_limit": 300})
    assert response.status_code == 404


def test_update_drone_repeated(session: Session, client: TestClient):

    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    assert response.status_code == 200

    data_1 = response.json()
    drone_id_1 = data_1['id']

    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_2)
    assert response.status_code == 200

    response = client.patch(f"{base_url}/{drones_url}/{drone_id_1}", json={"serial_number": drone_item_2["serial_number"]})

    assert response.status_code == 422


def test_update_drone_with_weight_limit_over_limit(client: TestClient):    
    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    assert response.status_code == 200

    data = response.json()
    drone_id = data['id']

    response = client.patch(f"{base_url}/{drones_url}/{drone_id}", json={"weight_limit": 501})
    assert response.status_code == 422


def test_update_drone_with_weight_limit_under_limit(client: TestClient):    
    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    assert response.status_code == 200

    data = response.json()
    drone_id = data['id']

    response = client.patch(f"{base_url}/{drones_url}/{drone_id}", json={"weight_limit": -1})
    assert response.status_code == 422


def test_update_drone_with_battery_capacity_over_limit(client: TestClient):    
    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    assert response.status_code == 200

    data = response.json()
    drone_id = data['id']

    response = client.patch(f"{base_url}/{drones_url}/{drone_id}", json={"battery_capacity": 101})
    assert response.status_code == 422


def test_update_drone_with_battery_capacity_under_limit(client: TestClient):    
    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    assert response.status_code == 200

    data = response.json()
    drone_id = data['id']

    response = client.patch(f"{base_url}/{drones_url}/{drone_id}", json={"battery_capacity": -1})
    assert response.status_code == 422


#-------------------------------------------------------------------------------------------------#


def test_delete_drone(session: Session, client: TestClient):

    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    assert response.status_code == 200

    data = response.json()
    drone_id = data['id']
    
    response = client.delete(f"{base_url}/{drones_url}/{drone_id}")
    assert response.status_code == 200

    response = client.get(f"{base_url}/{drones_url}/{data['id']}")
    assert response.status_code == 404


def test_delete_drone_that_doesnt_exists(session: Session, client: TestClient):
    response = client.delete(f"{base_url}/{drones_url}/{1}")
    assert response.status_code == 404


#-------------------------------------------------------------------------------------------------#


def test_create_drone(client: TestClient):
    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    data = response.json()
    
    assert response.status_code == 200
    assert data["serial_number"] == drone_item_1["serial_number"]
    assert data["model"] == drone_item_1["model"]
    assert data["weight_limit"] == drone_item_1["weight_limit"]
    assert data["battery_capacity"] == drone_item_1["battery_capacity"]
    assert data["state"] == drone_item_1["state"]


def test_create_drone_repated(client: TestClient):
    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    data = response.json()
    
    assert response.status_code == 200
    assert data["serial_number"] == drone_item_1["serial_number"]
    assert data["model"] == drone_item_1["model"]
    assert data["weight_limit"] == drone_item_1["weight_limit"]
    assert data["battery_capacity"] == drone_item_1["battery_capacity"]
    assert data["state"] == drone_item_1["state"]

    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    assert response.status_code == 422


def test_create_drone_incomplete(client: TestClient):
    response = client.post(f"{base_url}/{drones_url}", json=drone_item_incomplete)
    assert response.status_code == 422


def test_create_drone_invalid(client: TestClient):
    drone_item_1["serial_number"] = "s"*101
    response = client.post(
        f"{base_url}/{drones_url}",
        json=drone_item_1,
    )
    assert response.status_code == 422


def test_create_drone_with_weight_limit_over_limit(client: TestClient):
    drone_item_1["weight_limit"] = 501
    response = client.post(
        f"{base_url}/{drones_url}",
        json=drone_item_1,
    )
    assert response.status_code == 422


def test_create_drone_with_weight_limit_under_limit(client: TestClient):
    drone_item_1["weight_limit"] = -1
    response = client.post(
        f"{base_url}/{drones_url}",
        json=drone_item_1,
    )
    assert response.status_code == 422


def test_create_drone_with_weight_limit_over_limit(client: TestClient):
    drone_item_1["battery_capacity"] = 101
    response = client.post(
        f"{base_url}/{drones_url}",
        json=drone_item_1,
    )
    assert response.status_code == 422


def test_create_drone_with_weight_limit_under_limit(client: TestClient):
    drone_item_1["battery_capacity"] = -1
    response = client.post(
        f"{base_url}/{drones_url}",
        json=drone_item_1,
    )
    assert response.status_code == 422


#-------------------------------------------------------------------------------------------------#


