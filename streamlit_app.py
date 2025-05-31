import streamlit as st
import json
import os

st.set_page_config(page_title="Incident Dashboard", layout="wide")

LOG_FILE = 'logs/severity_log.json'
ACCIDENT_DB = 'logs/accident_db.json'

# Load logs
def load_logs():
    try:
        with open(LOG_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

# Save logs
def save_logs(logs):
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)

# Delete session
def delete_session(session_id):
    logs = load_logs()
    logs = [session for session in logs if session.get('session_id') != session_id]
    save_logs(logs)
    st.success(f"Session {session_id} deleted successfully!")
    st.rerun()

# Load accident database
def load_accident_db():
    try:
        with open(ACCIDENT_DB, 'r') as dbf:
            return json.load(dbf)
    except:
        return {}

# Custom Styles for Dashboard
st.markdown("""
    <style>
        .session-card {
            border-radius: 10px;
            padding: 15px;
            background-color: #1a1a1a;
            color: white;
            margin-bottom: 10px;
            box-shadow: 2px 2px 10px #aaaaaa;
        }
        .status {
            font-weight: bold;
            color: #ff4b4b;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🚨 Emergency Incident Monitoring")

logs = load_logs()
accident_data = load_accident_db()
accident_time = accident_data.get("datetime", "")

if not logs:
    st.warning("No active sessions.")
else:
    for session in reversed(logs):
        session_id = session.get("session_id", "Unknown ID")
        session_time = session.get('start_time', '')
        severity_score = session.get('severity_score', 0)
        blood_detected = session.get('detection_state', {}).get('blood_detected', 'No') == 'Yes'
        
        
        status = session.get('status', 'N/A').capitalize()
        status_color = "#ff4b4b" if status == "Critical" else "#ffa500" if status == "Moderate" else "#4caf50"

        st.markdown(f"""
            <div class="session-card">
                <h3>Session ID: {session_id} <span class="status" style="color:{status_color};">({status})</span></h3>
                <p><b>Start Time:</b> {session_time}</p>
                <p><b>Severity Score:</b> {severity_score}</p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### Detection States")
            with st.expander("View Detection Details"):
                for key, value in session.get('detection_state', {}).items():
                    emoji = "✅" if value == 'Yes' else "❌"
                    st.write(f"- **{key.replace('_', ' ').title()}**: {emoji} {value}")

        with col2:
            st.markdown("### Severity Breakdown")
            st.metric(label="Score", value=severity_score)
            
            if severity_score >= 6:
                st.error("🚨 Critical Severity Detected!")
            elif severity_score >= 3:
                st.warning("⚠️ Moderate Severity")
            elif severity_score > 0:
                st.info("ℹ️ Low Severity")
            else:
                st.success("✅ No Threat Detected")

        st.button(f"🗑️ Delete Session {session_id}", key=f"del_{session_id}", on_click=lambda: delete_session(session_id))
        st.divider()