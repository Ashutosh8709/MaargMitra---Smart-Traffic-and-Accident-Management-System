import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import calendar
import requests
import os

def download_and_load_pickle(url, local_path):
    # Download if not already present
    if not os.path.exists(local_path):
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        response = requests.get(url)
        with open(local_path, "wb") as f:
            f.write(response.content)
    # Load the pickle file
    with open(local_path, "rb") as f:
        return pickle.load(f)

def load_model():
    base_url = "https://github.com/Ashutosh8709/Traffic-and-Accident-Management-System/releases/download/v1.0/"
    
    data1 = download_and_load_pickle(base_url + "final_model_1.pkl", "models/final_model_1.pkl")
    data2 = download_and_load_pickle(base_url + "final_model_2.pkl", "models/final_model_2.pkl")
    data3 = download_and_load_pickle(base_url + "final_model_3.pkl", "models/final_model_3.pkl")
    data4 = download_and_load_pickle(base_url + "final_model_4.pkl", "models/final_model_4.pkl")

    return data1, data2, data3, data4

# Load models
data1, data2, data3, data4 = load_model()

# Extract actual model objects
m1 = data1['model']
m2 = data2['model']
m3 = data3['model']
m4 = data4['model']

e = data1['le_day']

def date_to_day(year, month, date):
    date = datetime.datetime(year, month, date)
    day = calendar.day_name[date.weekday()]
    return day

def show_predict_page():

    st.title("Traffic Prediction")

    st.write("""### We need some information about the date and Junction to predict the traffic.""")
    
    year = {
        2025,2026,2027,2028,2029,2030
    }

    month = {
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12
    }

    date = {
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31
    }

    hour = {
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23
    }

    

    junction = {
        1, 2, 3, 4 
    }

    year = st.selectbox("In what year would you be travelling?", year)
    month = st.selectbox("Type in the month", month)
    date = st.selectbox("Type in the date", date)
    hour = st.selectbox("At what approximate hour would you be travelling?", hour)
    junction = st.selectbox("Which Junction would you be following?", junction)

    day = date_to_day(year, month, date)
    day = e[day]

    ok = st.button("Predict Traffic")

    if ok:
        if junction == 1:
            prediction = m1.predict([[year, month, date, hour, day]])
            prediction = int(np.ceil(prediction[0]))
            st.subheader(f"The number of vehicles on the Junction 1 at the given hour are predicted to be {prediction}")
            if prediction > 36:
                st.subheader(f"The congestion at Junction 1 at given hour are predicted to be high")
            elif prediction >14:
                st.subheader(f"The congestion at Junction 1 at given hour are predicted to be medium")
            else:
                st.subheader(f"The congestion at Junction 1 at given hour are predicted to be low")

        elif junction == 2:
            prediction = m2.predict([[year, month, date, hour, day]])
            prediction = int(np.ceil(prediction[0]))
            st.subheader(f"The number of vehicles on the Junction 2 at the given hour are predicted to be {prediction}")
            if prediction > 36:
                st.subheader(f"The congestion at Junction 2 at given hour are predicted to be high")
            elif prediction > 14:
                st.subheader(f"The congestion at Junction 2 at given hour are predicted to be medium")
            else:
                st.subheader(f"The congestion at Junction 2 at given hour are predicted to be low")

        elif junction == 3:
            prediction = m3.predict([[year, month, date, hour, day]])
            prediction = int(np.ceil(prediction[0]))
            st.subheader(f"The number of vehicles on the Junction 3 at the given hour are predicted to be {prediction}")
            if prediction > 36:
                st.subheader(f"The congestion at Junction 3 at given hour are predicted to be high")
            elif prediction > 14:
                st.subheader(f"The congestion at Junction 3 at given hour are predicted to be medium")
            else:
                st.subheader(f"The congestion at Junction 3 at given hour are predicted to be low")

        elif junction == 4:
            prediction = m4.predict([[year, month, date, hour, day]])
            prediction = int(np.ceil(prediction[0]))
            st.subheader(f"The number of vehicles on the Junction 4 at the given hour are predicted to be {prediction}")  
            if prediction > 36:
                st.subheader(f"The congestion at Junction 4 at given hour are predicted to be high")
            elif prediction > 14:
                st.subheader(f"The congestion at Junction 4 at given hour are predicted to be medium")
            else:
                st.subheader(f"The congestion at Junction 4 at given hour are predicted to be low")         
