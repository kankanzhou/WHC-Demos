import datetime
from pathlib import Path

import pandas as pd

input_filepath = Path("data/")

## dict for user input para
dict_clinic = {
    "1b": "clinic_1b",
    "2b": "clinic_2b",
    "tcmsb": "TCMSB",
    "tcsock": "TCSOCK",
    "all": "all",
}
dict_service = {
    "registration": "patient_load_reg",
    "payments": "patient_load_pay",
    "financial_counselling": "patient_load_fin",
    "all": "all",
}

## load and pre-process appt data
f_appt = "appt_load.csv"
f_queue = "session_load.csv"


df_appt_load = pd.read_csv(input_filepath / f_appt).rename(
    columns={"appt_load": "num_appointments"}
)
df_appt_load["date"] = pd.to_datetime(
    df_appt_load["DateTime"], infer_datetime_format=True
)

df_appt_load.set_index("date", inplace=True)
df_appt_load = pd.concat(
    [
        df_appt_load,
        df_appt_load.groupby(level=0)[["num_appointments"]].sum().assign(clinic="all"),
    ]
)

## load and pre-process queue data
df_queue_load = pd.read_csv(input_filepath / f_queue)
df_queue_load["date"] = pd.to_datetime(
    df_queue_load["DateTime"], infer_datetime_format=True
)
df_queue_load.set_index("date", inplace=True)

df_queue_load = pd.concat(
    [
        df_queue_load,
        df_queue_load.groupby(level=0)[
            ["patient_load_reg", "patient_load_pay", "patient_load_fin"]
        ]
        .sum()
        .assign(clinic="all"),
    ]
)


def get_appt_load(start_date: datetime.date, end_date: datetime.date, clinic: str):
    print(start_date, end_date, clinic)

    assert clinic in dict_clinic, "Invalid clinic!"
    assert start_date <= end_date, "End date must greater or equal to start date!"

    return (
        df_appt_load[(df_appt_load["clinic"] == dict_clinic[clinic])]
        .loc[start_date:end_date, ["num_appointments"]]
        .reset_index()
        .to_dict("records")
    )


def get_queue_load(
    start_date: datetime.date,
    end_date: datetime.date,
    clinic: str,
    service_station: str,
):
    print(start_date, end_date, clinic, service_station)

    assert clinic in dict_clinic, "Invalid clinic!"
    assert start_date <= end_date, "End date must greater or equal to start date!"
    assert service_station in dict_service, "Invalid service station!"

    return (
        df_queue_load[(df_queue_load["clinic"] == dict_clinic[clinic])]
        .loc[start_date:end_date]
        .rename(columns={dict_service[service_station]: "num_patients"})[
            ["num_patients"]
        ]
        .reset_index()
        .to_dict("records")
    )


if __name__ == "__main__":
    clinic = "all"
    start_date = pd.to_datetime("20200101", format="%Y%m%d", errors="ignore").date()
    end_date = pd.to_datetime("20200102", format="%Y%m%d", errors="ignore").date()

    service_station = "payments"
    appt_workload = get_appt_load(start_date, end_date, clinic)
    print(appt_workload)

    queue_workload = get_queue_load(start_date, end_date, clinic, service_station)
    print(queue_workload)
