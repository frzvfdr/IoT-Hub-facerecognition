# IoT Hub Face Recognition
A Python based program using OpenCV, Face recognition and Requests to control Light Links IoT Hub GPIO values Online and Real-Time.

# How it works?
**In Simple Words:** <br/>

The program detects the presence of the Master User ( Who is privillaged to use smart home equipments ) in the room ( Multiple cameras needed) or in front of a webcam by detecting his/her face and if the user photo is detected in the image database, then the program will send HTTP POST requests to your IoT Server API so you can control smart home facilities using Computer vision and Face Recognition.

**In More Detail:** <br/>

- This program uses OpenCV and Face Recognition to capture your connected camera (WebCam) video and it will choose single resized (1/4 of the original size) live video frames of the camera to compare each frame with its Image Database.
- Then we use face_distance to match the video frame to the most similar image in the database, If the video frame matches the image then code will search for the person name related to the detected image.
- Now the IoT part begins, if the person name matches the Master User name, the program will send an HTTP post request to IoT server API in order to activate the smart home equipment ( in this example it will make [Light Links](https://lightlinks.ir) IoT Hub's GPIO Active High, Otherwise, if the detected face is unknown or not in the database ( or no face detected ) it will send HTTP POST request to DeActivate the equipment.
> This program is Online and Real-Time so you can extend this code in case of controling servo motors, relays and other I/Os using Computer Vision.

# Requirements and installation:
- [X] Cmake :
  - it is important to have Cmake, it is necessary for installing and using Dlib and Face Recognition packages.
  - In MAC you have to install X-Code command line tools and Homebrew.
- [X] Dlib
- [X] Face Recognition
- [X] OpenCV
- [X] Requests
- [X] Numpy
  - Numpy is needed for frame size calculations<br/>

**Running the code :**
- First, it is recommended to creat a folder named "image-database" in the same directory as the code ( just clone this repository to have an error-free experience! )
- Run the code using :
```sh
python3 IoT-Hub-Face-Recognition.py
```
- now a new window showing webcam output and your detected face as "unknown" face will popup.
- I've added the images of Hans Zimmer and Leonardo Dicaprio in the img-database folder as samples. You can add your own.

**Adding images to image databse :** <br/>
You can simply copy your own images to img-database folder, but keep in mind that you have to change image name in the code and add your own name to the known_face_names array. For doing that follow the steps :
 - change the name of the first and the second users photo in this line to your image names:
```sh
First_User_image = face_recognition.load_image_file("img-database/Your-Photo.png")

Second_User_image = face_recognition.load_image_file("img-database/Second-user-photo.jpg")
```
- Add the person name related to first and second photo in known_face_names array:

```sh
known_face_names = [
    "Your name",
    "Second user name if exists"
]
```
- Now you've customized the Face Recognition Section based on your biometrics.
- For IoT section you have to connect the code to your IoT platform API and change the Json array. **If you use Light Links IoT Hubs then just input your device UID and enjoy your Computer Vision IoT Hub!**
- The first Key value in myobj Json array is the place where you have to input your device UID.( you can change other objects to satisfy your needs)

```sh
myobj = {'id': 'Input your Light links IOT hub and router UDI here', 'gp1': '1', 'gp2': '1'}
]
```


