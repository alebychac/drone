# coding=utf-8


#-------------------------------------------------------------------------------------------------#


import sys
from pathlib import Path
path = Path(__file__).absolute().parent
sys.path.append(str(path))


#-------------------------------------------------------------------------------------------------#


import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool

from app.main import api_router
from app.db_engine import get_session
from app.models import DroneModel, DroneState, Drone


#-------------------------------------------------------------------------------------------------#


base_url = "/api/v1"
drones_url = "drones"
medications_url = "medications"


app = FastAPI()
app.include_router(api_router, prefix=f"{base_url}")


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


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
    "weight": 75,
    "code": "IBU_01",
    "image": "imag ibu 01",
    # "drone_id": 1,
}


medication_item_incomplete = {
    "name": "dipirona",
    "weight": 75,
    "image": "imag dip 01",
    # "drone_id": 1,
}


#-------------------------------------------------------------------------------------------------#

