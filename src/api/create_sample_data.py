

import datetime
import numpy as np
import pandas as pd



dt = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2020, 1, 31, 23, 59, 59)
step = datetime.timedelta(hours=12)

DateTime = []

while dt < end:
    DateTime.append(dt.strftime('%Y-%m-%d %H:%M:%S'))
    dt += step


clinic_list = ['clinic_1b','clinic_2b','TCMSB','TCSOCK']

def generate_appt_data(DateTime,clinic):
    appt_load =  np.random.randint(5,20,len(DateTime))
    df = pd.DataFrame(list(zip(DateTime, appt_load)),  columns =['DateTime', 'appt_load'])
    df['clinic'] = clinic
    return df



def generate_queue_data(DateTime,clinic):
    queue_load_reg =  np.random.randint(8,20,len(DateTime))
    queue_load_pay =  np.random.randint(3,15,len(DateTime))
    queue_load_fin =  np.random.randint(1,10,len(DateTime))
    
    df = pd.DataFrame(list(zip(DateTime, queue_load_reg,queue_load_pay,queue_load_fin)),  columns =['DateTime','patient_load_reg', 'patient_load_pay','patient_load_fin'])
    df['clinic'] = clinic
    return df

appt_load = pd.concat([generate_appt_data(DateTime,clinic) for clinic in clinic_list])
session_load = pd.concat([generate_queue_data(DateTime,clinic) for clinic in clinic_list])

appt_load.to_csv('data/appt_load.csv', index=False)  
session_load.to_csv('data/session_load.csv', index=False)  

