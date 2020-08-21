import streamlit as st
from bokeh.plotting import figure
import pandas as pd
from datetime import datetime, timedelta
from bokeh.models import DatetimeTickFormatter, ColumnDataSource, HoverTool
from Mock import get_workload_pred, get_workload_trend, get_appointments

BOKEH_TOOLS = "pan,wheel_zoom,box_zoom,reset"
SOC_LOCATIONS = ("Overall Aggregated", "Registration", "FC", "Payment")
DAYS_BEFORE_TO_SHOW = 30
DAYS_TO_PREDICT = 7

# USER INPUT ============================================
st.sidebar.title("WHC SOC Workload Prediction")
st.sidebar.markdown("## Demo Settings")
today_date = st.sidebar.date_input("Today's Date")

# DATA PROCESSING =======================================

x_trend, y_trend = get_workload_trend(DAYS_BEFORE_TO_SHOW)
x_pred, y_pred = get_workload_pred(DAYS_TO_PREDICT)
x_appt, y_appt = get_appointments(DAYS_BEFORE_TO_SHOW + DAYS_TO_PREDICT)

# Convert to dates
today_date = datetime.combine(today_date, datetime.min.time())
x_trend = [today_date - timedelta(days=DAYS_BEFORE_TO_SHOW - inc) for inc in x_trend[:-1]]
x_pred = [today_date + timedelta(days=inc) for inc in x_pred]
x_appt = [today_date + timedelta(days=inc - DAYS_BEFORE_TO_SHOW) for inc in x_appt]

# Ensure that trend and predicted lines "join" up, by making the first value in
# pred line the last value in trend line
x_pred = [x_trend[-1]] + x_pred
y_pred = [y_trend[-1]] + y_pred

# Mock Datatable
datatable = pd.DataFrame({"Day": x_pred, "Overall": y_pred,})
datatable["Registration"] = datatable["Overall"].apply(lambda x: round(x * 0.4))
datatable["Payments"] = datatable["Overall"].apply(lambda x: round(x * 0.4))
datatable["FC"] = datatable["Overall"].apply(
    lambda x: round(x * 0.2)
)

# UI STARTS ==========================================

st.title("[WHC POC4] SOC Workload Prediction")
location = st.selectbox("Select Location", SOC_LOCATIONS)
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

st.write(datatable)

