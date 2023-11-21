# coding=utf-8


#-------------------------------------------------------------------------------------------------#


import sys
from pathlib import Path
path = Path(__file__).absolute()
print(path)
sys.path.append(str(path))


#-------------------------------------------------------------------------------------------------#


import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import api_router
from app.db_engine import get_session


#-------------------------------------------------------------------------------------------------#


base_url = "/api/v1"
drones_url = "drones"
medication_url = "medication"


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

