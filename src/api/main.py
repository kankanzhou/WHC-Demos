import datetime
from typing import List, Optional

from fastapi import FastAPI
from ETL_for_view import get_appt_load, get_queue_load

from models import Appointments, Clinics, ServiceStations, Workload

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
    res: List[Appointments] = get_appt_load(
        start_date, end_date, clinic,
    )
    return res


@app.get("/historical_workload", response_model=List[Workload])
async def read_item(
    start_date: datetime.date,
    end_date: datetime.date,
    clinic: Optional[Clinics] = Clinics.ALL,
    serviceStation: Optional[ServiceStations] = ServiceStations.REG,
):
    res: List[Workload] = get_queue_load(start_date, end_date, clinic, serviceStation)
    return res


@app.get("/predicted_workload", response_model=List[Workload])
async def read_item(
    start_date: datetime.date,
    clinic: Optional[Clinics] = Clinics.ALL,
    serviceStation: Optional[ServiceStations] = ServiceStations.REG,
):
    res: List[Workload] = []
    return res
