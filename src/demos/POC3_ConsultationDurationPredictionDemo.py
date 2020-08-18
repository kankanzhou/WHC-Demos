import streamlit as st
from enum import Enum
from datetime import time

st.title("[WHC POC3] Consultation Duration Prediction")
created_date = st.date_input("Created or Modified Date")
patient_key = st.text_input("Patient Key")
case_number = st.text_input("Case Number")
appt_date = st.date_input("Appointment Date")
appt_time = st.slider("Appointment Time", value=time(11, 30), format="hh:mm a",)
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
doctor = st.selectbox("Room", ("M01", "M02", "M03"))
