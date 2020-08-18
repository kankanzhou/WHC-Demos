def get_appt_load(st_date, ed_date, clinic):

    input_filepath = Path("C:/Temp/")
    f_name = "appt_load.csv"

    df = pd.read_csv(input_filepath / f_name, encoding="latin")

    df["DateTime"] = pd.to_datetime(df["DateTime"], infer_datetime_format=True)

    df["session"] = "PM"

    mask = df["DateTime"].dt.strftime("%H:%M:%S").str[:2] == "00"
    df["session"][mask] = "AM"

    df["date"] = df["DateTime"].dt.date

    df = df[(df["DateTime"] >= st_date) & (df["DateTime"] <= ed_date)]

    df = df.rename(columns={"appt_load": "num_appointments"})
    df = df.drop(columns=["DateTime"])

    if clinic == "1b":
        df = df[df["clinic"] == "clinic_1b"]
        df = df.drop(columns=["clinic"])

    elif clinic == "2b":
        df = df[df["clinic"] == "clinic_2b"]
        df = df.drop(columns=["clinic"])

    elif clinic == "temsb":
        df = df[df["clinic"] == "TCMSB"]
        df = df.drop(columns=["clinic"])

    elif clinic == "tcsock":
        df = df[df["clinic"] == "TCSOCK"]
        df = df.drop(columns=["clinic"])

    elif clinic == "all":
        df = df.groupby(["session", "date"])["num_appointments"].sum().reset_index()

    else:

        print("Select not defined!")

    dict_a = df.to_dict("records")
    return [key for key in dict_a]


def get_queue_load(st_date, ed_date, clinic, service_station):

    input_filepath = Path("C:/Temp/")

    f_name = "session_load.csv"

    df = pd.read_csv(input_filepath / f_name, encoding="latin")

    df["DateTime"] = pd.to_datetime(df["DateTime"], infer_datetime_format=True)

    df["session"] = "PM"

    mask = df["DateTime"].dt.strftime("%H:%M:%S").str[:2] == "00"
    df["session"][mask] = "AM"

    df["date"] = df["DateTime"].dt.date

    df = df[(df["DateTime"] >= st_date) & (df["DateTime"] <= ed_date)]

    if service_station == "registraion":
        df["num_patients"] = df["patient_load_reg"]
    elif service_station == "payments":
        df["num_patients"] = df["patient_load_pay"]
    elif service_station == "financial_counselling":
        df["num_patients"] = df["patient_load_fin"]
    else:
        print("Select not defined!")

    df = df.drop(
        columns=["DateTime", "patient_load_reg", "patient_load_pay", "patient_load_fin"]
    )

    if clinic == "1b":
        df = df[df["clinic"] == "clinic_1b"]
        df = df.drop(columns=["clinic"])

    elif clinic == "2b":
        df = df[df["clinic"] == "clinic_2b"]
        df = df.drop(columns=["clinic"])

    elif clinic == "temsb":
        df = df[df["clinic"] == "TCMSB"]
        df = df.drop(columns=["clinic"])

    elif clinic == "tcsock":
        df = df[df["clinic"] == "TCSOCK"]
        df = df.drop(columns=["clinic"])

    elif clinic == "all":
        df = df.groupby(["session", "date"])["num_patients"].sum().reset_index()

    else:

        print("Select not defined!")

    dict_a = df.to_dict("records")
    return [key for key in dict_a]


def main():
    import pandas as pd
    from pathlib import Path

    start_date = pd.to_datetime("20160101", format="%Y%m%d", errors="ignore")
    end_date = pd.to_datetime("20210117", format="%Y%m%d", errors="ignore")

    clinic = "all"
    service_station = "financial_counselling"

    queue_workload = get_queue_load(start_date, end_date, clinic, service_station)
    appt_workload = get_appt_load(start_date, end_date, clinic)

    print(queue_workload)
    print(appt_workload)


if __name__ == "__main__":
    main()
