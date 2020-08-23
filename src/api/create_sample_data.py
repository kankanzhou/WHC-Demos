import datetime
import numpy as np
import pandas as pd

from numpy.random import normal


class Clinic(object):
    def __init__(self, clinic_name, start_date, stop_date, frequency):
        self.clinic_name = clinic_name
        self.start_date = start_date
        self.stop_date = stop_date
        self.frequency = frequency
        self.date_range()

        self._mean_weekly_appt = 80
        self._mean_weekend_appt = 10

        self._registration_factors = (0.9, 0.2)
        self._payment_factors = (0.7, 0.2)
        self._fc_factors = (0.1, 0.2)

    def date_range(self):
        retval = pd.date_range(
            self.start_date, self.stop_date, freq=self.frequency, name="DateTime"
        )
        self._date_range = retval[retval.weekday != 6]
        self._saturdays = retval[retval == 5]
        self._len = len(self._date_range)

    def generate_appt_data(self):
        retval = normal(
            self._mean_weekly_appt, np.sqrt(self._mean_weekly_appt), self._len
        )

        retval[self._date_range.weekday == 5] = normal(
            self._mean_weekend_appt,
            np.sqrt(self._mean_weekend_appt),
            (self._date_range.weekday == 5).sum(),
        )

        retval = pd.DataFrame(
            retval, index=self._date_range, columns=["appt_load"]
        ).astype(int)
        retval["clinic"] = self.clinic_name
        self._appt_data = retval
        return retval

    def generate_queue_data(self):
        retval = pd.concat(
            [
                self._appt_data["appt_load"]
                .mul(normal(k[0], k[1], self._len), axis=0)
                .astype(int)
                .clip(0, None)
                for k in [
                    self._registration_factors,
                    self._payment_factors,
                    self._fc_factors,
                ]
            ],
            axis=1,
        )
        retval.columns = [
            "patient_load_reg",
            "patient_load_pay",
            "patient_load_fin",
        ]
        self._queue_data = retval
        retval["clinic"] = self.clinic_name
        return retval


if __name__ == "__main__":

    clinic_list = ["clinic_1b", "clinic_2b", "TCMSB", "TCSOCK"]
    start_date = "2020-01-01"
    stop_date = "2020-09-30"
    frequency = "12H"

    clinics = {Clinic(k, start_date, stop_date, frequency) for k in clinic_list}

    # clinic.generate_appt_data()
    # clinic.generate_queue_data()
    # print(clinic._appt_data)
    # print(clinic._queue_data)

    appt_load = pd.concat([k.generate_appt_data() for k in clinics])
    session_load = pd.concat([k.generate_queue_data() for k in clinics])

    appt_load.to_csv("data/appt_load.csv")
    session_load.to_csv("data/session_load.csv")
