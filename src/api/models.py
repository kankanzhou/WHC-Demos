from enum import Enum
from pydantic import BaseModel
from typing import List, Optional
import datetime


class ServiceStations(str, Enum):
    REG = "registration"
    PAY = "payments"
    FC = "financial_counselling"
    # ALL = "all"


class Clinics(str, Enum):
    CLINIC_1B = "1b"
    CLINIC_2B = "2b"
    TCMSB = "tcmsb"
    TCSOCK = "tcsock"
    ALL = "all"


# class Session(str, Enum):
#     AM = "AM"
#     PM = "PM"


class Appointments(BaseModel):
    date: datetime.datetime
    # session: Session
    num_appointments: int


class Workload(BaseModel):
    date: datetime.datetime
    # session: Session
    num_patients: int
