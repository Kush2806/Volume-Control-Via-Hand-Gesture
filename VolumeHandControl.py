import cv2
import time
import numpy as np
import math
import hand_tracking_module as htm
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

pTime = 0
cTime = 0

detector = htm.HandDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    Lmlist = detector.findPosition(img,draw=False)
    if len(Lmlist) != 0:
        # print(Lmlist[4], Lmlist[8])
        x1, y1 = Lmlist[4][1], Lmlist[4][2]
        x2, y2 = Lmlist[8][1], Lmlist[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2
        cv2.circle(img,(x1,y1),11,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),11,(255,0,255),cv2.FILLED)
        cv2.circle(img,(cx,cy),11,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)

        length = math.hypot(x2-x1,y2-y1)
        # print(length)
        vol = np.interp(length,[50,300],[minVol,maxVol])
        volume.SetMasterVolumeLevel(vol, None)

        if length < 50:
            cv2.circle(img,(cx,cy),11,(0,255,0),cv2.FILLED)
    

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img,f'FPS: {int(fps)}',(40,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
    
    cv2.imshow("Img",img)
    cv2.waitKey(1)