import streamlit as st
import json
import time

ACCIDENT_DB = 'logs/severity_log.json'

st.markdown("""
    <style>
        .alert-box {
            background-color: #ff4b4b;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: white;
            font-size: 22px;
            font-weight: bold;
            animation: blink 1s infinite alternate;
            margin-bottom: 20px;
        }
        @keyframes blink {
            from {opacity: 1;}
            to {opacity: 0.6;}
        }
        .info-box {
            background-color: #1e1e1e;
            padding: 16px;
            border-radius: 10px;
            color: #ffffff;
            box-shadow: 2px 2px 12px #555;
            margin-top: 20px;
        }
        .section-title {
            font-size: 24px;
            font-weight: bold;
            padding-bottom: 10px;
            border-bottom: 2px solid #ff4b4b;
            margin-bottom: 15px;
        }
        .button-container {
            margin-top: 25px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Emergency Alert for Clinics & Helpers")

try:
    with open(ACCIDENT_DB, 'r') as f:
        data = json.load(f)
        if data:
            latest = data[-1]  # Get the most recent entry
        else:
            st.warning("No recent accident data available.")
            st.stop()
except:
    st.error("Error loading accident data.")
    st.stop()

start_time = latest.get('start_time', 'N/A')
severity_score = latest.get('severity_score', 0)
location = latest.get('location', 'Unknown Location')


st.markdown('<div class="alert-box">Accident Reported Nearby - Immediate Assistance Needed!</div>', unsafe_allow_html=True)


st.markdown(f"""
    <div class="info-box">
        <h3 class="section-title">📅 Date & Time: {start_time}</h3>
        <h3 class="section-title">📍 Location: {location}</h3>
        <h3 class="section-title">🔥 Severity Score: <span style="color:{'#ff4b4b' if severity_score >=6 else '#ffa500' if severity_score >=3 else '#4caf50'};">{severity_score}</span></h3>
    </div>
""", unsafe_allow_html=True)
st.markdown("")
st.markdown("")
st.markdown("")
st.info("Nearby helpers or clinics, please proceed to the accident location for immediate assistance.")


st.markdown('<div class="button-container">', unsafe_allow_html=True)
if st.button("✅ Confirm I Have Arrived"):
    st.success("Thank you! Your presence has been recorded for assistance.")
st.markdown('</div>', unsafe_allow_html=True)
if st.button("✅ Confirm I Have Arrived"):
    st.session_state.arrived = True
    st.rerun()

if st.session_state.get("arrived"):
    st.switch_page("first_aid_response.py")  # Requires Streamlit 1.22+ and multipage setup


# Emergency Contact Button
st.markdown("---")
st.markdown("### Need More Help?")
if st.button("Call Emergency Services"):
    st.warning("Emergency services have been alerted. Help is on the way!")


