# coding=utf-8


#-------------------------------------------------------------------------------------------------#


from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from typing import List

from app.db_engine import(
    Session, 
    get_session
)

from app.models.drone import Drone, DroneModel, DroneState, DroneCreate, DroneRead, DroneUpdate
from app.models.medication import Medication, MedicationRead
from app.models.drone_battery_log import DroneBatteryLog


#-------------------------------------------------------------------------------------------------#


drones_router = APIRouter()


#-------------------------------------------------------------------------------------------------#



@drones_router.get("/drones/models")
async def get_drone_models():
    return {"drone_models": [model.value for model in DroneModel]}


@drones_router.get("/drones/states")
async def get_drone_states():
    return {"drone_states": [model.value for model in DroneState]}


#-------------------------------------------------------------------------------------------------#


#                       _       
#                      | |      
#    ___ _ __ ___  __ _| |_ ___ 
#   / __| '__/ _ \/ _` | __/ _ \
#  | (__| | |  __/ (_| | ||  __/
#   \___|_|  \___|\__,_|\__\___|


@drones_router.post("/drones/", response_model=DroneRead)
def create_drone(*, session: Session = Depends(get_session), drone: DroneCreate):
    db_drone = Drone.from_orm(drone)
    try:
        session.add(db_drone)
        session.commit()
        session.refresh(db_drone)        
        return db_drone
    except IntegrityError:        
        raise HTTPException(status_code=422, detail=f"Already exists a drone with '{drone.serial_number}' serial number")


#-------------------------------------------------------------------------------------------------#


#              _   
#             | |  
#    __ _  ___| |_ 
#   / _` |/ _ \ __|
#  | (_| |  __/ |_ 
#   \__, |\___|\__|
#    __/ |         
#   |___/      


@drones_router.get("/drones/", response_model=List[DroneRead])
def get_drones(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    drones = session.exec(select(Drone).offset(offset).limit(limit)).all()
    return drones


@drones_router.get("/drones/idle-drones", response_model=List[DroneRead])
async def get_idle_drones(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    drones = session.exec(select(Drone).where(Drone.state == DroneState.idle).offset(offset).limit(limit)).all()
    return drones


@drones_router.get("/drones/{drone_id}", response_model=DroneRead)
def get_drone(*, session: Session = Depends(get_session), drone_id: int):
    drone = session.get(Drone, drone_id)
    if not drone:
        raise HTTPException(status_code=404, detail="Drone not found")
    return drone


@drones_router.get("/drones/serial_number/{serial_number}", response_model=DroneRead)
def get_drone_by_serial_number(*, session: Session = Depends(get_session), serial_number: str):
    query = select(Drone).where(Drone.serial_number == serial_number)
    drone = session.exec(query).first()
    if not drone:
        raise HTTPException(status_code=404, detail="Drone not found")
    return drone


@drones_router.get("/drones/{drone_id}/battery_level")
def get_drone_battery_level(*, session: Session = Depends(get_session), drone_id: int):
    drone = session.get(Drone, drone_id)
    if not drone:
        raise HTTPException(status_code=404, detail="Drone not found")
    return {"drone id": drone.id, "battery_level": drone.battery_capacity}


@drones_router.get("/drones/serial_number/{serial_number}/battery_level")
def get_drone_battery_level_by_serial_number(*, session: Session = Depends(get_session), serial_number: str):
    query = select(Drone).where(Drone.serial_number == serial_number)
    drone = session.exec(query).first()
    if not drone:
        raise HTTPException(status_code=404, detail="Drone not found")
    return {"drone serial number": drone.serial_number, "battery_level": drone.battery_capacity}


@drones_router.get("/drones/{serial_number}/medications", response_model=List[MedicationRead])
def get_drone_medications_by_serial_number(serial_number: str, session: Session = Depends(get_session)):
    query_drone = select(Drone).where(Drone.serial_number == serial_number)
    drone = session.exec(query_drone).first()
    if not drone:
        raise HTTPException(status_code=404, detail="Drone not found")
    medications = drone.medications
    return medications


@drones_router.get("/drones/{serial_number}/available_cargo_weight")
def get_available_cargo_weight_by_serial_number(serial_number: str, session: Session = Depends(get_session)):
    # Search for the drone by its serial number
    query_drone = select(Drone).where(Drone.serial_number == serial_number)
    drone = session.exec(query_drone).first()
    if not drone:
        raise HTTPException(status_code=404, detail="Drone not found")

    available_cargo_weight = drone.weight_limit - sum([med.weight for med in drone.medications])

    return {f"available_cargo_weight for drone '{serial_number}'": available_cargo_weight}


@drones_router.get("/latest_drone_battery_logs")
async def get_latest_drone_battery_logs(session: Session = Depends(get_session)):          
    number_of_drones = len(session.query(Drone).all())
    query = session.query(DroneBatteryLog).order_by(DroneBatteryLog.timestamp.desc()).limit(number_of_drones)
    result = session.exec(query).fetchall()
    return result


#-------------------------------------------------------------------------------------------------#


#                   _       _       
#                  | |     | |      
#   _   _ _ __   __| | __ _| |_ ___ 
#  | | | | '_ \ / _` |/ _` | __/ _ \
#  | |_| | |_) | (_| | (_| | ||  __/
#   \__,_| .__/ \__,_|\__,_|\__\___|
#        | |                        
#        |_|         


@drones_router.patch("/drones/{drone_id}", response_model=DroneRead)
def update_drone(
    *, session: Session = Depends(get_session), drone_id: int, drone: DroneUpdate
):
    try:
        db_drone = session.get(Drone, drone_id)
        if not db_drone:
            raise HTTPException(status_code=404, detail="Drone not found")
        drone_data = drone.dict(exclude_unset=True)

        if "weight_limit" in drone_data.keys():
            if drone_data["weight_limit"] > 500 or drone_data["weight_limit"] < 0:
                raise HTTPException(status_code=422, detail="Drone weight_limit must be greater than 0 and under 500")
    
        if "battery_capacity" in drone_data.keys():
            if drone_data["battery_capacity"] > 100 or drone_data["battery_capacity"] < 0:
                 raise HTTPException(status_code=422, detail="Drone battery_capacity must be greater than 0 and under 100")
    

        for key, value in drone_data.items():
            setattr(db_drone, key, value)
        session.add(db_drone)
        session.commit()
        session.refresh(db_drone)
        return db_drone

    except IntegrityError:        
        raise HTTPException(status_code=422, detail=f"Already exists a drone with '{drone.serial_number}' serial number")


#-------------------------------------------------------------------------------------------------#


#       _      _      _       
#      | |    | |    | |      
#    __| | ___| | ___| |_ ___ 
#   / _` |/ _ \ |/ _ \ __/ _ \
#  | (_| |  __/ |  __/ ||  __/
#   \__,_|\___|_|\___|\__\___|
                                      

@drones_router.delete("/drones/{drone_id}")
def delete_drone(*, session: Session = Depends(get_session), drone_id: int):
    drone = session.get(Drone, drone_id)
    if not drone:
        raise HTTPException(status_code=404, detail="Drone not found")
    session.delete(drone)
    session.commit()
    return {"ok": True}


#-------------------------------------------------------------------------------------------------#


#         _   _                   
#        | | | |                  
#    ___ | |_| |__   ___ _ __ ___ 
#   / _ \| __| '_ \ / _ \ '__/ __|
#  | (_) | |_| | | |  __/ |  \__ \
#   \___/ \__|_| |_|\___|_|  |___/


@drones_router.post("/medications/{medication_code}/link-drone/{drone_serial_number}")
def link_medication_with_drone(medication_code: str, drone_serial_number: str, session: Session = Depends(get_session)):
    
    query_medication = select(Medication).where(Medication.code == medication_code)
    medication = session.exec(query_medication).first()
    if not medication:
        raise HTTPException(status_code=404, detail="Medication not found")

    query_drone = select(Drone).where(Drone.serial_number == drone_serial_number)
    drone = session.exec(query_drone).first()
    if not drone:
        raise HTTPException(status_code=404, detail="Drone not found")
    
    available_cargo_weight = drone.weight_limit - sum([med.weight for med in drone.medications])
    if available_cargo_weight < medication.weight:
        raise HTTPException(status_code=422, detail=f"The weight of the Medication exceeds the available cargo weight of the Drone.")

    medication.drone = drone
    session.add(medication)
    session.commit()

    return {"message": f"Medication {medication_code} linked with drone {drone_serial_number}"}


#-------------------------------------------------------------------------------------------------#

