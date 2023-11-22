# coding=utf-8


#-------------------------------------------------------------------------------------------------#


from app.tests.config_for_tests import *


#-------------------------------------------------------------------------------------------------#


def test_read_medication_by_code(session: Session, client: TestClient):
    
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    medication_code = response.json()["code"]
    assert response.status_code == 200

    response = client.get(f"{base_url}/{medications_url}/code/{medication_code}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == medication_item_1["name"]
    assert data["code"] == medication_item_1["code"]
    assert data["weight"] == medication_item_1["weight"]
    assert data["image"] == medication_item_1["image"]


def test_read_medication_by_code_that_doesnt_exists(session: Session, client: TestClient):
    
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    assert response.status_code == 200

    response = client.get(f"{base_url}/{medications_url}/code/{medication_item_2['code']}")
    assert response.status_code == 404


#-------------------------------------------------------------------------------------------------#


def test_read_medication(session: Session, client: TestClient):
    
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    assert response.status_code == 200
    data = response.json()


    response = client.get(f"{base_url}/{medications_url}/{data['id']}")

    assert response.status_code == 200
    assert data["name"] == medication_item_1["name"]
    assert data["code"] == medication_item_1["code"]
    assert data["weight"] == medication_item_1["weight"]
    assert data["image"] == medication_item_1["image"]
    # assert data["drone_id"] == medication_item_1["drone_id"]


def test_read_medication_that_doesnt_exists(session: Session, client: TestClient):
    
    response = client.get(f"{base_url}/{medications_url}/{1}")

    assert response.status_code == 404


def test_read_medications(session: Session, client: TestClient):
    
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    assert response.status_code == 200

    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_2)
    assert response.status_code == 200

    response = client.get(f"{base_url}/{medications_url}/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 2


    assert data[0]["name"] == medication_item_1["name"]
    assert data[0]["code"] == medication_item_1["code"]
    assert data[0]["weight"] == medication_item_1["weight"]
    assert data[0]["image"] == medication_item_1["image"]


    assert data[1]["name"] == medication_item_2["name"]
    assert data[1]["code"] == medication_item_2["code"]
    assert data[1]["weight"] == medication_item_2["weight"]
    assert data[1]["image"] == medication_item_2["image"]


#-------------------------------------------------------------------------------------------------#


def test_update_medication(session: Session, client: TestClient):

    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    data = response.json()
    assert response.status_code == 200
    medication_id = data['id']
    response = client.patch(f"{base_url}/{medications_url}/{medication_id}", json={"weight": 50})

    data = response.json()

    assert response.status_code == 200
    assert data["name"] == medication_item_1["name"]
    assert data["code"] == medication_item_1["code"]
    assert data["weight"] == 50
    assert data["image"] == medication_item_1["image"]


def test_update_medication_that_doesnt_exists(session: Session, client: TestClient):
    response = client.patch(f"{base_url}/{medications_url}/{1}", json={"weight": 50})
    assert response.status_code == 404


def test_update_medication_repeated(session: Session, client: TestClient):

    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    assert response.status_code == 200

    data_1 = response.json()
    medication_id_1 = data_1['id']

    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_2)
    assert response.status_code == 200

    response = client.patch(f"{base_url}/{medications_url}/{medication_id_1}", json={"code": medication_item_2["code"]})

    assert response.status_code == 422


def test_update_medication_with_weight_under_limit(client: TestClient):    
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    assert response.status_code == 200

    data = response.json()
    medication_id = data['id']

    response = client.patch(f"{base_url}/{medications_url}/{medication_id}", json={"weight": -1})
    assert response.status_code == 422


def test_update_medication_invalid_name_1(client: TestClient): 
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    assert response.status_code == 200

    data = response.json()
    medication_id = data['id']

    response = client.patch(f"{base_url}/{medications_url}/{medication_id}", json={"name": "med "})
    assert response.status_code == 422


def test_update_medication_invalid_name_2(client: TestClient):  
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)  
    assert response.status_code == 200

    data = response.json()
    medication_id = data['id']

    response = client.patch(f"{base_url}/{medications_url}/{medication_id}", json={"name": "med*"})
    assert response.status_code == 422


def test_update_medication_invalid_code_1(client: TestClient):
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    assert response.status_code == 200

    data = response.json()
    medication_id = data['id']

    response = client.patch(f"{base_url}/{medications_url}/{medication_id}", json={"code": "med"})
    assert response.status_code == 422


def test_update_medication_invalid_code_2(client: TestClient):
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    assert response.status_code == 200

    data = response.json()
    medication_id = data['id']

    response = client.patch(f"{base_url}/{medications_url}/{medication_id}", json={"code": "MED-"})
    assert response.status_code == 422


def test_update_medication_invalid_code_3(client: TestClient):
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    assert response.status_code == 200

    data = response.json()
    medication_id = data['id']

    response = client.patch(f"{base_url}/{medications_url}/{medication_id}", json={"code": "MED_1*"})
    assert response.status_code == 422


def test_update_medication_invalid_code_4(client: TestClient):
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    assert response.status_code == 200

    data = response.json()
    medication_id = data['id']

    response = client.patch(f"{base_url}/{medications_url}/{medication_id}", json={"code": "MED _1*"})
    assert response.status_code == 422


def test_update_medication_with_drone(session: Session, client: TestClient):    
    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    drone_data = response.json()
    assert response.status_code == 200

    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    assert response.status_code == 200

    data = response.json()
    medication_id = data['id']

    response = client.patch(f"{base_url}/{medications_url}/{medication_id}", json={"drone_id": drone_data['id']})
    assert response.status_code == 200
    med_data = response.json()
          
    query_drone = select(Drone).where(Drone.serial_number == drone_data['serial_number'])
    drone = session.exec(query_drone).first()
    medications = drone.medications

    assert medications[0].id == med_data["id"]
    assert medications[0].name == med_data["name"]
    assert medications[0].code == med_data["code"]
    assert medications[0].weight == med_data["weight"]
    assert medications[0].image == med_data["image"]
    medication_item_1["drone_id"] = None


def test_update_medication_with_drone_exceeds_cargo_weight_1(session: Session, client: TestClient):

    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    drone_data = response.json()
    assert response.status_code == 200

    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    assert response.status_code == 200

    data = response.json()
    medication_id = data['id']

    response = client.patch(f"{base_url}/{medications_url}/{medication_id}", json={"drone_id": drone_data['id'], "weight": 126})
    med_data = response.json()
    assert response.status_code == 422
          
    query_drone = select(Drone).where(Drone.serial_number == drone_data['serial_number'])
    drone = session.exec(query_drone).first()
    medications = drone.medications

    assert len(medications) == 0
    assert response.status_code == 422
    assert med_data == {'detail': 'The weight of the Medication exceeds the available cargo weight of the Drone.'}


def test_update_medication_with_drone_exceeds_cargo_weight_2(session: Session, client: TestClient):

    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    drone_data = response.json()
    assert response.status_code == 200

    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    assert response.status_code == 200

    data = response.json()
    medication_id = data['id']

    response = client.patch(f"{base_url}/{medications_url}/{medication_id}", json={"weight": 126})
    assert response.status_code == 200
          
    response = client.patch(f"{base_url}/{medications_url}/{medication_id}", json={"drone_id": drone_data['id']})
    med_data = response.json()
    assert response.status_code == 422

    query_drone = select(Drone).where(Drone.serial_number == drone_data['serial_number'])
    drone = session.exec(query_drone).first()
    medications = drone.medications

    assert len(medications) == 0
    assert response.status_code == 422
    assert med_data == {'detail': 'The weight of the Medication exceeds the available cargo weight of the Drone.'}
  

def test_update_medication_with_drone_medication_that_doesnt_exists(session: Session, client: TestClient):
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    assert response.status_code == 200

    data = response.json()
    medication_id = data['id']

    response = client.patch(f"{base_url}/{medications_url}/{medication_id}", json={"drone_id": "1"})
    assert response.status_code == 404


#-------------------------------------------------------------------------------------------------#


def test_delete_medication(session: Session, client: TestClient):

    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    assert response.status_code == 200

    data = response.json()
    medication_id = data['id']
    
    response = client.delete(f"{base_url}/{medications_url}/{medication_id}")
    assert response.status_code == 200

    response = client.get(f"{base_url}/{medications_url}/{data['id']}")
    assert response.status_code == 404


def test_delete_medication_that_doesnt_exists(session: Session, client: TestClient):
    response = client.delete(f"{base_url}/{medications_url}/{1}")
    assert response.status_code == 404


def test_delete_medication_linked_to_a_drone(session: Session, client: TestClient):
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
    
    response = client.delete(f"{base_url}/{medications_url}/{medication_id}")
    assert response.status_code == 200

    query_drone = select(Drone).where(Drone.serial_number == drone_data['serial_number'])
    drone = session.exec(query_drone).first()
    medications = drone.medications

    assert len(medications) == 0

    response = client.get(f"{base_url}/{medications_url}/{medication_id}")
    assert response.status_code == 404


#-------------------------------------------------------------------------------------------------#


def test_create_medication(client: TestClient):
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    data = response.json()
    
    assert response.status_code == 200
    assert data["name"] == medication_item_1["name"]
    assert data["code"] == medication_item_1["code"]
    assert data["weight"] == medication_item_1["weight"]
    assert data["image"] == medication_item_1["image"]


def test_create_medication_repated(client: TestClient):
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    data = response.json()
    
    assert response.status_code == 200
    assert data["name"] == medication_item_1["name"]
    assert data["code"] == medication_item_1["code"]
    assert data["weight"] == medication_item_1["weight"]
    assert data["image"] == medication_item_1["image"]

    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    assert response.status_code == 422


def test_create_medication_incomplete(client: TestClient):
    response = client.post(f"{base_url}/{medications_url}", json=medication_item_incomplete)
    assert response.status_code == 422


def test_create_medication_invalid_name_1(client: TestClient): 
    n = medication_item_1["name"] 
    medication_item_1["name"] = "med "
    response = client.post(
        f"{base_url}/{medications_url}",
        json=medication_item_1,
    )
    assert response.status_code == 422
    medication_item_1["name"] = n


def test_create_medication_invalid_name_2(client: TestClient):    
    n = medication_item_1["name"] 
    medication_item_1["name"] = "med*"
    response = client.post(
        f"{base_url}/{medications_url}",
        json=medication_item_1,
    )
    assert response.status_code == 422
    medication_item_1["name"] = n


def test_create_medication_invalid_code_1(client: TestClient):
    n = medication_item_1["code"]
    medication_item_1["code"] = "med"
    response = client.post(
        f"{base_url}/{medications_url}",
        json=medication_item_1,
    )
    assert response.status_code == 422
    medication_item_1["code"] = n


def test_create_medication_invalid_code_2(client: TestClient):
    n = medication_item_1["code"]
    medication_item_1["code"] = "MED-"
    response = client.post(
        f"{base_url}/{medications_url}",
        json=medication_item_1,
    )
    assert response.status_code == 422
    medication_item_1["code"] = n


def test_create_medication_invalid_code_3(client: TestClient):
    n = medication_item_1["code"]
    medication_item_1["code"] = "MED_1*"
    response = client.post(
        f"{base_url}/{medications_url}",
        json=medication_item_1,
    )
    assert response.status_code == 422
    medication_item_1["code"] = n


def test_create_medication_invalid_code_4(client: TestClient):
    n = medication_item_1["code"]
    medication_item_1["code"] = "MED _1"
    response = client.post(
        f"{base_url}/{medications_url}",
        json=medication_item_1,
    )
    assert response.status_code == 422
    medication_item_1["code"] = n


def test_create_medication_with_weight_under_limit(client: TestClient):
    n = medication_item_1["weight"]
    medication_item_1["weight"] = -1
    response = client.post(
        f"{base_url}/{medications_url}",
        json=medication_item_1,
    )
    assert response.status_code == 422
    medication_item_1["weight"] = n


def test_create_medication_with_drone(session: Session, client: TestClient):
    
    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    drone_data = response.json()
    assert response.status_code == 200
    
    medication_item_1["drone_id"] = 1
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    med_data = response.json()
    assert response.status_code == 200
        
    query_drone = select(Drone).where(Drone.serial_number == drone_data['serial_number'])
    drone = session.exec(query_drone).first()
    medications = drone.medications

    assert medications[0].id == med_data["id"]
    assert medications[0].name == med_data["name"]
    assert medications[0].code == med_data["code"]
    assert medications[0].weight == med_data["weight"]
    assert medications[0].image == med_data["image"]
    medication_item_1["drone_id"] = None


def test_create_medication_with_drone_exceeds_cargo_weight(session: Session, client: TestClient):
    
    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    drone_data = response.json()
    assert response.status_code == 200
    
    n = medication_item_1["weight"]
    medication_item_1["weight"] = 126    
    medication_item_1["drone_id"] = drone_data["id"]
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    med_data = response.json()
    medication_item_1["weight"] = n
    medication_item_1["drone_id"] = None

    query_drone = select(Drone).where(Drone.serial_number == drone_data['serial_number'])
    drone = session.exec(query_drone).first()
    medications = drone.medications

    assert len(medications) == 0
    assert response.status_code == 422
    assert med_data == {'detail': 'The weight of the Medication exceeds the available cargo weight of the Drone.'}


def test_create_medication_with_drone_medication_that_doesnt_exists(session: Session, client: TestClient):
    
    medication_item_1["drone_id"] = 1
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    medication_item_1["drone_id"] = None
    assert response.status_code == 404

    
#-------------------------------------------------------------------------------------------------#


def test_link_medication_with_drone_success(session: Session, client: TestClient):   

    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    drone_data = response.json()
    assert response.status_code == 200
    
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    med_data = response.json()
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


def test_link_medication_with_drone_medication_that_doesnt_exists(session: Session, client: TestClient):   

    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    drone_data = response.json()
    assert response.status_code == 200
        
    response = client.post(f"{base_url}/{medications_url}/MED-05/link-drone/{drone_item_1['serial_number']}")

    assert response.status_code == 404


def test_link_medication_with_drone_drone_that_doesnt_exists(session: Session, client: TestClient):   

    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    assert response.status_code == 200
    med_data = response.json()
        
    response = client.post(f"{base_url}/{medications_url}/{med_data['code']}/link-drone/DR-01")
   
    assert response.status_code == 404


def test_link_medication_with_drone_success_with_2_medications(session: Session, client: TestClient):   

    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    assert response.status_code == 200
    drone_data = response.json()
    
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    med_data_1 = response.json()
    assert response.status_code == 200

    response = client.post(f"{base_url}/{medications_url}/{med_data_1['code']}/link-drone/{drone_item_1['serial_number']}")
    assert response.status_code == 200
    assert {'message': f"Medication {med_data_1['code']} linked with drone {drone_item_1['serial_number']}"} 
      
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_2)
    assert response.status_code == 200
    med_data_2 = response.json()

    response = client.post(f"{base_url}/{medications_url}/{med_data_2['code']}/link-drone/{drone_item_1['serial_number']}")
    assert response.status_code == 200
    assert {'message': f"Medication {med_data_2['code']} linked with drone {drone_item_1['serial_number']}"} 
       
    query_drone = select(Drone).where(Drone.serial_number == drone_data['serial_number'])
    drone = session.exec(query_drone).first()
    medications = drone.medications

    assert medications[0].id == med_data_1["id"]
    assert medications[0].name == med_data_1["name"]
    assert medications[0].code == med_data_1["code"]
    assert medications[0].weight == med_data_1["weight"]
    assert medications[0].image == med_data_1["image"]

    assert medications[1].id == med_data_2["id"]
    assert medications[1].name == med_data_2["name"]
    assert medications[1].code == med_data_2["code"]
    assert medications[1].weight == med_data_2["weight"]
    assert medications[1].image == med_data_2["image"]


def test_link_medication_with_drone_exceeds_cargo_weight(session: Session, client: TestClient):   

    response = client.post(f"{base_url}/{drones_url}/", json=drone_item_1)
    assert response.status_code == 200
    drone_data = response.json()
    
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_1)
    med_data_1 = response.json()
    assert response.status_code == 200

    response = client.post(f"{base_url}/{medications_url}/{med_data_1['code']}/link-drone/{drone_item_1['serial_number']}")
    assert response.status_code == 200
    assert {'message': f"Medication {med_data_1['code']} linked with drone {drone_item_1['serial_number']}"} 
      
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_2)
    assert response.status_code == 200
    med_data_2 = response.json()

    response = client.post(f"{base_url}/{medications_url}/{med_data_2['code']}/link-drone/{drone_item_1['serial_number']}")
    assert response.status_code == 200
    assert {'message': f"Medication {med_data_2['code']} linked with drone {drone_item_1['serial_number']}"} 
             
    response = client.post(f"{base_url}/{medications_url}/", json=medication_item_3)
    assert response.status_code == 200
    med_data_3 = response.json()

    response = client.post(f"{base_url}/{medications_url}/{med_data_3['code']}/link-drone/{drone_item_1['serial_number']}")
    assert response.json() == {'detail': 'The weight of the Medication exceeds the available cargo weight of the Drone.'} 
    assert response.status_code == 422

    query_drone = select(Drone).where(Drone.serial_number == drone_data['serial_number'])
    drone = session.exec(query_drone).first()
    medications = drone.medications

    assert medications[0].id == med_data_1["id"]
    assert medications[0].name == med_data_1["name"]
    assert medications[0].code == med_data_1["code"]
    assert medications[0].weight == med_data_1["weight"]
    assert medications[0].image == med_data_1["image"]

    assert medications[1].id == med_data_2["id"]
    assert medications[1].name == med_data_2["name"]
    assert medications[1].code == med_data_2["code"]
    assert medications[1].weight == med_data_2["weight"]
    assert medications[1].image == med_data_2["image"]
