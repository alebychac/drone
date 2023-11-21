from fastapi import FastAPI, APIRouter

from .db_engine import *
from .models import *
from .endpoints import drone_router


app = FastAPI()

api_router = APIRouter()
api_router.include_router(drone_router)

app.include_router(api_router, prefix=f"/api/v1")

@app.get("/")
def root():
    return {
        "message": "Home",
    }


create_db_and_tables()