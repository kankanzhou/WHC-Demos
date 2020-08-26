import requests
import pandas as pd

from numpy.random import normal
from numpy import sqrt, int_

url = "http://localhost:8000/"


stations_dict = {
    "Overall Aggregated": "all",
    "Registration": "registration",
    "FC": "financial_counselling",
    "Payment": "payments",
}
clinics_dict = {
    "Clinic 1b": "1b",
    "Clinic 2b": "2b",
    "TCMSB": "tcmsb",
    "TCSOCK": "tcsock",
    "Overall Aggregated": "all",
}

def get_workload_trend(start_date, end_date, station, clinic):
    params = dict(
        serviceStation=stations_dict[station],
        clinic=clinics_dict[clinic],
        end_date=end_date.strftime('%Y-%m-%d'),
        start_date=start_date.strftime('%Y-%m-%d')
        )
    print(params)
    response = requests.get(
    url + "historical_workload",
    params=params)

    df = pd.read_json(response.content)
    if len(df) > 0:
        print(df)
        return df.T.values
    return None, None


def get_appointments(start_date, end_date, clinic):
    params = dict(
        clinic=clinics_dict[clinic],
        end_date=end_date.strftime('%Y-%m-%d'),
        start_date=start_date.strftime('%Y-%m-%d')
        )
    print(params)
    response = requests.get(
    url + "appointments",
    params=params)

    df = pd.read_json(response.content)
    if len(df) > 0:
        return df.T.values
    return None, None


def get_workload_pred(start_date, end_date, station, clinic):
    x, y = get_workload_trend(start_date, end_date, station, clinic)
    noise = [normal(0, sqrt(k)) for k in y]
    y += noise
    return x, int_(y)


# if __name__ == "__main__":
#     print(get_workload_trend('2020-01-07', '2020-01-20', 'registration', clinic))

    

