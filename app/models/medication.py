# coding=utf-8


#-------------------------------------------------------------------------------------------------#


from typing import Optional, TYPE_CHECKING

from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel, DateTime

from sqlalchemy import Column

if TYPE_CHECKING:
    from app.models.drone import Drone


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
    drone: Optional["Drone"] = Relationship(back_populates="medications")


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

