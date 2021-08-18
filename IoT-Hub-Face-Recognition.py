import face_recognition
import cv2
import numpy as np

import requests

# starting video capture usning webcam number 0
video_capture = cv2.VideoCapture(0)

# You can add different pictures to recognize them, in this sample I just added 2 different images
# First Image
First_User_image = face_recognition.load_image_file("img-database/hans.jpeg")
# Encode the first image
First_User_Face_Encoding = face_recognition.face_encodings(First_User_image)[0]

# Second Image
Second_User_image = face_recognition.load_image_file("img-database/leo.jpeg")
# Encode the second image
Second_User_Face_encoding = face_recognition.face_encodings(Second_User_image)[0]

# We have to put encoded images in an array
known_face_encodings = [
    First_User_Face_Encoding,
    Second_User_Face_encoding
    #Add third, fourth and ...
]
# Input names related to images in order
known_face_names = [
    "Hans",
    "Leo"
]

# Declair the Master name, the person who his/her face will active Smart Home IoT systems
# WHO IS THE MASTER ?
Master = "Hans"

# Making 3 arrays for storing face locations and face encodings and face names
face_locations = []
face_encodings = []
face_names = []
# Make it true to enter the if and then we will make it false to continue the code running inside the while loop
process_this_frame = True
# Using this booleans to make one post request only
valid_face_request = True
invalid_face_request = True
name = "No Name"
TempName = "tmp"

# ------------------------------- Face Recognition Section ----------------------------------
# ---------Reading Webcam Frames, comparing with known faces and using face_distance to choose the nearest face-------------

while True:
    # We have to choose a single frame from webcam video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)


    # making process_this_frame false to continue running the code inside while loop
    process_this_frame = not process_this_frame
    # make name to "No Name" if there is no face
    name = "No Name"


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # This line is for drawing a rectangle box around the detected face
        cv2.rectangle(frame, (left, top), (right, bottom), (52, 110, 235), 10)

        # Fill the name caption area at the bottom of the box
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (52, 89, 235), cv2.FILLED)
        # selecting font
        font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
        # Text Font size, color, position and thickness
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.5, (255, 255, 255), 2)

    # Display Analyzed video on new window
    cv2.imshow('IOT Vision', frame)


    # ------------------------------- IOT Section ----------------------------------
    # ---------Using Python "request" to send HTTP POST requests to our API----------

    if name == Master and TempName != Master:
        url = 'https://lightlinks.ir/button/iot.php'
        myobj = {'id': '322', 'gp1': '1', 'gp2': '1'}

        Re = requests.post(url, data=myobj)

        print(Re.text)
        print("My Master")
        TempName = name

    if  name == "No Name"  and TempName != "No Name":
        url = 'https://lightlinks.ir/button/iot.php'
        myobj = {'id': '322', 'gp1': '1', 'gp2': '0'}

        Re = requests.post(url, data=myobj)

        print(Re.text)
        print(name)
        TempName = name
        print("Not My Master")


    # Just a quick code to use "q" key as exit option
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    print(name)


# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
