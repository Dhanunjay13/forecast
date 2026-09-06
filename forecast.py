import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
from datetime import timedelta

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PJM Energy Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# PROFESSIONAL THEME
# ============================================================

st.markdown(
    """
    <style>
    /* Main application background */
    .stApp {
        background:
            linear-gradient(
                rgba(5, 15, 30, 0.93),
                rgba(8, 22, 42, 0.96)
            ),
            url("https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&w=2400&q=85");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Main content width and spacing */
    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                rgba(5, 18, 38, 0.98),
                rgba(7, 28, 55, 0.98)
            );
        border-right: 1px solid rgba(130, 190, 255, 0.16);
    }

    section[data-testid="stSidebar"] * {
        color: #eaf4ff !important;
    }

    /* Main title */
    h1 {
        color: #f4f9ff !important;
        font-size: 2.35rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.8px;
        margin-bottom: 0.25rem !important;
    }

    h2 {
        color: #eaf4ff !important;
        font-weight: 750 !important;
        margin-top: 1.5rem !important;
    }

    h3 {
        color: #dcecff !important;
        font-weight: 700 !important;
    }

    /* Intro text */
    .intro-text {
        color: #9eb9d6;
        font-size: 1.02rem;
        margin-bottom: 1.4rem;
    }

    /* Native metric cards */
    div[data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                rgba(15, 43, 77, 0.95),
                rgba(8, 26, 50, 0.95)
            );
        border: 1px solid rgba(112, 190, 255, 0.18);
        border-radius: 16px;
        padding: 18px 18px 16px 18px;
        box-shadow: 0 14px 30px rgba(0, 0, 0, 0.20);
        min-height: 120px;
    }

    div[data-testid="stMetric"] label {
        color: #89a9c9 !important;
        font-size: 0.78rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
    }

    div[data-testid="stMetricValue"] {
        color: #f6fbff !important;
        font-size: 1.75rem !important;
        font-weight: 800 !important;
    }

    div[data-testid="stMetricDelta"] {
        color: #79d9ff !important;
    }

    /* Buttons */
    .stButton > button,
    .stDownloadButton > button {
        border-radius: 11px;
        min-height: 46px;
        font-weight: 750;
        border: 1px solid rgba(107, 199, 255, 0.25);
        color: white;
        background: linear-gradient(90deg, #008fd5, #005bc4);
        box-shadow: 0 8px 22px rgba(0, 120, 210, 0.24);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 12px 28px rgba(0, 120, 210, 0.34);
    }

    /* Sidebar slider */
    div[data-baseweb="slider"] {
        margin-bottom: 0.75rem;
    }

    /* Selectbox / input style */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        border-radius: 10px;
        background: rgba(12, 37, 67, 0.78);
        border-color: rgba(115, 185, 240, 0.18);
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(11, 35, 63, 0.82);
        border-radius: 12px;
        color: #eaf4ff !important;
        font-weight: 700;
    }

    /* Dataframe */
    div[data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid rgba(110, 185, 245, 0.14);
    }

    /* Charts */
    div[data-testid="stVegaLiteChart"],
    div[data-testid="stArrowVegaLiteChart"],
    div[data-testid="stPlotlyChart"] {
        background: rgba(7, 24, 45, 0.72);
        border-radius: 14px;
        border: 1px solid rgba(110, 185, 245, 0.12);
        padding: 8px;
    }

    /* Status / info boxes */
    div[data-testid="stAlert"] {
        border-radius: 12px;
    }

    /* Footer */
    .footer-text {
        color: #6987a7;
        text-align: center;
        font-size: 0.78rem;
        padding: 1.8rem 0 0.5rem 0;
    }

    /* Mobile spacing */
    @media (max-width: 900px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        h1 {
            font-size: 1.9rem !important;
        }

        div[data-testid="stMetric"] {
            min-height: 105px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():
    model_path = BASE_DIR / "xgb_model.pkl"

    if not model_path.exists():
        raise FileNotFoundError("xgb_model.pkl was not found.")

    return joblib.load(model_path)


# ============================================================
# LOAD METADATA
# ============================================================

@st.cache_resource
def load_metadata():
    feature_path = BASE_DIR / "feature_columns.pkl"
    holiday_path = BASE_DIR / "holiday_dates.pkl"

    if not feature_path.exists():
        raise FileNotFoundError("feature_columns.pkl was not found.")

    if not holiday_path.exists():
        raise FileNotFoundError("holiday_dates.pkl was not found.")

    feature_columns = list(joblib.load(feature_path))
    holiday_dates = joblib.load(holiday_path)

    return feature_columns, holiday_dates


# ============================================================
# LOAD DATASET
# ============================================================

@st.cache_data
def load_data():
    data_path = BASE_DIR / "PJMW_MW_Hourly.xlsx"

    if not data_path.exists():
        raise FileNotFoundError("PJMW_MW_Hourly.xlsx was not found.")

    df = pd.read_excel(data_path)

    # Detect datetime column
    if "Datetime" not in df.columns:
        possible_date_columns = [
            col
            for col in df.columns
            if "date" in str(col).lower()
            or "time" in str(col).lower()
        ]

        if not possible_date_columns:
            raise ValueError("Datetime column was not found.")

        df = df.rename(
            columns={possible_date_columns[0]: "Datetime"}
        )

    # Detect target column
    if "PJMW_MW" not in df.columns:
        possible_target_columns = [
            col
            for col in df.columns
            if "pjmw" in str(col).lower()
            or "mw" in str(col).lower()
        ]

        if not possible_target_columns:
            raise ValueError("PJMW_MW column was not found.")

        df = df.rename(
            columns={possible_target_columns[0]: "PJMW_MW"}
        )

    df["Datetime"] = pd.to_datetime(
        df["Datetime"],
        errors="coerce"
    )

    df["PJMW_MW"] = pd.to_numeric(
        df["PJMW_MW"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["Datetime", "PJMW_MW"]
    )

    df = (
        df.sort_values("Datetime")
        .reset_index(drop=True)
    )

    return df


# ============================================================
# FEATURE ENGINEERING
# ============================================================

def create_features(history, holiday_dates):
    current_time = (
        history["Datetime"].iloc[-1]
        + timedelta(hours=1)
    )

    features = {
        "Hour": current_time.hour,
        "Day": current_time.day,
        "DayOfWeek": current_time.dayofweek,
        "Month": current_time.month,
        "Year": current_time.year,
        "IsWeekend": int(current_time.dayofweek in [5, 6]),
        "IsHoliday": int(current_time.date() in holiday_dates),

        "lag_1": history["PJMW_MW"].iloc[-1],
        "lag_2": history["PJMW_MW"].iloc[-2],
        "lag_3": history["PJMW_MW"].iloc[-3],
        "lag_24": history["PJMW_MW"].iloc[-24],
        "lag_48": history["PJMW_MW"].iloc[-48],
        "lag_168": history["PJMW_MW"].iloc[-168],

        "rolling_mean_24": (
            history["PJMW_MW"].iloc[-24:].mean()
        ),

        "rolling_mean_168": (
            history["PJMW_MW"].iloc[-168:].mean()
        ),

        "rolling_std_24": (
            history["PJMW_MW"].iloc[-24:].std()
        ),
    }

    return pd.DataFrame([features]), current_time


# ============================================================
# FORECAST GENERATION
# ============================================================

def generate_forecast(
    historical_df,
    days,
    model,
    feature_columns,
    holiday_dates,
):
    if len(historical_df) < 168:
        raise ValueError(
            "At least 168 hourly observations are required."
        )

    history = historical_df[
        ["Datetime", "PJMW_MW"]
    ].copy()

    predictions = []

    for _ in range(days * 24):
        x_future, timestamp = create_features(
            history,
            holiday_dates,
        )

        missing_columns = [
            col
            for col in feature_columns
            if col not in x_future.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing model features: {missing_columns}"
            )

        prediction = float(
            model.predict(
                x_future[feature_columns]
            )[0]
        )

        prediction = max(0.0, prediction)

        predictions.append(
            {
                "Datetime": timestamp,
                "Forecast_MW": prediction,
            }
        )

        next_row = pd.DataFrame(
            {
                "Datetime": [timestamp],
                "PJMW_MW": [prediction],
            }
        )

        history = pd.concat(
            [history, next_row],
            ignore_index=True,
        )

    return pd.DataFrame(predictions)


# ============================================================
# LOAD REQUIRED FILES
# ============================================================

try:
    model = load_model()
    feature_columns, holiday_dates = load_metadata()
    df = load_data()

except Exception as error:
    st.error(f"Application setup failed: {error}")
    st.info(
        "Place forecast.py, xgb_model.pkl, feature_columns.pkl, "
        "holiday_dates.pkl and PJMW_MW_Hourly.xlsx in the same folder."
    )
    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚡ Energy AI")
st.sidebar.caption("PJM Demand Forecasting System")

st.sidebar.divider()

st.sidebar.subheader("Forecast Settings")

forecast_days = st.sidebar.slider(
    "Forecast Horizon (Days)",
    min_value=1,
    max_value=30,
    value=30,
    step=1,
)

st.sidebar.write(
    f"**Hourly predictions:** {forecast_days * 24}"
)

st.sidebar.divider()

st.sidebar.subheader("Model")

st.sidebar.write("**XGBoost Regressor**")
st.sidebar.write("**Frequency:** Hourly")
st.sidebar.write("**Target:** PJMW_MW")
st.sidebar.write("**Maximum horizon:** 30 days")


# ============================================================
# HEADER
# ============================================================

st.title("⚡ PJM Energy Intelligence")

st.markdown(
    '<p class="intro-text">'
    "Machine learning powered electricity demand forecasting "
    "using an XGBoost regression model."
    "</p>",
    unsafe_allow_html=True,
)


# ============================================================
# OVERVIEW METRICS
# ============================================================

st.header("Historical Overview")

latest_value = df["PJMW_MW"].iloc[-1]
average_value = df["PJMW_MW"].mean()
peak_value = df["PJMW_MW"].max()
latest_timestamp = df["Datetime"].iloc[-1]

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "Current Demand",
    f"{latest_value:,.0f} MW",
)

m2.metric(
    "Historical Average",
    f"{average_value:,.0f} MW",
)

m3.metric(
    "Peak Demand",
    f"{peak_value:,.0f} MW",
)

m4.metric(
    "Last Observation",
    latest_timestamp.strftime("%d %b %Y %H:%M"),
)


# ============================================================
# HISTORICAL CHART
# ============================================================

st.subheader("Historical Demand — Last 7 Days")

historical_chart = (
    df.tail(24 * 7)
    .set_index("Datetime")[["PJMW_MW"]]
)

st.line_chart(
    historical_chart,
    height=380,
)


# ============================================================
# FORECAST SECTION
# ============================================================

st.header("Future Energy Forecast")

st.write(
    f"Generate {forecast_days * 24:,} hourly predictions "
    f"for the next {forecast_days} day(s)."
)

generate_forecast_button = st.button(
    "⚡ Generate Forecast",
    type="primary",
    use_container_width=True,
)

if generate_forecast_button:
    with st.spinner(
        f"Generating {forecast_days}-day hourly forecast..."
    ):
        try:
            forecast_df = generate_forecast(
                df,
                forecast_days,
                model,
                feature_columns,
                holiday_dates,
            )

            st.session_state["forecast_df"] = forecast_df

        except Exception as error:
            st.error(
                f"Forecast generation failed: {error}"
            )


# ============================================================
# FORECAST RESULTS
# ============================================================

if "forecast_df" in st.session_state:
    forecast_df = st.session_state["forecast_df"]

    st.subheader("Forecast Summary")

    average_forecast = (
        forecast_df["Forecast_MW"].mean()
    )

    maximum_forecast = (
        forecast_df["Forecast_MW"].max()
    )

    minimum_forecast = (
        forecast_df["Forecast_MW"].min()
    )

    peak_row = forecast_df.loc[
        forecast_df["Forecast_MW"].idxmax()
    ]

    peak_time = peak_row["Datetime"]

    f1, f2, f3, f4 = st.columns(4)

    f1.metric(
        "Average Forecast",
        f"{average_forecast:,.0f} MW",
    )

    f2.metric(
        "Forecast Peak",
        f"{maximum_forecast:,.0f} MW",
    )

    f3.metric(
        "Forecast Minimum",
        f"{minimum_forecast:,.0f} MW",
    )

    f4.metric(
        "Expected Peak Time",
        peak_time.strftime("%d %b %H:%M"),
    )

    st.subheader("Forecasted Demand")

    forecast_chart = (
        forecast_df
        .set_index("Datetime")[["Forecast_MW"]]
    )

    st.line_chart(
        forecast_chart,
        height=400,
    )

    st.subheader("Hourly Forecast Data")

    display_df = forecast_df.copy()

    display_df["Datetime"] = (
        display_df["Datetime"]
        .dt.strftime("%d-%b-%Y %H:%M")
    )

    display_df["Forecast_MW"] = (
        display_df["Forecast_MW"].round(2)
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        height=430,
    )

    csv_data = forecast_df.to_csv(
        index=False
    )

    st.download_button(
        label="⬇️ Download Forecast CSV",
        data=csv_data,
        file_name=(
            f"pjm_{forecast_days}_day_forecast.csv"
        ),
        mime="text/csv",
        use_container_width=True,
    )


# ============================================================
# PROJECT INFORMATION
# ============================================================

st.header("Project Information")

with st.expander(
    "Model Information",
    expanded=True,
):
    st.write("**Model:** XGBoost Regressor")
    st.write(
        "**Features:** Hour, Day, DayOfWeek, Month, Year, "
        "IsWeekend, IsHoliday, lag variables and rolling statistics."
    )
    st.write(
        "**Forecast Method:** Recursive multi-step forecasting. "
        "Each predicted value is added to the historical sequence "
        "and used to create the next prediction."
    )

with st.expander(
    "Dataset Information",
    expanded=True,
):
    d1, d2, d3 = st.columns(3)

    d1.metric(
        "Observations",
        f"{len(df):,}",
    )

    d2.metric(
        "Data Start",
        df["Datetime"].min().strftime("%Y"),
    )

    d3.metric(
        "Data End",
        df["Datetime"].max().strftime("%Y"),
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<p class="footer-text">'
    "PJM Hourly Energy Consumption Forecasting • "
    "XGBoost Regression • Streamlit"
    "</p>",
    unsafe_allow_html=True,
)
