# coding=utf-8


#-------------------------------------------------------------------------------------------------#


from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from typing import List
from re import match

from app.db_engine import(
    Session, 
    get_session
)

from app.models.drone import Drone
from app.models.medication import Medication, MedicationCreate, MedicationRead, MedicationUpdate


#-------------------------------------------------------------------------------------------------#


medications_router = APIRouter()


#-------------------------------------------------------------------------------------------------#


#                       _       
#                      | |      
#    ___ _ __ ___  __ _| |_ ___ 
#   / __| '__/ _ \/ _` | __/ _ \
#  | (__| | |  __/ (_| | ||  __/
#   \___|_|  \___|\__,_|\__\___|


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


#-------------------------------------------------------------------------------------------------#


#              _   
#             | |  
#    __ _  ___| |_ 
#   / _` |/ _ \ __|
#  | (_| |  __/ |_ 
#   \__, |\___|\__|
#    __/ |         
#   |___/          


@medications_router.get("/medications/", response_model=List[MedicationRead])
def get_medications(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    medications = session.exec(select(Medication).offset(offset).limit(limit)).all()
    return medications


@medications_router.get("/medications/{medication_id}", response_model=MedicationRead)
def get_medication(*, session: Session = Depends(get_session), medication_id: int):
    medication = session.get(Medication, medication_id)
    if not medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    return medication


@medications_router.get("/medications/code/{code}", response_model=MedicationRead)
def get_medication_by_code(*, session: Session = Depends(get_session), code: str):
    query = select(Medication).where(Medication.code == code)
    medication = session.exec(query).first()
    if not medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    return medication


#-------------------------------------------------------------------------------------------------#


#                   _       _       
#                  | |     | |      
#   _   _ _ __   __| | __ _| |_ ___ 
#  | | | | '_ \ / _` |/ _` | __/ _ \
#  | |_| | |_) | (_| | (_| | ||  __/
#   \__,_| .__/ \__,_|\__,_|\__\___|
#        | |                        
#        |_|         


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


#-------------------------------------------------------------------------------------------------#


#       _      _      _       
#      | |    | |    | |      
#    __| | ___| | ___| |_ ___ 
#   / _` |/ _ \ |/ _ \ __/ _ \
#  | (_| |  __/ |  __/ ||  __/
#   \__,_|\___|_|\___|\__\___|
                                      

@medications_router.delete("/medications/{medication_id}")
def delete_medication(*, session: Session = Depends(get_session), medication_id: int):
    medication = session.get(Medication, medication_id)
    if not medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    session.delete(medication)
    session.commit()
    return {"ok": True}


#-------------------------------------------------------------------------------------------------#

