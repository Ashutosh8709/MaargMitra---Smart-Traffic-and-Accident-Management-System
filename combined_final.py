import torch
import asyncio
import base64

# Fix asyncio bug with Torch
asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

import os
os.environ["STREAMLIT_DISABLE_WATCHDOG_WARNINGS"] = "true"
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

# Imports
import streamlit as st
from predict_page import show_predict_page
from testing5 import show_speed_monitor_page
from accident_severity_prone import show

# Page config
st.set_page_config(page_title="🚦 Traffic Monitoring System", layout="wide")
st.markdown("""
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
""", unsafe_allow_html=True)

# Initialize session state
if "start_monitoring" not in st.session_state:
    st.session_state.start_monitoring = False
if "nav_option" not in st.session_state:
    st.session_state.nav_option = "home"

# Theme colors (fixed)
bg_color = "#0f1117"
text_color = "#ffffff"
button_bg = "#1f77b4"



# Function to convert GIF to base64
def get_base64_of_bin_file(bin_file_path):
    with open(bin_file_path, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Load and encode the GIF
gif_path = "6be4cff8300f07b219108b3e0dd6540f.gif"  # Make sure this is in /mnt/data/ if using Streamlit Cloud
gif_base64 = get_base64_of_bin_file(gif_path)
# CSS Styling
st.markdown(f"""
    <style>
        html, body, [class*="css"] {{
            background: url("data:image/gif;base64,{gif_base64}") no-repeat center center fixed;
            background-size: cover;
        }}
        .stApp {{
            background-color: rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(2px);
        }}
        .main-title {{
            font-size: 3.5em;
            font-weight: bold;
            text-align: left;
            color: {text_color};
            text-shadow: 2px 2px 5px #555;
            border-radius: 20px;
            display: flex;
            align-items: center;
            gap: 20px;
        }}
        .main-title i{{
            font-size: 2.5em;
            
        }}
        .sub-title {{
            font-size: 1.2em;
            color: gray;
            margin-top:0;
            margin-bottom: 40px;
            margin-left: 120px
        }}
        .nav-container {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 40px;
        }}
        .nav-button {{
            background-color: transparent;
            color: {text_color};
            border: 2px solid {text_color};
            border-radius: 12px;
            padding: 15px 30px;
            font-size: 1.2em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        .nav-button:hover {{
            background-color: {button_bg};
            color: white;
            transform: scale(1.05);
            box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
        }}
        .stButton > button {{
            background-color: {button_bg};
            color: white;
            border-radius: 12px;
            padding: 15px 30px;
            font-size: 0.75em;
            font-weight: 600;
            transition: all 0.3s ease;
            margin-top: 40px;
        }}
        .stButton > button:hover {{
            transform: scale(1.05);
            box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
        }}
        .emoji {{
            font-size: 2em;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.2); }}
            100% {{ transform: scale(1); }}
        }}
    </style>
""", unsafe_allow_html=True)

# ----------------- MAIN NAVIGATION ------------------

if st.session_state.nav_option == "home":
    st.markdown('<div class="main-title"> <i class="fas fa-traffic-light"></i> Smart Traffic Monitoring System</div>', unsafe_allow_html=True)
    # st.markdown('<div class="sub-title">Live Monitoring • Predictive Analysis • Risk Mapping</div>', unsafe_allow_html=True)

    st.markdown("""
    <style>
    .blur-container {
        padding: 50px;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.002);
        box-shadow: 0 12px 35px rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
        margin-top: 40px;
    }

    .background-wrapper::before {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image: url('https://images.unsplash.com/photo-1503264116251-35a269479413?auto=format&fit=crop&w=1470&q=80');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        filter: blur(10px);
        opacity: 0.4;
        z-index: -1;
    }

    @keyframes glow {
        0% { text-shadow: 0 0 10px #1f77b4; }
        50% { text-shadow: 0 0 20px #1f77b4; }
        100% { text-shadow: 0 0 10px #1f77b4; }
    }
    </style>

    <div class="background-wrapper">
        <div class="blur-container">
            <h1 style='font-size: 2.5em; color: #ffffff; animation: glow 2s infinite;'> Welcome to <span style="color:#ffffff;">your MaargMitra</span></h1>
            <p style='font-size: 0.85em; color: #ddd; margin-top: -10px;'>Empowering Urban Mobility through AI and Vision</p>
        </div>
    </div>
""", unsafe_allow_html=True)


    if st.button("🚦 Start Monitoring Now", use_container_width=True):
        st.session_state.start_monitoring = True
        st.rerun()

    if st.session_state.start_monitoring:
        st.markdown('<div class="nav-container">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🚗 Real-time Traffic", use_container_width=True):
                st.session_state.nav_option = "realtime"
                st.rerun()
        with col2:
            if st.button("📈 Congestion Forecast", use_container_width=True):
                st.session_state.nav_option = "forecast"
                st.rerun()
        with col3:
            if st.button("⚠️ Accident Zones", use_container_width=True):
                st.session_state.nav_option = "accidents"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)





# Custom CSS


# Custom CSS for large div and small cards inside it
    import streamlit as st
    import streamlit.components.v1 as components

# Set page background to dark for effect
    st.markdown(
    """
    <style>
    body {
        background-color: #1e1e1e;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

    html_code = """
<style>
    .big-div {
        display: flex;
        justify-content: space-between;
        gap: 30px;
        padding: 20px;
    }

    .custom-card {
        height: 300px;
        width: 420px;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 60px;
        padding: 30px;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        color: #fff;
        text-align: center;
        box-shadow: 0 12px 35px rgba(31, 38, 135, 0.37);
        transition: transform 0.3s ease;
    }

    .custom-card:hover {
        transform: scale(1.03);
    }

    .icon-circle {
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        width: 80px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 20px;
        font-size: 40px;
    }

    .card-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .card-description {
        font-size: 16px;
        line-height: 1.5;
        color: #ddd;
    }
</style>

<div class="big-div">
    <div class="custom-card">
        <div class="icon-circle">📹</div>
        <div class="card-title">Real-Time Monitoring</div>
        <div class="card-description">
            Live detection of vehicles using computer vision.<br>
            Analyze traffic flow and congestion instantly with smart surveillance.
        </div>
    </div>


    <div class="custom-card">
        <div class="icon-circle">📈</div>
        <div class="card-title">Congestion Forecasting</div>
        <div class="card-description">
            Predict future traffic levels using machine learning.<br>
            Plan smarter routes and reduce travel time with data-driven insights.
        </div>
    </div>


    <div class="custom-card">
        <div class="icon-circle">🛑</div>
        <div class="card-title">Accident Risk Analysis</div>
        <div class="card-description">
            Identify accident-prone areas and generate preventive alerts.<br>
            Enhance road safety using AI-powered risk detection.
        </div>
    </div>
</div>
"""

    components.html(html_code, height=450)




    # About Section
    st.markdown("""
        <div style='margin-top: 30px; padding: 35px; background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; box-shadow: 0 6px 25px rgba(0,0,0,0.2); text-align: left;'>
            <h2 style='color:#00b894; font-size: 2.2em;'>📖 About This App</h2>
            <ul style='font-size: 1.2em; line-height: 1.7; color: #ccc;'>
                <li>🔍 <strong>YOLOv8 + DeepSORT</strong> for real-time object tracking</li>
                <li>🧠 ML models for <strong>traffic congestion forecasting</strong></li>
                <li>🗺️ Accident-prone zone detection across India</li>
                <li>⚙️ Built with <strong>Streamlit, PyTorch, OpenCV</strong></li>
                <li>🚀 Fully open-source and customizable</li>
                <li>💡 Designed for city authorities & mobility planners</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    



# Load the uploaded image and encode it to base64
    with open("/Users/ashutoshkumar/Desktop/ML_PROJECT copy/79a4003c8f4b5c576bd43336da7c78a7.png", "rb") as img_file:
        encoded_image = base64.b64encode(img_file.read()).decode()

    components.html(f"""
<style>
    .newsletter-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #82b1ff;
        border-radius: 25px;
        padding: 40px;
        margin-top: 80px;
        font-family: 'Segoe UI', sans-serif;
        color: #1e1e1e;
        height: 300px;
        position: relative;
        overflow: visible;
    }}

    .newsletter-text {{
        max-width: 50%;
    }}

    .newsletter-text h2 {{
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 15px;
    }}

    .newsletter-text p {{
        font-size: 1.1em;
        color: #333;
        margin-bottom: 25px;
    }}

    .form-group {{
        margin-bottom: 15px;
    }}

    .form-group input {{
        width: 100%;
        padding: 12px 15px;
        border-radius: 8px;
        border: 1px solid #ccc;
        font-size: 1em;
    }}

    .form-group input:focus {{
        outline: none;
        border-color: #2962ff;
    }}

    .newsletter-image {{
        max-width: 40%;
        position: relative;
    }}

    .newsletter-image img {{
        max-width: 100%;
        border-radius: 12px;
        margin-top: -80px;
        z-index: 2;
        position: relative;
    }}

    @media (max-width: 900px) {{
        .newsletter-container {{
            flex-direction: column;
            text-align: center;
            height: auto;
        }}

        .newsletter-text, .newsletter-image {{
            max-width: 100%;
        }}

        .newsletter-image {{
            margin-top: 30px;
        }}

        .newsletter-image img {{
            margin-top: -40px;
        }}
    }}
</style>

<div class="newsletter-container">
    <div class="newsletter-text">
        <h2>Get Traffic Intelligence Updates</h2>
        <p>Subscribe to receive real-time traffic insights, system updates, and smart mobility innovations straight to your inbox. Stay ahead of the traffic chaos!</p>
        <div class="form-group">
            <input type="text" placeholder="Your Name*" />
        </div>
        <div class="form-group">
            <input type="email" placeholder="Email Address*" />
        </div>
    </div>
    <div class="newsletter-image">
        <img src="data:image/png;base64,{encoded_image}" alt="Smart Traffic Newsletter" />
    </div>
</div>
""", height=650)

    
    
elif st.session_state.nav_option == "realtime":
    st.subheader("📡 Monitoring Real-time Congestion")
    st.info("Detecting and tracking vehicles using YOLOv8 and DeepSORT...")
    show_speed_monitor_page()
    if st.button("🔙 Back to Home", use_container_width=True):
        st.session_state.nav_option = "home"
        st.rerun()

elif st.session_state.nav_option == "forecast":
    st.subheader("🔮 Predicting Traffic Congestion")
    st.info("Forecasting traffic using ML models trained on historical data...")
    show_predict_page()
    if st.button("🔙 Back to Home", use_container_width=True):
        st.session_state.nav_option = "home"
        st.rerun()

elif st.session_state.nav_option == "accidents":
    st.subheader("🚨 Accident Risk Zones")
    st.warning("Displaying regions with high accident likelihood across India...")
    show()
    if st.button("🔙 Back to Home", use_container_width=True):
        st.session_state.nav_option = "home"
        st.rerun()


