# coding=utf-8


#-------------------------------------------------------------------------------------------------#


from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from typing import List

from .db_engine import(
    Session, 
    get_session
)
from .models import (
    Drone,
    DroneRead,
    DroneCreate,
    DroneUpdate
)


#-------------------------------------------------------------------------------------------------#


drones_router = APIRouter()


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
                raise HTTPException(status_code=422, detail="weight_limit must be greater than 0 and under 500")
    
        if "battery_capacity" in drone_data.keys():
            if drone_data["battery_capacity"] > 100 or drone_data["battery_capacity"] < 0:
                 raise HTTPException(status_code=422, detail="battery_capacity must be greater than 0 and under 100")
    

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
