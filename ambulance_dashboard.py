import streamlit as st
from streamlit_autorefresh import st_autorefresh
import json

st.set_page_config(page_title="Emergency Response Dashboard", layout="wide")

# Custom Styling
st.markdown("""
    <style>
        .card {
            background-color: #121212;
            padding: 15px;
            border-radius: 10px;
            color: white;
            margin-bottom: 10px;
            box-shadow: 2px 2px 10px #555;
        }
        .title {
            text-align: center;
            font-size: 26px;
            color: white;
            background: linear-gradient(to right, #ff4b4b, #ffa500);
            padding: 10px;
            border-radius: 8px;
        }
        .status {
            font-weight: bold;
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

# Password protection
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        with st.form("password_form"):
            password = st.text_input("🔒 Enter Password", type="password")
            submitted = st.form_submit_button("Unlock")
            if submitted:
                if password == "1234abc":
                    st.session_state.authenticated = True
                else:
                    st.error("Incorrect password. Try again.")
                    st.stop()
            else:
                st.stop()

check_password()

ACCIDENT_DB = 'logs/severity_log.json'
ROUTE_DB = 'logs/routes_db.json'


st_autorefresh(interval=4000, key="ambulance_refresh")

st.markdown('<div class="title">Live Ambulance Response System</div>', unsafe_allow_html=True)

try:
    with open(ACCIDENT_DB, 'r') as f:
        data = json.load(f)
        if not data:
            st.warning("No recent accident data available.")
            st.stop()
        latest = data[-1]
except:
    st.error("")
    st.stop()


start_time = latest.get('start_time', 'N/A')
severity = latest.get('severity_score', 0)
status = latest.get('status', '').lower()
location = "ABC"  

st.markdown(f"""
    <div class="card">
        <h3>Accident Detected Nearby</h3>
        <p><b>Date & Time:</b> {start_time}</p>
        <p><b>Location:</b> {location}</p>
        <p><b>Severity Score:</b> <span class="status" style="color:{'#ff4b4b' if severity >=6 else '#ffa500' if severity >=3 else '#4caf50'};">{severity}</span></p>
    </div>
""", unsafe_allow_html=True)

if status != "ambulance enroute":
    if st.button("🚑 Accept Ambulance Dispatch"):
        try:
            latest['status'] = 'ambulance enroute'
            data[-1] = latest
            with open(ACCIDENT_DB, 'w') as f:
                json.dump(data, f, indent=4)
            st.success("🚑 Request Accepted. Ambulance is enroute now!")
            st.experimental_rerun()
        except:
            st.error("")
else:
    st.success("Ambulance has already accepted the request and is enroute.")

    # Show route details 
    try:
        with open(ROUTE_DB) as f:
            routes = json.load(f)

        relevant_routes = [r for r in routes if r['location'] == location]

        if relevant_routes:
            best_route = min(relevant_routes, key=lambda r: r['estimated_time_min'])
            
            st.markdown("### Best Route to Accident Scene")
            col1, col2 = st.columns([1, 1])

            with col1:
                st.write(f"**Route ID:** {best_route['route_id']}")
                st.write(f"**Distance:** {best_route['distance_km']} km")

            with col2:
                st.write(f"**ETA:** {best_route['estimated_time_min']:.2f} mins")
                st.progress(best_route['estimated_time_min'] / 30)  # Visual ETA

        else:
            st.warning("No route information available for the location.")
    except:
        st.error("Error fetching route details.")

    
    st.markdown("---")
    if st.button("Reset Ambulance Dispatch"):
        try:
            latest['status'] = 'pending'
            data[-1] = latest
            with open(ACCIDENT_DB, 'w') as f:
                json.dump(data, f, indent=4)
            st.success("Dispatch request reset to pending.")
            st.experimental_rerun()
        except:
            st.error("")