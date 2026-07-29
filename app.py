import json
import pickle
from datetime import date

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Rain Tomorrow Predictor",
    page_icon="🌦️",
    layout="wide",
)

with open("model_meta.json") as f:
    META = json.load(f)

with open("rain_prediction_model.pkl", "rb") as f:
    MODEL = pickle.load(f)

NUM_RANGES = META["numeric_ranges"]
CAT_OPTIONS = META["categorical_options"]
CLIP_BOUNDS = META["clip_bounds"]
WIND_DIRS = CAT_OPTIONS["WindGustDir"]
LOCATIONS = CAT_OPTIONS["Location"]

CUSTOM_CSS = """
<style>
.stApp {
    background: linear-gradient(180deg, #0f2027 0%, #203a43 45%, #2c5364 100%);
}
[data-testid="stHeader"] { background: rgba(0,0,0,0); }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #14232e 0%, #1c333f 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}

.hero {
    padding: 1.6rem 2rem;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(255,255,255,0.10), rgba(255,255,255,0.03));
    border: 1px solid rgba(255,255,255,0.12);
    margin-bottom: 1.4rem;
}
.hero h1 { color: #ffffff; font-size: 2.1rem; margin-bottom: 0.2rem; }
.hero p { color: #cfe8f3; font-size: 1.02rem; margin: 0; }

.icon-banner {
    text-align: center;
    font-size: 3.2rem;
    margin-bottom: 0.4rem;
}

label, .stMarkdown, p, span, div { color: #eaf6fb; }

div[data-baseweb="select"] > div, .stNumberInput input, .stDateInput input {
    background-color: rgba(255,255,255,0.08) !important;
    color: #ffffff !important;
    border-radius: 8px !important;
}

.stButton>button, .stFormSubmitButton>button {
    background: linear-gradient(135deg, #36d1dc, #5b86e5);
    color: white;
    font-weight: 600;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.4rem;
    width: 100%;
}
.stButton>button:hover, .stFormSubmitButton>button:hover { filter: brightness(1.08); }

.result-card {
    padding: 1.6rem 2rem;
    border-radius: 18px;
    margin-top: 0.6rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.15);
}
.tier-0 { background: linear-gradient(135deg, #f7971e, #ffd200); }
.tier-1 { background: linear-gradient(135deg, #a8e063, #56ab2f); }
.tier-2 { background: linear-gradient(135deg, #7f8c9a, #5c7080); }
.tier-3 { background: linear-gradient(135deg, #3a6186, #89253e); }
.tier-4 { background: linear-gradient(135deg, #232526, #0f2027); }
.tier-0 h2, .tier-0 p { color: #1f1300 !important; }
.tier-1 h2, .tier-1 p { color: #10240a !important; }
.tier-2 h2, .tier-2 p, .tier-3 h2, .tier-3 p, .tier-4 h2, .tier-4 p { color: #ffffff !important; }
.result-card h2 { margin: 0 0 0.3rem 0; font-size: 1.85rem; }

.summary-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 14px;
    padding: 1rem 1.4rem;
    margin-top: 1rem;
}
.summary-card h4 { margin-top: 0; color: #cfe8f3; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.markdown(
    """
    <div class="hero">
        <h1>🌦️ Rain Tomorrow Predictor</h1>
        <p>weatherAUS — Machine Learning for Data Analysis · NTI Creativa Innovation Hubs (Benha)</p>
        <p>Fill in today's weather observations from the sidebar, then predict whether it will rain tomorrow.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


def slider(label, col, key, step=None, help_text=None):
    r = NUM_RANGES[col]
    lo, hi, med = r["min"], r["max"], r["median"]
    if step is None:
        step = 1.0 if hi - lo > 20 else 0.1
    return st.slider(label, min_value=float(lo), max_value=float(hi), value=float(med), step=step, help=help_text, key=key)


with st.sidebar:
    st.markdown("## 🧭 Weather Inputs")

    with st.form("weather_form"):
        with st.expander("📍 General", expanded=True):
            location = st.selectbox("Location", LOCATIONS, index=LOCATIONS.index("Canberra") if "Canberra" in LOCATIONS else 0)
            obs_date = st.date_input("Observation date", value=date(2017, 6, 1))
            rain_today = st.selectbox("Rain today?", CAT_OPTIONS["RainToday"])

        with st.expander("🌡️ Temperature"):
            min_temp = slider("Min Temp (°C)", "MinTemp", "min_temp")
            max_temp = slider("Max Temp (°C)", "MaxTemp", "max_temp")
            temp_9am = slider("Temp at 9am (°C)", "Temp9am", "temp_9am")
            temp_3pm = slider("Temp at 3pm (°C)", "Temp3pm", "temp_3pm")

        with st.expander("💧 Humidity & Pressure"):
            humidity_9am = slider("Humidity at 9am (%)", "Humidity9am", "hum_9am")
            humidity_3pm = slider("Humidity at 3pm (%)", "Humidity3pm", "hum_3pm")
            pressure_9am = slider("Pressure at 9am (hPa)", "Pressure9am", "pres_9am")
            pressure_3pm = slider("Pressure at 3pm (hPa)", "Pressure3pm", "pres_3pm")

        with st.expander("🌬️ Wind"):
            wind_gust_dir = st.selectbox("Wind gust direction", WIND_DIRS, index=WIND_DIRS.index("W") if "W" in WIND_DIRS else 0)
            wind_gust_speed = slider("Wind gust speed (km/h)", "WindGustSpeed", "gust_speed")
            wind_dir_9am = st.selectbox("Wind direction 9am", WIND_DIRS, index=WIND_DIRS.index("N") if "N" in WIND_DIRS else 0)
            wind_speed_9am = slider("Wind speed 9am (km/h)", "WindSpeed9am", "wind_9am")
            wind_dir_3pm = st.selectbox("Wind direction 3pm", WIND_DIRS, index=WIND_DIRS.index("SE") if "SE" in WIND_DIRS else 0)
            wind_speed_3pm = slider("Wind speed 3pm (km/h)", "WindSpeed3pm", "wind_3pm")

        with st.expander("☁️ Sky & Rain"):
            cloud_9am = st.slider("Cloud cover 9am (oktas)", 0, 9, 5, key="cloud_9am")
            cloud_3pm = st.slider("Cloud cover 3pm (oktas)", 0, 9, 5, key="cloud_3pm")
            sunshine = slider("Sunshine (hours)", "Sunshine", "sunshine")
            rainfall = slider("Rainfall today (mm)", "Rainfall", "rainfall")
            evaporation = slider("Evaporation (mm)", "Evaporation", "evaporation")

        submitted = st.form_submit_button("🔮 Predict rain tomorrow")


def sky_icon(cloud_avg, sunshine_val):
    if sunshine_val >= 9 and cloud_avg <= 3:
        return "☀️"
    if cloud_avg <= 4:
        return "🌤️"
    if cloud_avg <= 6:
        return "⛅"
    if cloud_avg <= 8:
        return "☁️"
    return "🌧️"


st.markdown(
    f'<div class="icon-banner">{sky_icon((cloud_9am + cloud_3pm) / 2, sunshine)}</div>',
    unsafe_allow_html=True,
)
st.caption("<div style='text-align:center;'>Live sky preview based on today's cloud cover & sunshine</div>", unsafe_allow_html=True)

if submitted:
    row = {
        "Location": location,
        "MinTemp": min_temp,
        "MaxTemp": max_temp,
        "Rainfall": rainfall,
        "Evaporation": evaporation,
        "Sunshine": sunshine,
        "WindGustDir": wind_gust_dir,
        "WindGustSpeed": wind_gust_speed,
        "WindDir9am": wind_dir_9am,
        "WindDir3pm": wind_dir_3pm,
        "WindSpeed9am": wind_speed_9am,
        "WindSpeed3pm": wind_speed_3pm,
        "Humidity9am": humidity_9am,
        "Humidity3pm": humidity_3pm,
        "Pressure9am": pressure_9am,
        "Pressure3pm": pressure_3pm,
        "Cloud9am": cloud_9am,
        "Cloud3pm": cloud_3pm,
        "Temp9am": temp_9am,
        "Temp3pm": temp_3pm,
        "RainToday": rain_today,
        "Year": obs_date.year,
        "Month": obs_date.month,
        "Day": obs_date.day,
    }
    row["TempDifference"] = row["MaxTemp"] - row["MinTemp"]
    row["HumidityDifference"] = row["Humidity3pm"] - row["Humidity9am"]
    row["PressureDifference"] = row["Pressure3pm"] - row["Pressure9am"]
    row["WindSpeedDifference"] = row["WindSpeed3pm"] - row["WindSpeed9am"]

    input_df = pd.DataFrame([row])
    for col, (lo, hi) in CLIP_BOUNDS.items():
        if col in input_df.columns:
            input_df[col] = input_df[col].clip(lo, hi)

    proba = MODEL.predict_proba(input_df)[0]
    classes = list(MODEL.classes_)
    rain_proba = float(proba[classes.index("Yes")]) * 100

    if rain_proba < 20:
        tier, label, icon = 0, "Very unlikely to rain", "☀️"
    elif rain_proba < 40:
        tier, label, icon = 1, "Unlikely to rain", "🌤️"
    elif rain_proba < 60:
        tier, label, icon = 2, "Chance of rain", "⛅"
    elif rain_proba < 80:
        tier, label, icon = 3, "Rain likely", "🌧️"
    else:
        tier, label, icon = 4, "Rain very likely", "⛈️"

    col_gauge, col_result = st.columns([1, 1])

    with col_gauge:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=rain_proba,
            number={"suffix": "%", "font": {"color": "white", "size": 40}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "white", "tickfont": {"color": "white"}},
                "bar": {"color": "#36d1dc"},
                "bgcolor": "rgba(255,255,255,0.05)",
                "steps": [
                    {"range": [0, 20], "color": "#ffd200"},
                    {"range": [20, 40], "color": "#a8e063"},
                    {"range": [40, 60], "color": "#7f8c9a"},
                    {"range": [60, 80], "color": "#3a6186"},
                    {"range": [80, 100], "color": "#0f2027"},
                ],
                "threshold": {"line": {"color": "white", "width": 3}, "value": rain_proba},
            },
        ))
        fig.update_layout(
            height=280,
            margin=dict(t=20, b=10, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            font={"color": "white"},
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_result:
        st.markdown(
            f"""
            <div class="result-card tier-{tier}">
                <h2>{icon} {label}</h2>
                <p>Estimated probability of rain tomorrow: <b>{rain_proba:.1f}%</b></p>
                <p>Location: <b>{location}</b> · Date: <b>{obs_date}</b></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="summary-card">
            <h4>📋 Input summary</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Max / Min Temp", f"{max_temp:.1f}° / {min_temp:.1f}°")
    s2.metric("Humidity 9am / 3pm", f"{humidity_9am:.0f}% / {humidity_3pm:.0f}%")
    s3.metric("Wind gust", f"{wind_gust_speed:.0f} km/h ({wind_gust_dir})")
    s4.metric("Cloud 9am / 3pm", f"{cloud_9am} / {cloud_3pm}")
