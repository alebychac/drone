# coding=utf-8


#-------------------------------------------------------------------------------------------------#


from fastapi import FastAPI, APIRouter

from .db_engine import create_db_and_tables
from .models.drone import Drone
from .models.medication import Medication 
from .models.drone_battery_log import DroneBatteryLog
from .endpoints.drone import drones_router
from .endpoints.medication import medications_router
from .backgrounds_tasks import scheduler


#-------------------------------------------------------------------------------------------------#


app = FastAPI()

api_router = APIRouter()
api_router.include_router(drones_router)
api_router.include_router(medications_router)
app.include_router(api_router, prefix=f"/api/v1")


@app.get("/")
def root():
    return {
        "message": "Root",
    }


#-------------------------------------------------------------------------------------------------#


create_db_and_tables()

scheduler.start()


#-------------------------------------------------------------------------------------------------#

