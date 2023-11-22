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


@drones_router.get("/drones/idle-drones", response_model=List[DroneRead])
async def get_idle_drones(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    drones = session.exec(select(Drone).where(Drone.state == DroneState.idle).offset(offset).limit(limit)).all()
    return drones


#-------------------------------------------------------------------------------------------------#


@drones_router.get("/drones/serial_number/{serial_number}", response_model=DroneRead)
def read_drone_by_serial_number(*, session: Session = Depends(get_session), serial_number: str):
    query = select(Drone).where(Drone.serial_number == serial_number)
    drone = session.exec(query).first()
    if not drone:
        raise HTTPException(status_code=404, detail="Drone not found")
    return drone


#-------------------------------------------------------------------------------------------------#


@drones_router.get("/drones/{drone_id}/battery_level")
def read_drone_battery_level(*, session: Session = Depends(get_session), drone_id: int):
    drone = session.get(Drone, drone_id)
    if not drone:
        raise HTTPException(status_code=404, detail="Drone not found")
    return {"drone id": drone.id, "battery_level": drone.battery_capacity}


@drones_router.get("/drones/serial_number/{serial_number}/battery_level")
def read_drone_battery_level_by_serial_number(*, session: Session = Depends(get_session), serial_number: str):
    query = select(Drone).where(Drone.serial_number == serial_number)
    drone = session.exec(query).first()
    if not drone:
        raise HTTPException(status_code=404, detail="Drone not found")
    return {"drone serial number": drone.serial_number, "battery_level": drone.battery_capacity}


#-------------------------------------------------------------------------------------------------#


@drones_router.get("/drones/{serial_number}/medications", response_model=List[MedicationRead])
def get_drone_medications(serial_number: str, session: Session = Depends(get_session)):
    query_drone = select(Drone).where(Drone.serial_number == serial_number)
    drone = session.exec(query_drone).first()
    if not drone:
        raise HTTPException(status_code=404, detail="Drone not found")
    medications = drone.medications
    return medications


@drones_router.get("/drones/{serial_number}/available_cargo_weight")
def get_available_cargo_weight(serial_number: str, session: Session = Depends(get_session)):
    # Search for the drone by its serial number
    query_drone = select(Drone).where(Drone.serial_number == serial_number)
    drone = session.exec(query_drone).first()
    if not drone:
        raise HTTPException(status_code=404, detail="Drone not found")

    available_cargo_weight = drone.weight_limit - sum([med.weight for med in drone.medications])

    return {f"available_cargo_weight for drone '{serial_number}'": available_cargo_weight}


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

    if db_medication.drone_id:
        drone = session.get(Drone, db_medication.drone_id)
        if not drone:
            raise HTTPException(status_code=404, detail="Drone not found")
    
        available_cargo_weight = drone.weight_limit - sum([med.weight for med in drone.medications])

        if available_cargo_weight < db_medication.weight:
            raise HTTPException(status_code=422, detail=f"The weight of the Medication exceeds the available cargo weight of the Drone.")

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
            

        if "drone_id" in medication_data.keys():

            drone = session.get(Drone, medication_data['drone_id'])
            if not drone:
                raise HTTPException(status_code=404, detail="Drone not found")
            
            available_cargo_weight = drone.weight_limit - sum([med.weight for med in drone.medications])
            
            if "weight" in medication_data.keys():                   

                if available_cargo_weight < medication_data['weight']:
                    raise HTTPException(status_code=422, detail=f"The weight of the Medication exceeds the available cargo weight of the Drone.")

            else:

                if available_cargo_weight < db_medication.weight:
                    raise HTTPException(status_code=422, detail=f"The weight of the Medication exceeds the available cargo weight of the Drone.")


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


@drones_router.get("/medications/code/{code}", response_model=MedicationRead)
def read_medication_by_code(*, session: Session = Depends(get_session), code: str):
    query = select(Medication).where(Medication.code == code)
    medication = session.exec(query).first()
    if not medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    return medication


#-------------------------------------------------------------------------------------------------#


@drones_router.post("/medications/{med_code}/link-drone/{serial_number}")
def link_medication_with_drone(med_code: str, serial_number: str, session: Session = Depends(get_session)):
    
    query_medication = select(Medication).where(Medication.code == med_code)
    medication = session.exec(query_medication).first()
    if not medication:
        raise HTTPException(status_code=404, detail="Medication not found")

    query_drone = select(Drone).where(Drone.serial_number == serial_number)
    drone = session.exec(query_drone).first()
    if not drone:
        raise HTTPException(status_code=404, detail="Drone not found")
    
    available_cargo_weight = drone.weight_limit - sum([med.weight for med in drone.medications])
    if available_cargo_weight < medication.weight:
        raise HTTPException(status_code=422, detail=f"The weight of the Medication exceeds the available cargo weight of the Drone.")

    medication.drone = drone
    session.add(medication)
    session.commit()

    return {"message": f"Medication {med_code} linked with drone {serial_number}"}



#-------------------------------------------------------------------------------------------------#


