from fastapi import FastAPI
import datetime
from .models import Appointments, Workload, Locations
from typing import List

app = FastAPI()


@app.get("/")
async def root():
    return {"status": "200 OK"}


@app.get("/appointments", response_model=List[Appointments])
async def read_item(start_date: datetime.date, end_date: datetime.date):
    res: List[Appointments] = []
    return res


@app.get("/historical_workload/{location}", response_model=List[Workload])
async def read_item(
    location: Locations, start_date: datetime.date, end_date: datetime.date
):
    res: List[Workload] = []
    return res


@app.get("/predicted_workload/{location}", response_model=List[Workload])
async def read_item(location: Locations, start_date: datetime.date):
    res: List[Workload] = []
    return res
