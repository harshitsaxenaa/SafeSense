import streamlit as st
import json
from datetime import datetime
import google.generativeai as genai  

# --- Gemini API Setup ---
GOOGLE_API_KEY = ""  # Enter your actual API key
genai.configure(api_key=GOOGLE_API_KEY)


try:
    with open("logs/severity_log.json", "r") as f:
        logs = json.load(f)
except FileNotFoundError:
    st.error("Log file not found.")
    st.stop()

if not logs:
    st.error("No logs found.")
    st.stop()


data = logs[-1]
detected_labels = data.get("detection_state", {})
severity = data.get("severity_score", 0)
location = data.get("location", "Unknown")
datetime_str = data.get("start_time", "N/A")


st.title("Emergency First-Aid Guidance")

st.markdown("## Detected Conditions")
for label in ["accident", "fire", "smoke", "blood", "lying_person"]:
    if detected_labels.get(label, "No") == "Yes":
        st.checkbox(label.replace("_", " ").title(), value=True, disabled=True)

st.markdown("## Severity Level")
st.info(f"Severity Score: {severity} | Location: {location} | Time: {datetime_str}")

# --- Gemini Prompt ---
prompt = f"""
An accident has occurred. The following conditions were detected:
- Severity Score: {severity}
- Fire Present: {"Yes" if detected_labels.get("fire", "No") == "Yes" else "No"}
- Smoke Present: {"Yes" if detected_labels.get("smoke", "No") == "Yes" else "No"}
- Blood Detected: {"Yes" if detected_labels.get("blood", "No") == "Yes" else "No"}
- Person Unconscious or Lying: {"Yes" if detected_labels.get("lying_person", "No") == "Yes" else "No"}

As a medical expert, please provide:
1. A clear, quick checklist of **first aid steps** suitable for nearby helpers before ambulance arrives.
2. Tips based on the current severity and detected elements.
3. Mention things to avoid or watch out for.
Keep the response short and effective.
"""

try:
    model = genai.GenerativeModel("gemini-1.5-flash")  # You can also try "gemini-1.5-flash" for faster output
    response = model.generate_content(prompt)
    st.markdown("## First-Aid Instructions (Powered by Gemini AI)")
    st.success(response.text)
except Exception as e:
    st.error(f"Error from Gemini API: {str(e)}")
