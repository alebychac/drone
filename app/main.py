# coding=utf-8


#-------------------------------------------------------------------------------------------------#


from fastapi import FastAPI, APIRouter

from .db_engine import create_db_and_tables
from .models import Drone, Medication
from .endpoints import drones_router, medications_router


#-------------------------------------------------------------------------------------------------#


app = FastAPI()

api_router = APIRouter()
api_router.include_router(drones_router)
api_router.include_router(medications_router)
app.include_router(api_router, prefix=f"/api/v1")


@app.get("/")
def root():
    return {
        "message": "Home",
    }


#-------------------------------------------------------------------------------------------------#


# create_db_and_tables()


#-------------------------------------------------------------------------------------------------#

