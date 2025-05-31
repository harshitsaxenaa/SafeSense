import cv2
import imutils
import winsound
from imutils import face_utils
import dlib
from scipy.spatial import distance
from pygame import mixer
import numpy as np
import requests
from geopy.geocoders import Nominatim
from twilio.rest import Client

# Twilio for SMS
TWILIO_ACCOUNT_SID = ''     
TWILIO_AUTH_TOKEN = ''       
TWILIO_PHONE_NUMBER = ''               
RECIPIENT_PHONE_NUMBER = ''           

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def fetch_current_location():
    try:
        ip_info = requests.get("https://ipinfo.io/json").json()
        loc = ip_info.get('loc', None)
        if loc:
            base_lat, base_lon = map(float, loc.split(','))
            city = ip_info.get("city", "")
            region = ip_info.get("region", "")
            country = ip_info.get("country", "")
            location = f"{city}, {region}, {country}"
            location_f = f"{city}"
            print(f"📍 Location: {location}")  
            print(f"📍 {base_lat:.6f}, {base_lon:.6f}")
            return location
        else:
            print(" No location found in API response")
            return "Unknown"
    except Exception as e:
        print(f" Error fetching location: {e}")
        return "Unknown"


def send_sms_alert(location):
    message = client.messages.create(
        body=f"ALERT! Mr. ABC is found unconscious while driving at location {location}. The car has been safely stopped.",
        from_=TWILIO_PHONE_NUMBER,
        to=RECIPIENT_PHONE_NUMBER
    )
    print(f"SMS sent: SID={message.sid}")

# Audio
alarm_playing=False
alarm_sound_path = "mixkit-classic-alarm-995.wav"

# EAR & MAR
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def mouth_aspect_ratio(mouth):
    A = distance.euclidean(mouth[2], mouth[10])
    B = distance.euclidean(mouth[4], mouth[8])
    C = distance.euclidean(mouth[0], mouth[6])
    return (A + B) / (2.0 * C)

def get_head_pose(shape, frame):
    image_points = np.array([
        shape[33], shape[8], shape[36],
        shape[45], shape[48], shape[54]
    ], dtype="double")

    model_points = np.array([
        (0.0, 0.0, 0.0),
        (0.0, -330.0, -65.0),
        (-225.0, 170.0, -135.0),
        (225.0, 170.0, -135.0),
        (-150.0, -150.0, -125.0),
        (150.0, -150.0, -125.0)
    ])

    size = frame.shape
    focal_length = size[1]
    center = (size[1] / 2, size[0] / 2)
    camera_matrix = np.array(
        [[focal_length, 0, center[0]],
         [0, focal_length, center[1]],
         [0, 0, 1]], dtype="double"
    )

    dist_coeffs = np.zeros((4, 1))
    (success, rotation_vector, translation_vector) = cv2.solvePnP(
        model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE
    )
    return (rotation_vector, translation_vector, camera_matrix, dist_coeffs)


# Thresholds
thresh = 0.40
mar_thresh = 0.4
frame_check = 20

eye_flag = 0
yawn_flag = 0
sleep_events = 0
yawn_events = 0

alert_sent = False  # 

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["mouth"]

detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

cap = cv2.VideoCapture(r"C:\Users\harsh\SGU Project\Video1.mp4")

yawn_alert_counter = 0
drowsy_alert_counter = 0
ALERT_DURATION_FRAMES = 60 

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = imutils.resize(frame, width=900) 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    subjects = detect(gray, 0)

    for subject in subjects:
        shape = predict(gray, subject)
        shape = face_utils.shape_to_np(shape)

        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        mouth = shape[mStart:mEnd]

        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        mouthHull = cv2.convexHull(mouth)

        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)

        leftEar = eye_aspect_ratio(leftEye)
        rightEar = eye_aspect_ratio(rightEye)
        ear = (leftEar + rightEar) / 2.0

        mar = mouth_aspect_ratio(mouth)

        if mar > mar_thresh:
            yawn_flag += 1
            yawn_events += 1
            if yawn_flag >= frame_check:
                yawn_alert_counter = ALERT_DURATION_FRAMES
                
        else:
            yawn_flag = 0

        if ear < thresh:
            eye_flag += 1
            sleep_events += 1
            if eye_flag >= frame_check:
                drowsy_alert_counter = ALERT_DURATION_FRAMES
                if not alarm_playing:
                    winsound.PlaySound(alarm_sound_path, winsound.SND_ASYNC | winsound.SND_LOOP)
                    alarm_playing = True
        else:
            if alarm_playing:
                winsound.PlaySound(None, winsound.SND_ASYNC)
                alarm_playing = False
            eye_flag = 0

        if yawn_alert_counter > 0:
            
            cv2.putText(frame, "*******YAWNING******", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            yawn_alert_counter -= 1
        else:
            pass

        if drowsy_alert_counter > 0:
            
            cv2.putText(frame, "*******ALERT (EYES CLOSED)******", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            drowsy_alert_counter -= 1
        else:
            pass

        get_head_pose(shape, frame)

    #Car stop condition + SMS Alert
    if (sleep_events > 500 or yawn_events > 500):
        cv2.putText(frame, "*****STOPPING CAR*****", (150, 300),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
        

        if not alert_sent:
            location = fetch_current_location()  # Fetch real-time location
            send_sms_alert(location)  # Send SMS with location
            alert_sent = True

    cv2.imshow("Driver Monitor", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break



cap.release()
cv2.destroyAllWindows()