```python
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


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# PROFESSIONAL DARK ENERGY THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL APPLICATION BACKGROUND
       ======================================================== */

    .stApp {
        background:
            linear-gradient(
                rgba(3, 12, 25, 0.72),
                rgba(3, 15, 32, 0.82)
            ),
            url("https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&w=2400&q=90");

        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }


    /* Additional subtle dark overlay */

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;

        background:
            radial-gradient(
                circle at 85% 15%,
                rgba(0, 153, 255, 0.10),
                transparent 35%
            ),
            radial-gradient(
                circle at 10% 85%,
                rgba(0, 95, 175, 0.12),
                transparent 40%
            );

        pointer-events: none;
        z-index: 0;
    }


    /* ========================================================
       MAIN CONTENT
       ======================================================== */

    .main {
        position: relative;
        z-index: 1;
    }

    .block-container {
        max-width: 1450px;

        padding-top: 2rem;
        padding-bottom: 3rem;

        padding-left: 2.5rem;
        padding-right: 2.5rem;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                rgba(3, 16, 34, 0.98),
                rgba(5, 27, 52, 0.98)
            );

        border-right:
            1px solid rgba(80, 180, 255, 0.20);

        box-shadow:
            8px 0 30px rgba(0, 0, 0, 0.35);
    }


    section[data-testid="stSidebar"] * {
        color: #edf7ff !important;
    }


    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {

        color: #ffffff !important;

        font-weight: 800 !important;
    }


    section[data-testid="stSidebar"] p {

        color: #b9d0e7 !important;

        line-height: 1.6;
    }


    section[data-testid="stSidebar"] strong {

        color: #ffffff !important;

        font-weight: 800 !important;
    }


    /* ========================================================
       SIDEBAR EXPANDERS
       ======================================================== */

    section[data-testid="stSidebar"]
    .streamlit-expanderHeader {

        background:
            linear-gradient(
                135deg,
                rgba(11, 39, 70, 0.96),
                rgba(7, 27, 51, 0.96)
            );

        border:
            1px solid rgba(105, 187, 245, 0.20);

        border-radius: 12px;

        color: #f2f8ff !important;

        font-weight: 750;

        padding: 0.75rem 0.9rem;
    }


    section[data-testid="stSidebar"]
    .streamlit-expanderContent {

        background:
            rgba(5, 22, 42, 0.96);

        border:
            1px solid rgba(100, 180, 240, 0.12);

        border-top: none;

        border-radius:
            0 0 12px 12px;

        color: #d8e9f8 !important;
    }


    /* ========================================================
       MAIN TITLE
       ======================================================== */

    h1 {

        color: #ffffff !important;

        font-size: 2.65rem !important;

        font-weight: 850 !important;

        letter-spacing: -1px;

        line-height: 1.15;

        margin-bottom: 0.35rem !important;

        text-shadow:
            0 3px 16px rgba(0, 0, 0, 0.65);
    }


    /* ========================================================
       SECTION HEADERS
       ======================================================== */

    h2 {

        color: #f5faff !important;

        font-size: 1.65rem !important;

        font-weight: 800 !important;

        letter-spacing: -0.3px;

        margin-top: 1.8rem !important;

        margin-bottom: 0.8rem !important;

        text-shadow:
            0 2px 12px rgba(0, 0, 0, 0.60);
    }


    h3 {

        color: #e3f4ff !important;

        font-size: 1.25rem !important;

        font-weight: 750 !important;

        margin-top: 1.2rem !important;

        margin-bottom: 0.65rem !important;

        text-shadow:
            0 2px 8px rgba(0, 0, 0, 0.55);
    }


    /* ========================================================
       NORMAL TEXT
       ======================================================== */

    p,
    li {

        color: #d7e8f8;

        line-height: 1.6;
    }


    .intro-text {

        color: #aec8e2;

        font-size: 1.05rem;

        line-height: 1.7;

        font-weight: 450;

        margin-bottom: 1.6rem;

        text-shadow:
            0 2px 8px rgba(0, 0, 0, 0.55);
    }


    /* ========================================================
       METRIC CARDS
       ======================================================== */

    div[data-testid="stMetric"] {

        background:
            linear-gradient(
                145deg,
                rgba(13, 46, 82, 0.95),
                rgba(5, 25, 50, 0.97)
            );

        border:
            1px solid rgba(101, 193, 255, 0.28);

        border-radius: 18px;

        padding: 20px 20px 18px 20px;

        min-height: 125px;

        box-shadow:
            0 14px 35px rgba(0, 0, 0, 0.30),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }


    div[data-testid="stMetric"]:hover {

        transform: translateY(-3px);

        box-shadow:
            0 18px 40px rgba(0, 0, 0, 0.42),
            0 0 20px rgba(0, 153, 255, 0.12);
    }


    div[data-testid="stMetric"] label {

        color: #91b5d7 !important;

        font-size: 0.76rem !important;

        font-weight: 750 !important;

        letter-spacing: 0.8px;

        text-transform: uppercase;
    }


    div[data-testid="stMetricValue"] {

        color: #ffffff !important;

        font-size: 1.85rem !important;

        font-weight: 850 !important;

        letter-spacing: -0.5px;

        text-shadow:
            0 2px 10px rgba(0, 0, 0, 0.40);
    }


    div[data-testid="stMetricDelta"] {

        color: #72d9ff !important;

        font-weight: 700 !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button,
    .stDownloadButton > button {

        min-height: 48px;

        border-radius: 12px;

        font-size: 0.95rem;

        font-weight: 800;

        letter-spacing: 0.2px;

        color: #ffffff !important;

        background:
            linear-gradient(
                90deg,
                #0098dc,
                #0065d1
            );

        border:
            1px solid rgba(130, 220, 255, 0.35);

        box-shadow:
            0 8px 25px rgba(0, 110, 200, 0.30);

        transition:
            all 0.2s ease;
    }


    .stButton > button:hover,
    .stDownloadButton > button:hover {

        transform: translateY(-2px);

        background:
            linear-gradient(
                90deg,
                #00a8ee,
                #0074e8
            );

        box-shadow:
            0 12px 30px rgba(0, 130, 230, 0.40);
    }


    /* ========================================================
       SIDEBAR SLIDER
       ======================================================== */

    div[data-baseweb="slider"] {

        margin-bottom: 1rem;
    }


    section[data-testid="stSidebar"]
    [data-testid="stWidgetLabel"] {

        color: #cfe5fa !important;

        font-weight: 700 !important;
    }


    /* ========================================================
       SELECTBOX / INPUTS
       ======================================================== */

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {

        background:
            rgba(10, 36, 65, 0.92) !important;

        border:
            1px solid rgba(110, 190, 245, 0.25) !important;

        border-radius: 11px;

        color: #ffffff !important;
    }


    input {

        color: #ffffff !important;
    }


    /* ========================================================
       EXPANDERS
       ======================================================== */

    .streamlit-expanderHeader {

        background:
            linear-gradient(
                135deg,
                rgba(11, 39, 70, 0.96),
                rgba(7, 27, 51, 0.96)
            );

        border:
            1px solid rgba(105, 187, 245, 0.20);

        border-radius: 12px;

        color: #f2f8ff !important;

        font-weight: 750;

        padding: 0.8rem 1rem;
    }


    .streamlit-expanderContent {

        background:
            rgba(5, 22, 42, 0.92);

        border:
            1px solid rgba(100, 180, 240, 0.12);

        border-top: none;

        border-radius:
            0 0 12px 12px;

        color: #d8e9f8 !important;
    }


    /* ========================================================
       DATAFRAME
       ======================================================== */

    div[data-testid="stDataFrame"] {

        border-radius: 15px;

        overflow: hidden;

        border:
            1px solid rgba(110, 190, 245, 0.20);

        box-shadow:
            0 12px 30px rgba(0, 0, 0, 0.28);

        background:
            rgba(5, 22, 42, 0.90);
    }


    /* ========================================================
       CHART CONTAINERS
       ======================================================== */

    div[data-testid="stVegaLiteChart"],
    div[data-testid="stArrowVegaLiteChart"],
    div[data-testid="stPlotlyChart"] {

        background:
            linear-gradient(
                145deg,
                rgba(6, 28, 52, 0.92),
                rgba(5, 21, 41, 0.95)
            );

        border:
            1px solid rgba(99, 183, 242, 0.18);

        border-radius: 16px;

        padding: 12px;

        box-shadow:
            0 12px 28px rgba(0, 0, 0, 0.24);
    }


    /* ========================================================
       ALERT / INFO BOXES
       ======================================================== */

    div[data-testid="stAlert"] {

        border-radius: 12px;

        background:
            rgba(8, 31, 57, 0.94);

        border:
            1px solid rgba(106, 190, 245, 0.18);
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {

        border: none;

        height: 1px;

        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(115, 190, 245, 0.35),
                transparent
            );

        margin: 1.4rem 0;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer-text {

        color: #7595b5;

        text-align: center;

        font-size: 0.78rem;

        padding: 2rem 0 0.5rem 0;

        letter-spacing: 0.3px;
    }


    /* ========================================================
       RESPONSIVE DESIGN
       ======================================================== */

    @media (max-width: 900px) {

        .block-container {

            padding-left: 1rem;
            padding-right: 1rem;
        }


        h1 {

            font-size: 2rem !important;
        }


        h2 {

            font-size: 1.45rem !important;
        }


        div[data-testid="stMetric"] {

            min-height: 105px;
            padding: 15px;
        }


        div[data-testid="stMetricValue"] {

            font-size: 1.45rem !important;
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

        raise FileNotFoundError(
            "xgb_model.pkl was not found."
        )

    return joblib.load(model_path)


# ============================================================
# LOAD METADATA
# ============================================================

@st.cache_resource
def load_metadata():

    feature_path = BASE_DIR / "feature_columns.pkl"

    holiday_path = BASE_DIR / "holiday_dates.pkl"


    if not feature_path.exists():

        raise FileNotFoundError(
            "feature_columns.pkl was not found."
        )


    if not holiday_path.exists():

        raise FileNotFoundError(
            "holiday_dates.pkl was not found."
        )


    feature_columns = list(
        joblib.load(feature_path)
    )

    holiday_dates = joblib.load(
        holiday_path
    )


    # Convert holiday values into date objects

    cleaned_holidays = set()


    for date_value in holiday_dates:

        try:

            cleaned_holidays.add(
                pd.Timestamp(date_value).date()
            )

        except Exception:

            pass


    return feature_columns, cleaned_holidays


# ============================================================
# LOAD DATASET
# ============================================================

@st.cache_data
def load_data():

    data_path = BASE_DIR / "PJMW_MW_Hourly.xlsx"


    if not data_path.exists():

        raise FileNotFoundError(
            "PJMW_MW_Hourly.xlsx was not found."
        )


    df = pd.read_excel(
        data_path
    )


    # --------------------------------------------------------
    # Detect Datetime column
    # --------------------------------------------------------

    if "Datetime" not in df.columns:

        possible_date_columns = [

            col

            for col in df.columns

            if "date" in str(col).lower()
            or "time" in str(col).lower()

        ]


        if not possible_date_columns:

            raise ValueError(
                "Datetime column was not found."
            )


        df = df.rename(
            columns={
                possible_date_columns[0]:
                    "Datetime"
            }
        )


    # --------------------------------------------------------
    # Detect target column
    # --------------------------------------------------------

    if "PJMW_MW" not in df.columns:

        possible_target_columns = [

            col

            for col in df.columns

            if "pjmw" in str(col).lower()
            or "mw" in str(col).lower()

        ]


        if not possible_target_columns:

            raise ValueError(
                "PJMW_MW column was not found."
            )


        df = df.rename(
            columns={
                possible_target_columns[0]:
                    "PJMW_MW"
            }
        )


    # --------------------------------------------------------
    # Convert Datetime
    # --------------------------------------------------------

    df["Datetime"] = pd.to_datetime(
        df["Datetime"],
        errors="coerce"
    )


    # --------------------------------------------------------
    # Convert target
    # --------------------------------------------------------

    df["PJMW_MW"] = pd.to_numeric(
        df["PJMW_MW"],
        errors="coerce"
    )


    # --------------------------------------------------------
    # Remove invalid rows
    # --------------------------------------------------------

    df = df.dropna(
        subset=[
            "Datetime",
            "PJMW_MW"
        ]
    )


    # --------------------------------------------------------
    # Sort data
    # --------------------------------------------------------

    df = (
        df
        .sort_values("Datetime")
        .reset_index(drop=True)
    )


    return df


# ============================================================
# FEATURE ENGINEERING
# ============================================================

def create_features(
    history,
    holiday_dates
):

    current_time = (
        history["Datetime"].iloc[-1]
        + timedelta(hours=1)
    )


    features = {

        "Hour":
            current_time.hour,

        "Day":
            current_time.day,

        "DayOfWeek":
            current_time.dayofweek,

        "Month":
            current_time.month,

        "Year":
            current_time.year,

        "IsWeekend":
            int(
                current_time.dayofweek
                in [5, 6]
            ),

        "IsHoliday":
            int(
                current_time.date()
                in holiday_dates
            ),


        # ----------------------------------------------------
        # Lag features
        # ----------------------------------------------------

        "lag_1":
            history["PJMW_MW"].iloc[-1],

        "lag_2":
            history["PJMW_MW"].iloc[-2],

        "lag_3":
            history["PJMW_MW"].iloc[-3],

        "lag_24":
            history["PJMW_MW"].iloc[-24],

        "lag_48":
            history["PJMW_MW"].iloc[-48],

        "lag_168":
            history["PJMW_MW"].iloc[-168],


        # ----------------------------------------------------
        # Rolling statistics
        # ----------------------------------------------------

        "rolling_mean_24":
            history["PJMW_MW"]
            .iloc[-24:]
            .mean(),

        "rolling_mean_168":
            history["PJMW_MW"]
            .iloc[-168:]
            .mean(),

        "rolling_std_24":
            history["PJMW_MW"]
            .iloc[-24:]
            .std(),
    }


    return (
        pd.DataFrame([features]),
        current_time
    )


# ============================================================
# FORECAST GENERATION
# ============================================================

def generate_forecast(
    historical_df,
    days,
    model,
    feature_columns,
    holiday_dates
):

    if len(historical_df) < 168:

        raise ValueError(
            "At least 168 hourly observations "
            "are required for forecasting."
        )


    history = historical_df[
        ["Datetime", "PJMW_MW"]
    ].copy()


    predictions = []


    # --------------------------------------------------------
    # Generate hourly predictions
    # --------------------------------------------------------

    for _ in range(days * 24):

        x_future, timestamp = create_features(
            history,
            holiday_dates
        )


        # ----------------------------------------------------
        # Check required features
        # ----------------------------------------------------

        missing_columns = [

            col

            for col in feature_columns

            if col not in x_future.columns

        ]


        if missing_columns:

            raise ValueError(
                f"Missing model features: "
                f"{missing_columns}"
            )


        # ----------------------------------------------------
        # Model prediction
        # ----------------------------------------------------

        prediction = float(
            model.predict(
                x_future[
                    feature_columns
                ]
            )[0]
        )


        # Demand cannot be negative

        prediction = max(
            0.0,
            prediction
        )


        # ----------------------------------------------------
        # Save prediction
        # ----------------------------------------------------

        predictions.append(

            {
                "Datetime":
                    timestamp,

                "Forecast_MW":
                    prediction
            }

        )


        # ----------------------------------------------------
        # Recursive forecasting
        # ----------------------------------------------------

        next_row = pd.DataFrame(

            {
                "Datetime":
                    [timestamp],

                "PJMW_MW":
                    [prediction]
            }

        )


        history = pd.concat(

            [
                history,
                next_row
            ],

            ignore_index=True

        )


    return pd.DataFrame(
        predictions
    )


# ============================================================
# LOAD REQUIRED FILES
# ============================================================

try:

    model = load_model()

    feature_columns, holiday_dates = (
        load_metadata()
    )

    df = load_data()


except Exception as error:

    st.error(
        f"Application setup failed: {error}"
    )

    st.info(
        "Place forecast.py, xgb_model.pkl, "
        "feature_columns.pkl, holiday_dates.pkl "
        "and PJMW_MW_Hourly.xlsx in the same folder."
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚡ Energy AI")

st.sidebar.caption(
    "PJM Demand Forecasting System"
)

st.sidebar.divider()


# ============================================================
# FORECAST SETTINGS
# ============================================================

st.sidebar.subheader(
    "Forecast Settings"
)


forecast_days = st.sidebar.slider(

    "Forecast Horizon (Days)",

    min_value=1,

    max_value=30,

    value=30,

    step=1
)


st.sidebar.write(
    f"**Hourly predictions:** "
    f"{forecast_days * 24:,}"
)


st.sidebar.divider()


# ============================================================
# MODEL INFORMATION
# ============================================================

with st.sidebar.expander(
    "🤖 Model Information",
    expanded=False
):

    st.write(
        "**Model:** XGBoost Regressor"
    )

    st.write(
        "**Target Variable:** PJMW_MW"
    )

    st.write(
        "**Forecast Frequency:** Hourly"
    )

    st.write(
        "**Forecast Type:** "
        "Recursive Multi-Step Forecasting"
    )

    st.write(
        "**Maximum Forecast Horizon:** "
        "30 Days"
    )

    st.write(
        "**Features:** Hour, Day, DayOfWeek, "
        "Month, Year, IsWeekend, IsHoliday, "
        "lag variables and rolling statistics."
    )

    st.write(
        "**Forecast Method:** Each predicted "
        "value is added back to the historical "
        "sequence and used to generate the next "
        "prediction."
    )


# ============================================================
# DATASET INFORMATION
# ============================================================

with st.sidebar.expander(
    "📊 Dataset Information",
    expanded=False
):

    st.metric(
        "Observations",
        f"{len(df):,}"
    )

    st.metric(
        "Data Start",
        df[
            "Datetime"
        ].min().strftime(
            "%d %b %Y"
        )
    )

    st.metric(
        "Data End",
        df[
            "Datetime"
        ].max().strftime(
            "%d %b %Y"
        )
    )

    st.metric(
        "Features",
        f"{len(feature_columns)}"
    )


# ============================================================
# MODEL DETAILS
# ============================================================

with st.sidebar.expander(
    "⚙️ Model Details",
    expanded=False
):

    st.write(
        "**Algorithm:** XGBoost Regressor"
    )

    st.write(
        "**Frequency:** Hourly"
    )

    st.write(
        "**Target:** PJMW_MW"
    )

    st.write(
        "**Maximum Horizon:** 30 Days"
    )


# ============================================================
# DATA STATUS
# ============================================================

st.sidebar.divider()

st.sidebar.subheader(
    "Data Status"
)


st.sidebar.success(
    "Dataset loaded successfully"
)


st.sidebar.write(
    f"**Rows:** {len(df):,}"
)


# ============================================================
# HEADER
# ============================================================

st.title(
    "⚡ PJM Energy Intelligence"
)


st.markdown(

    """
    <p class="intro-text">
        Machine learning powered electricity demand forecasting
        using an XGBoost regression model.
    </p>
    """,

    unsafe_allow_html=True
)


# ============================================================
# HISTORICAL OVERVIEW
# ============================================================

st.header(
    "Historical Overview"
)


latest_value = (
    df["PJMW_MW"].iloc[-1]
)


average_value = (
    df["PJMW_MW"].mean()
)


peak_value = (
    df["PJMW_MW"].max()
)


minimum_value = (
    df["PJMW_MW"].min()
)


latest_timestamp = (
    df["Datetime"].iloc[-1]
)


# ============================================================
# METRICS
# ============================================================

m1, m2, m3, m4 = st.columns(4)


with m1:

    st.metric(
        "Current Demand",
        f"{latest_value:,.0f} MW"
    )


with m2:

    st.metric(
        "Historical Average",
        f"{average_value:,.0f} MW"
    )


with m3:

    st.metric(
        "Peak Demand",
        f"{peak_value:,.0f} MW"
    )


with m4:

    st.metric(
        "Last Observation",
        latest_timestamp.strftime(
            "%d %b %Y %H:%M"
        )
    )


# ============================================================
# HISTORICAL DEMAND CHART
# ============================================================

st.subheader(
    "Historical Demand — Last 7 Days"
)


historical_chart = (

    df.tail(24 * 7)

    .set_index("Datetime")

    [["PJMW_MW"]]

)


st.line_chart(

    historical_chart,

    height=380
)


# ============================================================
# FORECAST SECTION
# ============================================================

st.header(
    "Future Energy Forecast"
)


st.markdown(

    f"""
    <p class="intro-text">
        Generate <strong style="color:#ffffff;">
        {forecast_days * 24:,} hourly predictions
        </strong>
        for the next
        <strong style="color:#ffffff;">
        {forecast_days} day(s)
        </strong>.
    </p>
    """,

    unsafe_allow_html=True
)


generate_forecast_button = st.button(

    "⚡ Generate Forecast",

    type="primary",

    use_container_width=True
)


# ============================================================
# FORECAST GENERATION
# ============================================================

if generate_forecast_button:

    with st.spinner(

        f"Generating {forecast_days}-day "
        f"hourly forecast..."

    ):

        try:

            forecast_df = generate_forecast(

                df,

                forecast_days,

                model,

                feature_columns,

                holiday_dates

            )


            # Store forecast

            st.session_state[
                "forecast_df"
            ] = forecast_df


            st.success(
                "Forecast generated successfully."
            )


        except Exception as error:

            st.error(
                f"Forecast generation failed: "
                f"{error}"
            )


# ============================================================
# FORECAST RESULTS
# ============================================================

if "forecast_df" in st.session_state:

    forecast_df = (
        st.session_state[
            "forecast_df"
        ]
    )


    # ========================================================
    # FORECAST SUMMARY
    # ========================================================

    st.subheader(
        "Forecast Summary"
    )


    average_forecast = (

        forecast_df[
            "Forecast_MW"
        ].mean()

    )


    maximum_forecast = (

        forecast_df[
            "Forecast_MW"
        ].max()

    )


    minimum_forecast = (

        forecast_df[
            "Forecast_MW"
        ].min()

    )


    peak_row = (

        forecast_df.loc[

            forecast_df[
                "Forecast_MW"
            ].idxmax()

        ]

    )


    peak_time = (
        peak_row["Datetime"]
    )


    # ========================================================
    # FORECAST METRICS
    # ========================================================

    f1, f2, f3, f4 = st.columns(4)


    with f1:

        st.metric(

            "Average Forecast",

            f"{average_forecast:,.0f} MW"

        )


    with f2:

        st.metric(

            "Forecast Peak",

            f"{maximum_forecast:,.0f} MW"

        )


    with f3:

        st.metric(

            "Forecast Minimum",

            f"{minimum_forecast:,.0f} MW"

        )


    with f4:

        st.metric(

            "Expected Peak Time",

            peak_time.strftime(
                "%d %b %H:%M"
            )

        )


    # ========================================================
    # FORECAST CHART
    # ========================================================

    st.subheader(
        "Forecasted Demand"
    )


    forecast_chart = (

        forecast_df

        .set_index("Datetime")

        [["Forecast_MW"]]

    )


    st.line_chart(

        forecast_chart,

        height=420

    )


    # ========================================================
    # HOURLY FORECAST TABLE
    # ========================================================

    st.subheader(
        "Hourly Forecast Data"
    )


    display_df = (
        forecast_df.copy()
    )


    display_df["Datetime"] = (

        display_df[
            "Datetime"
        ]

        .dt.strftime(
            "%d-%b-%Y %H:%M"
        )

    )


    display_df["Forecast_MW"] = (

        display_df[
            "Forecast_MW"
        ]

        .round(2)

    )


    st.dataframe(

        display_df,

        use_container_width=True,

        height=430

    )


    # ========================================================
    # DOWNLOAD
    # ========================================================

    csv_data = (
        forecast_df.to_csv(
            index=False
        )
    )


    st.download_button(

        label="⬇️ Download Forecast CSV",

        data=csv_data,

        file_name=(
            f"pjm_{forecast_days}"
            f"_day_forecast.csv"
        ),

        mime="text/csv",

        use_container_width=True

    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(

    """
    <p class="footer-text">
        ⚡ PJM Hourly Energy Consumption Forecasting
        &nbsp;•&nbsp;
        XGBoost Regression
        &nbsp;•&nbsp;
        Streamlit
    </p>
    """,

    unsafe_allow_html=True
)
```
