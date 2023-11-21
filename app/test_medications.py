# coding=utf-8


#-------------------------------------------------------------------------------------------------#


from app.models import DroneModel, DroneState
from app.config_for_tests import *


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


medication_item_incomplete = {
    "name": "dipirona",
    "weight": 75,
    "image": "imag dip 01",
    # "drone_id": 1,
}


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


def test_create_medication_invalid(client: TestClient):
    medication_item_1["name"] = "med "
    response = client.post(
        f"{base_url}/{medications_url}",
        json=medication_item_1,
    )
    assert response.status_code == 422


def test_create_medication_invalid2(client: TestClient):
    medication_item_1["name"] = "med*"
    response = client.post(
        f"{base_url}/{medications_url}",
        json=medication_item_1,
    )
    assert response.status_code == 422


def test_create_medication_invalid3(client: TestClient):
    medication_item_1["code"] = "med"
    response = client.post(
        f"{base_url}/{medications_url}",
        json=medication_item_1,
    )
    assert response.status_code == 422


def test_create_medication_invalid4(client: TestClient):
    medication_item_1["code"] = "MED_"
    response = client.post(
        f"{base_url}/{medications_url}",
        json=medication_item_1,
    )
    assert response.status_code == 422


def test_create_medication_invalid4(client: TestClient):
    medication_item_1["code"] = "MED_1*"
    response = client.post(
        f"{base_url}/{medications_url}",
        json=medication_item_1,
    )
    assert response.status_code == 422


def test_create_medication_with_weight_under_limit(client: TestClient):
    medication_item_1["weight"] = -1
    response = client.post(
        f"{base_url}/{medications_url}",
        json=medication_item_1,
    )
    assert response.status_code == 422


#-------------------------------------------------------------------------------------------------#

