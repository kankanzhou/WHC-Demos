

import pandas as pd
from pathlib import Path
import datetime


input_filepath = Path('data/') 

## dict for user input para
dict_clinic = {"1b": "clinic_1b",  "2b": "clinic_2b","temsb": "TCMSB","tcsock":"TCSOCK","all":"all"} 
dict_service = {"registraion": "patient_load_reg",  "payments": "patient_load_pay","financial_counselling": "patient_load_fin"} 

## load and pre-process appt data
f_appt ='appt_load.csv'
df_appt_load = pd.read_csv(input_filepath / f_appt, encoding="latin")
df_appt_load['DateTime'] = pd.to_datetime(df_appt_load['DateTime'], infer_datetime_format=True) 
df_appt_load['session'] = 'PM'
df_appt_load['session'][(df_appt_load['DateTime'].dt.hour == 0) ]= 'AM'
df_appt_load['date'] =df_appt_load['DateTime'].dt.date
df_appt_load= df_appt_load.set_index('date')
df_appt_load= df_appt_load.rename(columns={'appt_load':'num_appointments'}) 
df_appt_load_all = df_appt_load.groupby(['session','date'])['num_appointments'].sum().reset_index() 
df_appt_load_all = df_appt_load_all.set_index('date')

## load and pre-process queue data
f_queue ='session_load.csv'    
df_queue_load = pd.read_csv(input_filepath / f_queue, encoding="latin")
df_queue_load['DateTime'] = pd.to_datetime(df_queue_load['DateTime'], infer_datetime_format=True) 
df_queue_load['session'] = 'PM'
df_queue_load['session'][(df_queue_load['DateTime'].dt.hour == 0) ]= 'AM'
df_queue_load['date'] =df_queue_load['DateTime'].dt.date
df_queue_load = df_queue_load.set_index('date')
df_queue_load_all = df_queue_load.groupby(['session','date'])['patient_load_reg','patient_load_pay','patient_load_fin'].sum().reset_index() 
df_queue_load_all= df_queue_load_all.set_index('date')

    
def get_appt_load( start_date:datetime.date, end_date:datetime.date,clinic:str):

    assert clinic in dict_clinic, "Invalid clinic!"
    assert start_date<=end_date, "End date must greater or equal to start date!"
    
    if clinic == 'all':
        df = df_appt_load_all.loc[pd.date_range(start =start_date, end = end_date)].copy()
    else:
        df= df_appt_load[(df_appt_load['clinic']== dict_clinic[clinic])].loc[pd.date_range(start =start_date, end = end_date)][['num_appointments','session']].copy()
   
    return df.reset_index().to_dict('records') 


def get_queue_load(start_date:datetime.date, end_date:datetime.date,clinic:str,service_station:str):
    
    assert clinic in dict_clinic, "Invalid clinic!"
    assert start_date<=end_date, "End date must greater or equal to start date!"
    assert service_station in dict_service, "Invalid service station!"
    
    if clinic == 'all':
        df= df_queue_load_all.loc[pd.date_range(start =start_date, end = end_date)].rename(columns={dict_service[service_station]:'num_patients'}) [['num_patients','session']].copy()
    else:
        df= df_queue_load[(df_queue_load['clinic']== dict_clinic[clinic])].loc[pd.date_range(start =start_date, end = end_date)].rename(columns={dict_service[service_station]:'num_patients'})[['num_patients','session']].copy()

    return df.reset_index().to_dict('records') 
    
def main():

    
    clinic = '2b'
    start_date = pd.to_datetime('20200101', format='%Y%m%d', errors='ignore').date()
    end_date = pd.to_datetime('20200102', format='%Y%m%d', errors='ignore').date()

    service_station = 'payments'
    appt_workload =get_appt_load(start_date,end_date,clinic)

    queue_workload =get_queue_load(start_date,end_date,clinic,service_station)
    print(appt_workload)
    print(queue_workload)
    



if __name__ == "__main__":

    ## import lib not used for functions such as import plot 
    
    main() 


