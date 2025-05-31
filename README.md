## Project Execution Result Video Link: 
https://drive.google.com/file/d/1bBtus8Zff5HJA-OgjbsQkawmEcXI96O3/view?usp=sharing

Accident Prevention Module: https://drive.google.com/file/d/1UIgWLIhtA0Z7nh_Ddh-hUO9gukot6vN6/view?usp=sharing

## 📂 Results Folder
Access the results [here](Results/)

## Problem Statement: 
India witnesses over 4.6 lakh road accidents every year, leading to significant fatalities due to delayed emergency response. Traditional systems rely on human intervention, manual reporting, and are reactive instead of predictive. Emergency response delays occur due to lack of real-time accident detection, severity estimation, and proactive prevention measures. No integrated platform combines vehicle data, video, audio, and AI-driven crowd-aid and first-aid guidance to trigger timely interventions and accident prevention.

## Current Issues:
1. Lack of AI-powered prevention alerts to detect driver unconsciousness or drowsiness early.
2. Lack of real-time, automated accident detection mechanisms. 
3. No predictive estimation of accident severity or victim conditions.
4. Delayed ambulance dispatch and poor routing decisions cause avoidable deaths.
5. Absence of unified integrated systems integrating visual, audio, and sensor-based accident evidence. 
6. Need for a scalable, intelligent, city-wide system that reduces response time and improves post-accident outcomes.

## Proposed Solution:
SAFESENSE is a real-time accident detection and emergency response system based on multi-source inputs:
1. Prevention Module: Detects driver unconsciousness or drowsiness using facial analysis (yawning, eye closure) and issues early alerts to prevent accidents. Can halt the vehicle automatically if driver is unconscious.
2. Visual Detection (YOLOv8): Detect crashes, vehicle rollovers, smoke, fire, and fallen pedestrians from CCTV/ dashcams’ feeds.
3. Audio Analysis (YAMNet): Screeching tires, crashes—detectable even in low-visibility conditions. 
## 4. ML-Based Severity Prediction: Force of impact, number of victims, presence of flames, victim condition to predict severity.
5. Emergency Dispatch Engine: Auto-routes ambulance using Google Maps API and notifies hospitals based on severity. 
6. Crowd-Aid Module: Sends alerts to nearby verified users for immediate on-ground support before EMS arrives.

## Predictive Output:
1. Prevention Alerts: Driver unconsciousness and drowsiness detection alerts to avoid accidents.
2. Accident Detection: Real-time classification of accident vs. non-accident frames on basis of CCTV footage, sound etc.
3. Severity Estimation: Score on 1–10 scale for triage prioritization. 
4. Victim Count Estimation: Human pose detection and blood presence. 
5. Live Emergency Alerts: Exact GPS location and Severity level 
6. Suggested optimal ambulance route: On basis of time to reach/ traffic. 
7. Crowd-Aid Prompt: Instant notification to nearby civilians willing to help (Also for people planning to travel via same route.

## Steps to run:
Follow these steps to run the code on your local system:

1. Clone the repository:
   ```bash
   git clone https://github.com/harshitsaxenaa/SafeSense.git

2. Change directory:
   ```bash
   cd SafeSense

3. Create virtual environment:
   ```bash
   python -m venv venv

4. Activate virtual environment:
   ```bash
   venv\Scripts\activate

5. Install dependencies:
   ```bash
   pip install -r requirements.txt

6. Run scripts:
   ```bash
   python main.py

7. Open dashboards:
   ```bash
   streamlit run streamlit_app.py
   streamlit run ambulance_dashboard.py
   streamlit run nearby_help_page.py
   streamlit run Location Mapping.py
   streamlit run first_aid_response.py

OR click on file
run_streamlit.bat
    
