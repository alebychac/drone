# coding=utf-8


#-------------------------------------------------------------------------------------------------#


from typing import List, Optional

from datetime import datetime

from enum import Enum

from sqlmodel import Field, Relationship, SQLModel, DateTime

from sqlalchemy import Column


#-------------------------------------------------------------------------------------------------#


class DroneModel(str, Enum):
    light_weight = "Lightweight"
    middle_weight = "Middleweight"
    cruiser_weight = "Cruiserweight"
    heavy_weight = "Heavyweight"


class DroneState(str, Enum):
    idle = "IDLE"
    loading = "LOADING"
    loaded = "LOADED"
    delivering = "DELIVERING"
    delivered = "DELIVERED"
    returning = "RETURNING"


#-------------------------------------------------------------------------------------------------#


class DroneBase(SQLModel):
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column("created_at", DateTime(timezone=True)))
    last_update: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column("last_update", DateTime(timezone=True)))
    serial_number: str = Field(max_length=100, unique=True)
    model: Optional[DroneModel] = None
    weight_limit: float = Field(ge=0, le=500)
    battery_capacity: float = Field(ge=0, le=100)    
    state: Optional[DroneState] = None


class Drone(DroneBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    medications: List["Medication"] = Relationship(back_populates="drone")


class DroneCreate(DroneBase):
    pass


class DroneRead(DroneBase):
    id: int


class DroneUpdate(SQLModel):
    last_update: Optional[datetime] = datetime.utcnow()
    serial_number: Optional[str] = None
    model: Optional[DroneModel] = None
    weight_limit: Optional[float] = 0
    battery_capacity: Optional[float] = 0  
    state: Optional[DroneState] = None


#-------------------------------------------------------------------------------------------------#


class MedicationBase(SQLModel):
    name: str = Field(regex=r"^[a-zA-Z0-9-_]+$") # allowed only letters, numbers, ‘-‘, ‘_’
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column("created_at", DateTime(timezone=True)))
    last_update: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column("last_update", DateTime(timezone=True)))
    weight: float = Field(ge=1)
    code: str = Field(regex=r"^[A-Z0-9_]+$", unique=True) # allowed only upper case letters, underscore and numbers);
    image: str = Field()
    drone_id: Optional[int] = Field(default=None, foreign_key="drone.id")


class Medication(MedicationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    drone: Optional[Drone] = Relationship(back_populates="medications")


class MedicationRead(MedicationBase):
    id: int


class MedicationCreate(MedicationBase):
    pass


class MedicationUpdate(SQLModel):
    name: Optional[str] = None
    last_update: Optional[datetime] = datetime.utcnow()
    weight: Optional[float] = 0
    code: Optional[str] = None
    image: Optional[str] = None
    drone_id: Optional[int] = None


#-------------------------------------------------------------------------------------------------#

