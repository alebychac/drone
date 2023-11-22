# coding=utf-8


#-------------------------------------------------------------------------------------------------#


from typing import List, Optional

from datetime import datetime

from enum import Enum

from sqlmodel import Field, Relationship, SQLModel, DateTime

from sqlalchemy import Column

from .enums import DroneModel, DroneState

from .medication import Medication


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

