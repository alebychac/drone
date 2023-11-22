# coding=utf-8


#-------------------------------------------------------------------------------------------------#


from datetime import datetime

from sqlmodel import Field, SQLModel


#-------------------------------------------------------------------------------------------------#


class DroneBatteryLog(SQLModel, table=True):
    id: int = Field(primary_key=True)
    drone_id: int = Field(foreign_key="drone.id")
    battery_level: float = Field()
    timestamp: datetime = Field(default_factory=datetime.now)


#-------------------------------------------------------------------------------------------------#

