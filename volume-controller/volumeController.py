from handDetector import HandDetector
import cv2
import math
import numpy as np
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from pynput.keyboard import Key, Controller

handDetector = HandDetector(min_detection_confidence=0.7)
webcamFeed = cv2.VideoCapture(0)

# Volume related initializations
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# print(volume.GetVolumeRange()) --> (-65.25, 0.0)

while True:
    status, image = webcamFeed.read()
    handLandmarks = handDetector.findHandLandMarks(image=image, draw=True)

    if(len(handLandmarks) != 0):
        # for volume control we need 4th and 8th landmark
        # details: https://google.github.io/mediapipe/solutions/hands
        # 4 Thumb
        # 8 Index
        x1, y1 = handLandmarks[4][1], handLandmarks[4][2]
        x2, y2 = handLandmarks[8][1], handLandmarks[8][2]
        length_4_8 = math.hypot(x2-x1, y2-y1)
        # print(length_4_8)

        # Hand range(length_4_8): 50-250
        # Volume Range: (-65.25, 0.0)

        # coverting length_4_8 to proportionate to volume range
        volumeValue = np.interp(length_4_8, [50, 250], [-65.25, 0.0])
        volume.SetMasterVolumeLevel(volumeValue, None)

        cv2.circle(image, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(image, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 3)
        

        # Media Keys
        # Next Track
        # 12 Middle

        keyboard = Controller()

        x3, y3 = handLandmarks[12][1], handLandmarks[12][2]
        length_8_12 = math.hypot(x3-x2, y3-y2)
        # print(length_8_12)
        if(length_8_12 < 50):
            # print("HELLO WORLD")
            keyboard.press(Key.media_next)
            time.sleep(1) #more work

        cv2.circle(image, (x3, y3), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(image, (x2, y2), (x3, y3), (255, 255, 0 ), 3)

    cv2.imshow("Volume", image)
    cv2.waitKey(1)
