from fastapi import FastAPI
import datetime
from .models import Appointments, Workload, ServiceStations, Clinics
from typing import List, Optional

app = FastAPI()


@app.get("/")
async def root():
    return {"status": "200 OK"}


@app.get("/appointments", response_model=List[Appointments])
async def read_item(
    start_date: datetime.date,
    end_date: datetime.date,
    clinic: Optional[Clinics] = Clinics.ALL,
):
    res: List[Appointments] = []
    return res


@app.get("/historical_workload", response_model=List[Workload])
async def read_item(
    start_date: datetime.date,
    end_date: datetime.date,
    clinic: Optional[Clinics] = Clinics.ALL,
    serviceStation: Optional[ServiceStations] = ServiceStations.ALL,
):
    res: List[Workload] = []
    return res


@app.get("/predicted_workload", response_model=List[Workload])
async def read_item(
    start_date: datetime.date,
    clinic: Optional[Clinics] = Clinics.ALL,
    serviceStation: Optional[ServiceStations] = ServiceStations.ALL,
):
    res: List[Workload] = []
    return res
