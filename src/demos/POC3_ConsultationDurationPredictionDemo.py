import streamlit as st
from enum import Enum
from datetime import time
import numpy as np

st.title("[WHC POC3] Consultation Duration Prediction")
created_date = st.date_input("Created or Modified Date")
patient_key = st.text_input("Patient Key")
case_number = st.text_input("Case Number")
appt_date = st.date_input("Appointment Date")
appt_time = st.slider(
    "Appointment Time",
    min_value=time(8, 0),
    max_value=time(18, 0),
    value=time(11, 30),
    format="hh:mm a",
)
st.selectbox(
    "Appointment Type",
    (
        "General Consultation",
        "Retina (Medical) Consultation",
        "Glaucoma Consultation",
        "Compre Discharge Consultation",
        "Oculoplastic Consultation",
        "Retina (Surgical) Consultation",
        "Direct Access Consultation",
        "Uveitis Consultation",
        "Post Op Consultation",
    ),
)
visit_type = st.selectbox("Visit Type", ("RV", "FV", "TT", "AF"),)
patient_class = st.selectbox("Patient Class", ("SUB", "PTE", "FS"))
room = st.selectbox("Room", ("RM01", "RM02", "RM03"))
doctor = st.selectbox("Doctor", ("M01", "M02", "M03"))
user_input = st.text_area("Appointment Notes")


prediction = np.random.randint(2, 30)
st.sidebar.title("WHC Consultation Duration Prediction")


if st.sidebar.button("Predict"):
    st.sidebar.header(f"Expected appointment duration: {prediction} minutes")
