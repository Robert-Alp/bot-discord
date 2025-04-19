from fastapi import FastAPI
from api.v1 import apiv1
from database import init_database

init_database()

app = FastAPI()

app.include_router(apiv1)
