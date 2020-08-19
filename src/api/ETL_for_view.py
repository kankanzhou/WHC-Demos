
import pandas as pd
from pathlib import Path
import datetime

input_filepath = Path('data/') 
f_appt ='appt_load.csv'
df_appt_load = pd.read_csv(input_filepath / f_name, encoding="latin")
df_appt_load['DateTime'] = pd.to_datetime(df_appt_load['DateTime'], infer_datetime_format=True) 
df_appt_load['session'] = 'PM'
mask = df_appt_load['DateTime'].dt.strftime('%H:%M:%S').str[:2]=='00'
df_appt_load['session'][mask] ='AM'
df_appt_load['date'] =df_appt_load['DateTime'].dt.date
df_appt_load= df_appt_load.rename(columns={'appt_load':'num_appointments'}) 

f_queue ='session_load.csv'    
df_queue_load = pd.read_csv(input_filepath / f_name, encoding="latin")


def get_appt_load( start_date:datetime.date, end_date:datetime.date,clinic:str):

    ## assert clinic is in the key of the dictionary if assert fail raise an error
    ## assert the end_date > start_date
    ## type checking 
    ## use date range

    df= df_appt_load[(df_appt_load['DateTime'] >= st_date) & (df_appt_load['DateTime'] <= ed_date)][['clinic']].copy()

    df= df.drop(columns=['DateTime'])

    ## create a dictionary outside
    if clinic == '1b':
        df = df[df['clinic']=='clinic_1b'] 
        df =df.drop(columns=['clinic']) 
    
    elif clinic == '2b':
        df = df[df['clinic']=='clinic_2b'] 
        df =df.drop(columns=['clinic']) 

    elif clinic == 'temsb':
        df = df[df['clinic']=='TCMSB'] 
        df =df.drop(columns=['clinic']) 
    
    elif clinic == 'tcsock':
        df = df[df['clinic']=='TCSOCK'] 
        df =df.drop(columns=['clinic']) 
    
    ## create group by into dataframe with clinic = 'all'
    elif clinic == 'all':
        df = df.groupby(['session','date'])['num_appointments'].sum().reset_index() 
    
    else:
    
        print("Select not defined!") 
        
    return df.to_dict('records') 
 



def get_queue_load(st_date, ed_date,clinic,service_station):
    

    
    
    df['DateTime'] = pd.to_datetime(df['DateTime'], infer_datetime_format=True) 
    
    df['session'] = 'PM'
    
    mask = df['DateTime'].dt.strftime('%H:%M:%S').str[:2]=='00'
    df['session'][mask] ='AM'
    
    df['date'] =df['DateTime'].dt.date
    
    df= df[(df['DateTime'] >= st_date) & (df['DateTime'] <= ed_date)]
    
    
    ## df.rename(columns={dict_value:'num_patients'})
    if service_station == 'registraion':
        df['num_patients'] = df['patient_load_reg']    
    elif service_station == 'payments':
        df['num_patients'] = df['patient_load_pay']
    elif service_station == 'financial_counselling':
        df['num_patients'] = df['patient_load_fin']
    else:    
        print("Select not defined!") 
        
    df = df.drop(columns = ['DateTime','patient_load_reg','patient_load_pay','patient_load_fin'])
    
    if clinic == '1b':
        df = df[df['clinic']=='clinic_1b'] 
        df =df.drop(columns=['clinic']) 
    
    elif clinic == '2b':
        df = df[df['clinic']=='clinic_2b'] 
        df =df.drop(columns=['clinic']) 

    elif clinic == 'temsb':
        df = df[df['clinic']=='TCMSB'] 
        df =df.drop(columns=['clinic']) 
    
    elif clinic == 'tcsock':
        df = df[df['clinic']=='TCSOCK'] 
        df =df.drop(columns=['clinic']) 
    
    elif clinic == 'all':
        df = df.groupby(['session','date'])['num_patients'].sum().reset_index() 
    
    else:
    
        print("Select not defined!") 
        
    return df.to_dict('records') 
    
def main():

    
    start_date = pd.to_datetime('20160101', format='%Y%m%d', errors='ignore')
    end_date = pd.to_datetime('20210117', format='%Y%m%d', errors='ignore')
    
    clinic='all'
    service_station = 'financial_counselling'
    
    queue_workload = get_queue_load(start_date,end_date,clinic,service_station)
    appt_workload = get_appt_load(start_date,end_date,clinic)
    print(queue_workload[0])
    print(appt_workload[0])



if __name__ == "__main__":

    ## import lib not used for functions such as import plot 
    
    main() 


