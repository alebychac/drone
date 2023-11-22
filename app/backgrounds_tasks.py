# coding=utf-8


#-------------------------------------------------------------------------------------------------#


from fastapi import Depends
from sqlmodel import select
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from dotenv import load_dotenv
from os import getenv

from .db_engine import get_session_2
from .models.drone import Drone
from .models.drone_battery_log import DroneBatteryLog


#-------------------------------------------------------------------------------------------------#


load_dotenv()


def check_battery_levels():
    session = get_session_2()
    drones = session.query(Drone).all()
    for drone in drones:
        audit_log = DroneBatteryLog(
            drone_id=drone.id,
            battery_level=drone.battery_capacity,
            timestamp=datetime.now()
        )
        session.add(audit_log)
    session.commit()
    session.close()


#-------------------------------------------------------------------------------------------------#


CHECK_BATTERY_LEVELS_MINUTES_INTERVAL = int(getenv("CHECK_BATTERY_LEVELS_MINUTES_INTERVAL"))
scheduler = BackgroundScheduler()
scheduler.add_job(check_battery_levels, 'interval', minutes=CHECK_BATTERY_LEVELS_MINUTES_INTERVAL) 


#-------------------------------------------------------------------------------------------------#

