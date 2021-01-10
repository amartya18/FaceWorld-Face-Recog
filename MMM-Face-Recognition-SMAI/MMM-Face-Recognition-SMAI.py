# SMAI V1.01 - Face Recognition Module

# Modified by: Pratik & Eben
# This is a modified script from the open source face recognition repo:
#https://github.com/ageitgey/face_recognition
# Patch update to fix bugs

import cv2
import picamera
import numpy as np
import sys
import os
import time

import lib.face as face
import lib.config as config

# Get a reference to the Raspberry Pi camera.
# If this fails, make sure you have a camera connected to the RPi and that you
# enabled your camera in raspi-config and rebooted first.

# load model
model = config.model(config.RECOGNITION_ALGORITHM, config.POSITIVE_THRESHOLD)
model.load("training.xml")

# load camera
preview = True
detection_active = True
camera = config.get_camera(preview)

while True:
    time.sleep(1)
    print("Capturing image.")
    frame = camera.read()

    # Find all the faces and face encodings in the current frame of video
    image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    result = face.detect_single(image)
    
    label_str = "None"
    
    if result is not None:
        x, y, w, h = result
        # x and y coordinates of the face
        x_face = x
        y_face = y
        if config.RECOGNITION_ALGORITHM == 1:
            crop = face.crop(image, x, y, w, h)
        else:
            crop = face.resize(face.crop(image, x, y, w, h))

        # test face against model
        label, confidence = model.predict(crop)

        match = "None"
        label_str = "None"
        if (label != -1 and label != 0):
            label_str = config.user_label(label)

        # print(label_str)

        # manual user list
        if label_str == "User3":
            label_str = "Marc"
        elif label_str == "User1":
            label_str = "Marcell"
        elif label_str == "User2":
            label_str = "Amar"

        # the closer confidence is to zer the stronger the match
        # if confidence < 0.6 * config.POSITIVE_THRESHOLD:
        #     label_str = 'Strong:' + label_str
        # elif confidence < config.POSITIVE_THRESHOLD:
        #     label_str = 'Weak:' + label_str
        # elif confidence < 1.5 * config.POSITIVE_THRESHOLD:
        #     label_str = "Guess: " + label_str
        # else:
        #     lavel_str = "Unknown"

    print("Person Detected: {}!".format(label_str))

    if label_str != "None":
        print("IM IN!")
        f = open("/home/pi/MagicMirror/modules/MMM-Face-Recognition-SMAI/sample.txt", "w")
        f.write(label_str)
        f.close()
        #time taken before the user is logged off from the mirror
        time.sleep(15)
            
    f = open("/home/pi/MagicMirror/modules/MMM-Face-Recognition-SMAI/sample.txt", "w")
    f.write(label_str)
    f.close()
