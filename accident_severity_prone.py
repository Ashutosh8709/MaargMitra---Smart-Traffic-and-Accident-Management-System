import streamlit as st
import folium
import joblib
import pandas as pd
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import requests
import os

def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

def show():
    if not os.path.exists("rf_model.pkl"):
        download_file("https://github.com/Ashutosh8709/Traffic-and-Accident-Management-System/releases/download/v1.0/rf_model.pkl", "rf_model.pkl")

    if not os.path.exists("encoder.pkl"):
        download_file("https://github.com/Ashutosh8709/Traffic-and-Accident-Management-System/releases/download/v1.0/encoder.pkl", "encoder.pkl")

    if not os.path.exists("scaler.pkl"):
        download_file("https://github.com/Ashutosh8709/Traffic-and-Accident-Management-System/releases/download/v1.0/scaler.pkl", "scaler.pkl")

    rf_model = joblib.load("rf_model.pkl")
    encoder = joblib.load("encoder.pkl")
    scaler = joblib.load("scaler.pkl")
    
    


    # 📌 Feature names
    features = ['Road_Type', 'Speed_limit', 'Weather_Conditions', 'Number_of_Vehicles', 'latitude', 'longitude', 'Day_of_Week']
    categorical_features = ['Road_Type', 'Weather_Conditions', 'Day_of_Week']
    numeric_features = ['Speed_limit', 'Number_of_Vehicles', 'latitude', 'longitude']

    # 📌 Streamlit App Layout
    st.title("🚦 Accident Severity Prediction")

    # 📍 Dropdown to select the section
    option = st.selectbox("Select a Section:", ["📌 View Accident-Prone Areas", "🔍 Predict Accident Severity"])

    # 📍 Section 1: Display the Existing Accident-Prone Map
    if option == "📌 View Accident-Prone Areas":
        st.subheader("🗺️ Accident-Prone Areas in India")
        st.markdown("This map highlights accident-prone areas in India.")
        with open("accident_risk_map.html", "r", encoding="utf-8") as file:
            st.components.v1.html(file.read(), height=600, scrolling=True)

    # 📍 Section 2: Predict Severity Based on User Input
    elif option == "🔍 Predict Accident Severity":
        st.subheader("🚗 Predict Accident Severity")

        road_type = st.selectbox("Road Type:", [1, 2, 3, 4])
        speed_limit = st.slider("Speed Limit (km/h):", 10, 150, 50)
        weather = st.selectbox("Weather Conditions:", [1, 2, 3, 4, 5])
        num_vehicles = st.slider("Number of Vehicles:", 1, 10, 2)
        latitude = st.number_input("Latitude:", format="%.6f")
        longitude = st.number_input("Longitude:", format="%.6f")
        day_of_week = st.selectbox("Day of the Week:", [1, 2, 3, 4, 5, 6, 7])

        if st.button("🚀 Predict Severity"):
            # Convert inputs to correct types
            input_data = pd.DataFrame([[int(road_type), float(speed_limit), int(weather), int(num_vehicles), float(latitude), float(longitude), int(day_of_week)]],
                                  columns=features)

            # Ensure categorical values are reshaped properly before transformation
            input_data[categorical_features] = encoder.transform(input_data[categorical_features].astype(str))
            input_data[numeric_features] = scaler.transform(input_data[numeric_features])

            # Predict severity
            rf_prediction = rf_model.predict(input_data)[0] + 1  # Adjust label back

            # Display results
            st.success(f"✅ Predicted Severity: {rf_prediction} (1=Fatal, 2=Serious, 3=Minor)")

            # 📌 Map Output
            color = 'red' if rf_prediction == 1 else 'orange' if rf_prediction == 2 else 'green'

            accident_map = folium.Map(location=[latitude, longitude], zoom_start=12)
            folium.Marker(
                location=[latitude, longitude],
                popup=f"Predicted Severity: {rf_prediction}",
                icon=folium.Icon(color=color)
            ).add_to(accident_map)

            st.subheader("🗺️ Map with Predicted Severity")
            folium_static(accident_map)
