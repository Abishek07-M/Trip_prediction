import streamlit as st
import pandas as pd
import pickle

# Load model and scaler
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

with open("scaler.pkl", "rb") as file:
    scaler = pickle.load(file)

st.set_page_config(
    page_title="Taxi Trip Price Prediction",
    page_icon="🚕"
)

st.title("🚕 Taxi Trip Price Prediction")
st.write("Enter trip details to predict the price")

# Inputs
trip_distance = st.number_input(
    "Trip Distance (km)",
    min_value=0.0,
    value=10.0
)

passenger_count = st.number_input(
    "Passenger Count",
    min_value=1,
    max_value=10,
    value=2
)

base_fare = st.number_input(
    "Base Fare",
    min_value=0.0,
    value=50.0
)

per_km_rate = st.number_input(
    "Per KM Rate",
    min_value=0.0,
    value=15.0
)

per_minute_rate = st.number_input(
    "Per Minute Rate",
    min_value=0.0,
    value=2.0
)

duration = st.number_input(
    "Trip Duration (Minutes)",
    min_value=1,
    value=30
)

time_of_day = st.selectbox(
    "Time of Day",
    ["Morning", "Afternoon", "Evening", "Night"]
)

day = st.selectbox(
    "Day of Week",
    ["Weekday", "Weekend"]
)

traffic = st.selectbox(
    "Traffic Conditions",
    ["Low", "Medium", "High"]
)

weather = st.selectbox(
    "Weather",
    ["Clear", "Rain", "Snow"]
)


# Create input dataframe matching training columns
input_data = pd.DataFrame({
    "Trip_Distance_km": [trip_distance],
    "Passenger_Count": [passenger_count],
    "Base_Fare": [base_fare],
    "Per_Km_Rate": [per_km_rate],
    "Per_Minute_Rate": [per_minute_rate],
    "Trip_Duration_Minutes": [duration],

    "Time_of_Day_Evening": [1 if time_of_day=="Evening" else 0],
    "Time_of_Day_Morning": [1 if time_of_day=="Morning" else 0],
    "Time_of_Day_Night": [1 if time_of_day=="Night" else 0],

    "Day_of_Week_Weekend": [1 if day=="Weekend" else 0],

    "Traffic_Conditions_Low": [1 if traffic=="Low" else 0],
    "Traffic_Conditions_Medium": [1 if traffic=="Medium" else 0],

    "Weather_Rain": [1 if weather=="Rain" else 0],
    "Weather_Snow": [1 if weather=="Snow" else 0]
})


if st.button("Predict Price"):

    # Scale input
    scaled_data = scaler.transform(input_data)

    # Prediction
    prediction = model.predict(scaled_data)

    st.success(
        f"Estimated Trip Price: ₹ {prediction[0]:.2f}"
    )