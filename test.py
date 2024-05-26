import cv2
import time
import math
import numpy as np
import HandTrackingModule as htm
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


wCam, hCam = 1288, 720

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

volRange=volume.GetVolumeRange()
minVol=volRange[0]
maxVol=volRange[1]
volume.SetMasterVolumeLevel(-20.0, None)


cap = cv2.VideoCapture (0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime=8

detector = htm.handDetector()


while True:
    success, img=cap.read()
    img= detector.findHands(img)
    lmlist=detector.findPosition(img, draw=False)
    if len(lmlist)!=0:
        print(lmlist)

        x1,y1= lmlist[4][1], lmlist[4][2]
        
        x2,y2= lmlist[8][1], lmlist[8][2]
        cx,cy=(x1+x2)//2, (y1+y2)//2
        cv2.circle(img, (x1,y1), 15, (255,8,255),cv2.FILLED)
        cv2.circle(img, (x2,y2), 15, (255,8,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,8,255),3)

        length=math.hypot(x2-x1,y2-y1)
        print(length)

        vol=np.interp(length,[50,300],[minVol,maxVol])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol,None)


        if length<50:
            cv2.circle(img,(cx,cy),15,(0,255,0), cv2.FILLED)


    cTime = time.time()
    
    fps = 1/ (cTime - pTime)
    pTime=cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 58), cv2.FONT_HERSHEY_COMPLEX, 
                1, (255,0,0), 3)
    cv2.imshow("Img", img)
    cv2.waitKey(1)
























 