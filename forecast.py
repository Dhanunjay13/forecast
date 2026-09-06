import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
from datetime import timedelta

# ============================================================
# PAGE SETUP
# ============================================================

st.set_page_config(
    page_title="PJM Energy Forecast",
    page_icon="⚡",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():
    path = BASE_DIR / "xgb_model.pkl"
    if not path.exists():
        raise FileNotFoundError("xgb_model.pkl not found.")
    return joblib.load(path)


# ============================================================
# LOAD FEATURE COLUMNS + HOLIDAYS
# ============================================================

@st.cache_resource
def load_metadata():
    feature_path = BASE_DIR / "feature_columns.pkl"
    holiday_path = BASE_DIR / "holiday_dates.pkl"

    if not feature_path.exists():
        raise FileNotFoundError("feature_columns.pkl not found.")

    if not holiday_path.exists():
        raise FileNotFoundError("holiday_dates.pkl not found.")

    feature_cols = list(joblib.load(feature_path))
    holiday_dates = joblib.load(holiday_path)

    return feature_cols, holiday_dates


# ============================================================
# LOAD DATASET
# ============================================================

@st.cache_data
def load_data():
    path = BASE_DIR / "PJMW_MW_Hourly.xlsx"

    if not path.exists():
        raise FileNotFoundError("PJMW_MW_Hourly.xlsx not found.")

    df = pd.read_excel(path)

    # Find datetime column if needed
    if "Datetime" not in df.columns:
        date_columns = [
            col for col in df.columns
            if "date" in str(col).lower()
            or "time" in str(col).lower()
        ]

        if not date_columns:
            raise ValueError("Datetime column not found.")

        df = df.rename(columns={date_columns[0]: "Datetime"})

    # Find target column if needed
    if "PJMW_MW" not in df.columns:
        target_columns = [
            col for col in df.columns
            if "pjmw" in str(col).lower()
            or "mw" in str(col).lower()
        ]

        if not target_columns:
            raise ValueError("PJMW_MW column not found.")

        df = df.rename(columns={target_columns[0]: "PJMW_MW"})

    df["Datetime"] = pd.to_datetime(df["Datetime"], errors="coerce")
    df["PJMW_MW"] = pd.to_numeric(df["PJMW_MW"], errors="coerce")

    df = df.dropna(subset=["Datetime", "PJMW_MW"])
    df = df.sort_values("Datetime").reset_index(drop=True)

    return df


# ============================================================
# FEATURE ENGINEERING
# ============================================================

def create_features(history, holiday_dates):
    current_time = history["Datetime"].iloc[-1] + timedelta(hours=1)

    row = {
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

        "rolling_mean_24": history["PJMW_MW"].iloc[-24:].mean(),
        "rolling_mean_168": history["PJMW_MW"].iloc[-168:].mean(),
        "rolling_std_24": history["PJMW_MW"].iloc[-24:].std(),
    }

    return pd.DataFrame([row]), current_time


# ============================================================
# FORECAST FUNCTION
# ============================================================

def generate_forecast(
    historical_df,
    number_of_days,
    model,
    feature_cols,
    holiday_dates
):
    if len(historical_df) < 168:
        raise ValueError(
            "At least 168 historical hourly observations are required."
        )

    history = historical_df[["Datetime", "PJMW_MW"]].copy()
    predictions = []

    for _ in range(number_of_days * 24):
        x_future, timestamp = create_features(
            history,
            holiday_dates
        )

        missing_columns = [
            col for col in feature_cols
            if col not in x_future.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing model features: {missing_columns}"
            )

        prediction = float(
            model.predict(x_future[feature_cols])[0]
        )

        # Demand cannot be negative
        prediction = max(0.0, prediction)

        predictions.append(
            {
                "Datetime": timestamp,
                "Forecast_MW": prediction
            }
        )

        next_row = pd.DataFrame(
            {
                "Datetime": [timestamp],
                "PJMW_MW": [prediction]
            }
        )

        history = pd.concat(
            [history, next_row],
            ignore_index=True
        )

    return pd.DataFrame(predictions)


# ============================================================
# LOAD REQUIRED FILES
# ============================================================

try:
    model = load_model()
    feature_cols, holiday_dates = load_metadata()
    df = load_data()
except Exception as error:
    st.error(f"Application setup failed: {error}")
    st.info(
        "Keep forecast.py, xgb_model.pkl, feature_columns.pkl, "
        "holiday_dates.pkl and PJMW_MW_Hourly.xlsx in the same folder."
    )
    st.stop()


# ============================================================
# TITLE
# ============================================================

st.title("⚡ PJM Energy Forecast")
st.write(
    "Hourly electricity demand forecasting using an XGBoost regression model."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("Forecast Settings")

forecast_days = st.sidebar.slider(
    "Forecast Horizon (Days)",
    min_value=1,
    max_value=30,
    value=30,
    step=1
)

st.sidebar.write(f"Hourly predictions: {forecast_days * 24}")
st.sidebar.write("Model: XGBoost Regressor")
st.sidebar.write("Frequency: Hourly")
st.sidebar.write("Target: PJMW_MW")


# ============================================================
# HISTORICAL SUMMARY
# ============================================================

st.header("Historical Data")

latest_value = df["PJMW_MW"].iloc[-1]
average_value = df["PJMW_MW"].mean()
peak_value = df["PJMW_MW"].max()
latest_timestamp = df["Datetime"].iloc[-1]

c1, c2, c3, c4 = st.columns(4)

c1.metric("Current Demand", f"{latest_value:,.0f} MW")
c2.metric("Historical Average", f"{average_value:,.0f} MW")
c3.metric("Peak Demand", f"{peak_value:,.0f} MW")
c4.metric(
    "Last Observation",
    latest_timestamp.strftime("%d %b %Y %H:%M")
)


# ============================================================
# HISTORICAL CHART
# ============================================================

st.subheader("Historical Demand - Last 7 Days")

history_chart = (
    df.tail(24 * 7)
    .set_index("Datetime")[["PJMW_MW"]]
)

st.line_chart(history_chart)


# ============================================================
# FORECAST
# ============================================================

st.header("Future Forecast")

if st.button("⚡ Generate Forecast"):
    with st.spinner("Generating forecast..."):
        try:
            forecast_df = generate_forecast(
                df,
                forecast_days,
                model,
                feature_cols,
                holiday_dates
            )

            st.session_state["forecast_df"] = forecast_df

        except Exception as error:
            st.error(f"Forecast generation failed: {error}")


# ============================================================
# SHOW FORECAST RESULTS
# ============================================================

if "forecast_df" in st.session_state:
    forecast_df = st.session_state["forecast_df"]

    st.subheader("Forecast Summary")

    average_forecast = forecast_df["Forecast_MW"].mean()
    maximum_forecast = forecast_df["Forecast_MW"].max()
    minimum_forecast = forecast_df["Forecast_MW"].min()

    peak_row = forecast_df.loc[
        forecast_df["Forecast_MW"].idxmax()
    ]

    peak_time = peak_row["Datetime"]

    f1, f2, f3, f4 = st.columns(4)

    f1.metric(
        "Average Forecast",
        f"{average_forecast:,.0f} MW"
    )

    f2.metric(
        "Forecast Peak",
        f"{maximum_forecast:,.0f} MW"
    )

    f3.metric(
        "Forecast Minimum",
        f"{minimum_forecast:,.0f} MW"
    )

    f4.metric(
        "Expected Peak Time",
        peak_time.strftime("%d %b %H:%M")
    )

    st.subheader("Forecast Chart")

    chart_df = forecast_df.set_index("Datetime")[["Forecast_MW"]]
    st.line_chart(chart_df)

    st.subheader("Hourly Forecast Data")

    display_df = forecast_df.copy()
    display_df["Datetime"] = display_df["Datetime"].dt.strftime(
        "%d-%b-%Y %H:%M"
    )
    display_df["Forecast_MW"] = display_df["Forecast_MW"].round(2)

    st.dataframe(
        display_df,
        use_container_width=True,
        height=450
    )

    csv = forecast_df.to_csv(index=False)

    st.download_button(
        label="⬇️ Download Forecast CSV",
        data=csv,
        file_name=f"pjm_{forecast_days}_day_forecast.csv",
        mime="text/csv"
    )


# ============================================================
# PROJECT INFORMATION
# ============================================================

st.header("Project Information")

st.write("**Model:** XGBoost Regressor")
st.write(
    "**Features:** Hour, Day, DayOfWeek, Month, Year, IsWeekend, "
    "IsHoliday, lag variables and rolling statistics."
)
st.write(
    "**Forecast method:** Recursive multi-step forecasting. "
    "Each prediction is added to the historical sequence and used "
    "to generate the next prediction."
)

st.header("Dataset Information")

d1, d2, d3 = st.columns(3)

d1.metric("Observations", f"{len(df):,}")
d2.metric(
    "Data Start",
    df["Datetime"].min().strftime("%Y")
)
d3.metric(
    "Data End",
    df["Datetime"].max().strftime("%Y")
)

st.caption("PJM Hourly Energy Consumption Forecasting")
