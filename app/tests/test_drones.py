# coding=utf-8


#-------------------------------------------------------------------------------------------------#


from app.tests.config_for_tests import *


#-------------------------------------------------------------------------------------------------#


def test_get_drone_models(client: TestClient):
    
    response = client.get(f"{base_url}/{drones_url}/models")
    print(response.url)
    assert response.status_code == 200
    assert response.json() == {"drone_models": [model.value for model in DroneModel]}


def test_get_drone_states(client: TestClient):
    
    response = client.get(f"{base_url}/{drones_url}/states")
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


#-------------------------------------------------------------------------------------------------#


def test_get_available_cargo_weight_for_empty_drone(session: Session, client: TestClient):   

    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    assert response.status_code == 200
    drone_data = response.json()

    response = client.get(f"{base_url}/{drones_url}/{drone_data['serial_number']}/available_cargo_weight")
    assert response.status_code == 200
    data = response.json()

    assert {f"available_cargo_weight for drone '{drone_data['serial_number']}'": drone_data['weight_limit']} == data


def test_get_available_cargo_weight_for_drone_that_doesnt_exists(session: Session, client: TestClient):   
    response = client.get(f"{base_url}/{drones_url}/DR-01/available_cargo_weight")
    assert response.status_code == 404


def test_get_available_cargo_weight(session: Session, client: TestClient):   

    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    assert response.status_code == 200
    drone_data = response.json()
    
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    assert response.status_code == 200
    med_data = response.json()
    
    response = client.post(f"{base_url}/{medications_url}/{med_data['code']}/link-drone/{drone_data['serial_number']}")
    assert response.status_code == 200

    response = client.get(f"{base_url}/{drones_url}/{drone_data['serial_number']}/available_cargo_weight")
    assert response.status_code == 200
    data = response.json()
    
    query_drone = select(Drone).where(Drone.serial_number == drone_data['serial_number'])
    drone = session.exec(query_drone).first()
    available_cargo_weight = drone.weight_limit - sum([med.weight for med in drone.medications])

    assert {f"available_cargo_weight for drone '{drone_data['serial_number']}'": available_cargo_weight} == data


def test_get_available_cargo_weight_to_get_0_cargo_weigth_available(session: Session, client: TestClient):   

    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    assert response.status_code == 200
    drone_data = response.json()
    
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    assert response.status_code == 200
    med_data = response.json()
    
    response = client.post(f"{base_url}/{medications_url}/{med_data['code']}/link-drone/{drone_data['serial_number']}")
    assert response.status_code == 200

    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_2)
    assert response.status_code == 200
    med_data = response.json()
    
    response = client.post(f"{base_url}/{medications_url}/{med_data['code']}/link-drone/{drone_data['serial_number']}")
    assert response.status_code == 200

    response = client.get(f"{base_url}/{drones_url}/{drone_data['serial_number']}/available_cargo_weight")
    assert response.status_code == 200
    data = response.json()
    
    query_drone = select(Drone).where(Drone.serial_number == drone_data['serial_number'])
    drone = session.exec(query_drone).first()
    available_cargo_weight = drone.weight_limit - sum([med.weight for med in drone.medications])

    assert {f"available_cargo_weight for drone '{drone_data['serial_number']}'": 0} == data


#-------------------------------------------------------------------------------------------------#


def test_get_drone_medications_1_medication(session: Session, client: TestClient):   

    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    assert response.status_code == 200
    drone_data = response.json()
    
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    assert response.status_code == 200
    med_data = response.json()
    
    response = client.post(f"{base_url}/{medications_url}/{med_data['code']}/link-drone/{drone_data['serial_number']}")
    assert response.status_code == 200

    response = client.get(f"{base_url}/{drones_url}/{drone_data['serial_number']}/medications")
    assert response.status_code == 200
    data = response.json()
    
    query_drone = select(Drone).where(Drone.serial_number == drone_data['serial_number'])
    drone = session.exec(query_drone).first()
    medications = drone.medications

    assert medications[0].id == data[0]["id"]
    assert medications[0].name == data[0]["name"]
    assert medications[0].code == data[0]["code"]
    assert medications[0].weight == data[0]["weight"]
    assert medications[0].image == data[0]["image"]


def test_get_drone_medications_2_medication(session: Session, client: TestClient):   

    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    assert response.status_code == 200
    drone_data = response.json()
    
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    assert response.status_code == 200
    med_data = response.json()
    
    response = client.post(f"{base_url}/{medications_url}/{med_data['code']}/link-drone/{drone_data['serial_number']}")
    assert response.status_code == 200
    
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_2)
    assert response.status_code == 200
    med_data = response.json()
    
    response = client.post(f"{base_url}/{medications_url}/{med_data['code']}/link-drone/{drone_data['serial_number']}")
    assert response.status_code == 200

    response = client.get(f"{base_url}/{drones_url}/{drone_data['serial_number']}/medications")
    assert response.status_code == 200
    data = response.json()
    
    query_drone = select(Drone).where(Drone.serial_number == drone_data['serial_number'])
    drone = session.exec(query_drone).first()
    medications = drone.medications

    assert medications[0].id == data[0]["id"]
    assert medications[0].name == data[0]["name"]
    assert medications[0].code == data[0]["code"]
    assert medications[0].weight == data[0]["weight"]
    assert medications[0].image == data[0]["image"]

    assert medications[1].id == data[1]["id"]
    assert medications[1].name == data[1]["name"]
    assert medications[1].code == data[1]["code"]
    assert medications[1].weight == data[1]["weight"]
    assert medications[1].image == data[1]["image"]


def test_get_drone_medications_for_drone_that_doesnt_exists(session: Session, client: TestClient):   

    response = client.get(f"{base_url}/{drones_url}/DR-01/medications")
    assert response.status_code == 404


#-------------------------------------------------------------------------------------------------#


def test_read_drone_by_serial_number(session: Session, client: TestClient):
    
    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    drone_serial_number = response.json()["serial_number"]
    assert response.status_code == 200

    response = client.get(f"{base_url}/{drones_url}/serial_number/{drone_serial_number}")
    data = response.json()

    assert response.status_code == 200
    assert data["serial_number"] == drone_item_1["serial_number"]
    assert data["model"] == drone_item_1["model"]
    assert data["weight_limit"] == drone_item_1["weight_limit"]
    assert data["battery_capacity"] == drone_item_1["battery_capacity"]
    assert data["state"] == drone_item_1["state"]


def test_read_drone_by_serial_number_that_doesnt_exists(session: Session, client: TestClient):
    
    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    assert response.status_code == 200

    response = client.get(f"{base_url}/{drones_url}/serial_number/{drone_item_2['serial_number']}")
    assert response.status_code == 404


#-------------------------------------------------------------------------------------------------#


def test_read_drone_battery_level(session: Session, client: TestClient):
    
    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    drone_id = response.json()["id"]
    drone_battery_level = response.json()["battery_capacity"]
    assert response.status_code == 200

    response = client.get(f"{base_url}/{drones_url}/{drone_id}/battery_level")
    data = response.json()
    assert response.status_code == 200
    assert data == {'drone id': drone_id, 'battery_level': drone_battery_level}


def test_read_drone_battery_level_for_drone_that_doesnt_exists(session: Session, client: TestClient):
    
    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    assert response.status_code == 200

    response = client.get(f"{base_url}/{drones_url}/{2}/battery_level")
    assert response.status_code == 404


#-------------------------------------------------------------------------------------------------#


def test_read_drone_battery_level_by_serial_number(session: Session, client: TestClient):
    
    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    drone_serial_number = response.json()["serial_number"]
    drone_battery_level = response.json()["battery_capacity"]
    assert response.status_code == 200

    response = client.get(f"{base_url}/{drones_url}/serial_number/{drone_item_1['serial_number']}/battery_level")
    data = response.json()
    assert response.status_code == 200
    assert data == {'drone serial number': drone_serial_number, 'battery_level': drone_battery_level}


def test_read_drone_battery_level_by_serial_number_for_drone_that_doesnt_exists(session: Session, client: TestClient):

    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    assert response.status_code == 200

    response = client.get(f"{base_url}/{drones_url}/serial_number/{drone_item_2['serial_number']}/battery_level")
    assert response.status_code == 404


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


def test_delete_drone_linked_to_a_medication(session: Session, client: TestClient):
    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    drone_data = response.json()
    assert response.status_code == 200
    
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    med_data = response.json()
    medication_id = med_data['id']
    assert response.status_code == 200
    
    response = client.post(f"{base_url}/{medications_url}/{med_data['code']}/link-drone/{drone_item_1['serial_number']}")
    assert response.status_code == 200
    assert {'message': f"Medication {med_data['code']} linked with drone {drone_item_1['serial_number']}"} 
    
    query_drone = select(Drone).where(Drone.serial_number == drone_data['serial_number'])
    drone = session.exec(query_drone).first()
    medications = drone.medications

    assert medications[0].id == med_data["id"]
    assert medications[0].name == med_data["name"]
    assert medications[0].code == med_data["code"]
    assert medications[0].weight == med_data["weight"]
    assert medications[0].image == med_data["image"]
    
    response = client.delete(f"{base_url}/{drones_url}/{drone_data['id']}")
    assert response.status_code == 200
    
    response = client.get(f"{base_url}/{drones_url}/{drone_data['id']}")
    assert response.status_code == 404

    medication = session.get(Medication, medication_id)
    assert medication.drone_id == None



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
    n = drone_item_1["serial_number"]
    drone_item_1["serial_number"] = "s"*101
    response = client.post(
        f"{base_url}/{drones_url}",
        json=drone_item_1,
    )
    assert response.status_code == 422
    drone_item_1["serial_number"] = n


def test_create_drone_with_weight_limit_over_limit(client: TestClient):
    n = drone_item_1["weight_limit"]
    drone_item_1["weight_limit"] = 501
    response = client.post(
        f"{base_url}/{drones_url}",
        json=drone_item_1,
    )
    assert response.status_code == 422
    drone_item_1["weight_limit"] = n


def test_create_drone_with_weight_limit_under_limit(client: TestClient):
    n = drone_item_1["weight_limit"]
    drone_item_1["weight_limit"] = -1
    response = client.post(
        f"{base_url}/{drones_url}",
        json=drone_item_1,
    )
    assert response.status_code == 422
    drone_item_1["weight_limit"] = n


def test_create_drone_with_battery_capacity_limit_over_limit(client: TestClient):
    n = drone_item_1["battery_capacity"]
    drone_item_1["battery_capacity"] = 101
    response = client.post(
        f"{base_url}/{drones_url}",
        json=drone_item_1,
    )
    assert response.status_code == 422
    drone_item_1["battery_capacity"] = n


def test_create_drone_with_battery_capacity_limit_under_limit(client: TestClient):
    n = drone_item_1["battery_capacity"]
    drone_item_1["battery_capacity"] = -1
    response = client.post(
        f"{base_url}/{drones_url}",
        json=drone_item_1,
    )
    assert response.status_code == 422
    drone_item_1["battery_capacity"] = n


#-------------------------------------------------------------------------------------------------#


