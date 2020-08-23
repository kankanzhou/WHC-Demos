from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, HoverTool
from bokeh.plotting import figure

from data_fns import get_appointments, get_workload_pred, get_workload_trend

BOKEH_TOOLS = "pan,wheel_zoom,box_zoom,reset"
SOC_LOCATIONS = ("Registration", "FC", "Payment")
SOC_CLINICS = ("Overall Aggregated", "Clinic 1b", "Clinic 2b", "TCMSB", "TCSOCK")
DAYS_BEFORE_TO_SHOW = 30
DAYS_TO_PREDICT = 7

# USER INPUT ============================================
st.sidebar.title("WHC SOC Workload Prediction")
st.sidebar.markdown("## Demo Settings")
today_date = st.sidebar.date_input("Today's Date")

# Convert to dates
today_date = datetime.combine(today_date, datetime.min.time())

# UI STARTS ==========================================

st.title("[WHC POC4] SOC Workload Prediction")
location = st.selectbox("Select Station", SOC_LOCATIONS)
clinic = st.selectbox("Select Clinic", SOC_CLINICS)

x_appt, y_appt = get_appointments(
    today_date - timedelta(days=DAYS_BEFORE_TO_SHOW),
    today_date + timedelta(days=DAYS_TO_PREDICT),
    clinic,
)

x_trend, y_trend = get_workload_trend(
    today_date - timedelta(days=DAYS_BEFORE_TO_SHOW), today_date, location, clinic
)
x_pred, y_pred = get_workload_pred(
    today_date, today_date + timedelta(days=DAYS_TO_PREDICT), location, clinic
)

# Mock Datatable
datatable = pd.DataFrame(
    get_workload_pred(
        today_date, today_date + timedelta(days=DAYS_TO_PREDICT), "Registration", clinic
    )
)
datatable = datatable.T
datatable.columns = ["Session", "Registration"]
datatable["Registration"] = get_workload_pred(today_date, today_date + timedelta(days=DAYS_TO_PREDICT), "Registration", clinic)[1]
datatable["Payment"] = get_workload_pred(
    today_date, today_date + timedelta(days=DAYS_TO_PREDICT), "Payment", clinic
)[1]
datatable["FC"] = get_workload_pred(
    today_date, today_date + timedelta(days=DAYS_TO_PREDICT), "FC", clinic
)[1]


st.write(f"### SOC 30Day (+7Day Predicted) Workload for {location}")
p = figure(
    x_axis_label="Day",
    y_axis_label="Expected Number of Patients",
    plot_height=400,
    x_axis_type="datetime",
    tools=BOKEH_TOOLS,
)
p.xaxis.formatter = DatetimeTickFormatter(
    hours=["%I %p %d/%m"], days=["%d/%m %a"], months=["%d %b %Y"], years=["%Y"],
)
p.add_tools(
    HoverTool(
        tooltips=[
            ("Date", "@x{%a %d/%m %p}"),
            ("#Patients", "@y",),  # use @{ } for field names with spaces
        ],
        formatters={"@x": "datetime",},  # use 'datetime' formatter for '@date' field
        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode="vline",
    )
)
p.line(
    x_appt,
    y_appt,
    legend_label="Planned Appointments",
    line_width=1,
    color="grey",
    line_dash="dashed",
)
p.line(
    x_trend, y_trend, legend_label="Trend", line_width=2,
)
p.line(
    x_pred,
    y_pred,
    legend_label="Predicted",
    line_width=4,
    color="red",
    line_dash="dashed",
)
p.legend.location = "top_left"

st.bokeh_chart(p, use_container_width=True)

st.header('Forecast')
st.table(datatable.style.hide_index().format({"Session": "{:%a %d-%m-%Y %p}"}))