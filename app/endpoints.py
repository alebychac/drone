# coding=utf-8


#-------------------------------------------------------------------------------------------------#


from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from typing import List
from re import match

from .db_engine import(
    Session, 
    get_session
)
from .models import (
    Drone,
    DroneRead,
    DroneCreate,
    DroneUpdate, 
    Medication,
    MedicationRead,
    MedicationCreate,
    MedicationUpdate, 
    DroneModel, 
    DroneState
)


#-------------------------------------------------------------------------------------------------#


drones_router = APIRouter()


@drones_router.get("/drones/models")
async def get_drone_models():
    return {"drone_models": [model.value for model in DroneModel]}


@drones_router.get("/drones/states")
async def get_drone_states():
    return {"drone_states": [model.value for model in DroneState]}


#-------------------------------------------------------------------------------------------------#


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


@drones_router.get("/drones/", response_model=List[DroneRead])
def read_drones(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    drones = session.exec(select(Drone).offset(offset).limit(limit)).all()
    return drones
#-------------------------------------------------------------------------------------------------#


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
def read_drone(*, session: Session = Depends(get_session), drone_id: int):
    drone = session.get(Drone, drone_id)
    if not drone:
        raise HTTPException(status_code=404, detail="Drone not found")
    return drone


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


@drones_router.delete("/drones/{drone_id}")
def delete_drone(*, session: Session = Depends(get_session), drone_id: int):
    drone = session.get(Drone, drone_id)
    if not drone:
        raise HTTPException(status_code=404, detail="Drone not found")
    session.delete(drone)
    session.commit()
    return {"ok": True}


#-------------------------------------------------------------------------------------------------#


medications_router = APIRouter()


@medications_router.post("/medications/", response_model=MedicationRead)
def create_medication(*, session: Session = Depends(get_session), medication: MedicationCreate):

    db_medication = Medication.from_orm(medication)
    try:
        session.add(db_medication)
        session.commit()
        session.refresh(db_medication)        
        return db_medication
    except IntegrityError:        
        raise HTTPException(status_code=422, detail=f"Already exists a medication with '{medication.code}' code")


@medications_router.get("/medications/", response_model=List[MedicationRead])
def read_medications(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    medications = session.exec(select(Medication).offset(offset).limit(limit)).all()
    return medications


@medications_router.get("/medications/{medication_id}", response_model=MedicationRead)
def read_medication(*, session: Session = Depends(get_session), medication_id: int):
    medication = session.get(Medication, medication_id)
    if not medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    return medication


@medications_router.patch("/medications/{medication_id}", response_model=MedicationRead)
def update_medication(
    *, session: Session = Depends(get_session), medication_id: int, medication: MedicationUpdate
):
    try:
        db_medication = session.get(Medication, medication_id)
        if not db_medication:
            raise HTTPException(status_code=404, detail="Medication not found")
        medication_data = medication.dict(exclude_unset=True)

        

        if "weight" in medication_data.keys():
            if medication_data["weight"] < 1:
                raise HTTPException(status_code=422, detail="medication weight must be greater than 0")


        if "name" in medication_data.keys():
            if not match(r"^[a-zA-Z0-9-_]+$", medication_data["name"] ):
                raise HTTPException(status_code=422, detail="Invalid name format. Only letters, score, underscore, and numbers are allowed.")
        
        if "code" in medication_data.keys():
            if not match(r"^[A-Z0-9_]+$", medication_data["code"] ):
                raise HTTPException(status_code=422, detail="Invalid code format. Only uppercase letters, underscore, and numbers are allowed.")


        for key, value in medication_data.items():
            setattr(db_medication, key, value)
        session.add(db_medication)
        session.commit()
        session.refresh(db_medication)
        return db_medication

    except IntegrityError:        
        raise HTTPException(status_code=422, detail=f"Already exists a medication with '{medication.code}' code")


@medications_router.delete("/medications/{medication_id}")
def delete_medication(*, session: Session = Depends(get_session), medication_id: int):
    medication = session.get(Medication, medication_id)
    if not medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    session.delete(medication)
    session.commit()
    return {"ok": True}


#-------------------------------------------------------------------------------------------------#

