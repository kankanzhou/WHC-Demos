from enum import Enum
from pydantic import BaseModel
from typing import List, Optional
import datetime


class Locations(str, Enum):
    REG = "registration"
    PAY = "payments"
    FC = "financial_counselling"
    ALL = "all"


class Session(str, Enum):
    AM = "AM"
    PM = "PM"


class Appointments(BaseModel):
    date: datetime.date
    session: Session
    num_appointments: int


class Workload(BaseModel):
    date: datetime.date
    session: Session
    num_patients: int
