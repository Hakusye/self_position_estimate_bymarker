from PIL import Image
import numpy as np
import time
import cv2
from pprint import pprint
import QRlib

if __name__ == "__main__":
    numcam = 4
    qr = cv2.QRCodeDetector()
    n = 0
    base_path = "images/"
    ext = "png"
    cap = []
    cam = 50
    photo_time = 5.0
    
    for i in range(numcam):
        cap.append(cv2.VideoCapture(i))
    Stime = time.time()
    while True:
        for i in (range(numcam)):
            img, frame = cap[i].read()
            data, points, straight_qrcode = qr.detectAndDecode(frame)
            print(type(points))
            if(str(type(points)) != "<class 'NoneType'>"):
                Gx, Gy = QRlib.CenterOfGravity(points)
                frame[Gy-2:Gy+3, Gx-2:Gx+3] = [0, 0, 255]
                cam = i
                last_frame = frame
            cv2.imshow('frame'+str(i),frame)
        if time.time()-Stime >= photo_time:
            Stime = time.time()
            print("保存n:"+str(n)+",cam:"+str(cam))
            if(cam != 50):
                cv2.imwrite('{}num{}_cam{}.{}'.format(base_path, n,cam ,ext), last_frame)
                n += 1
            cam = 50
        if (n > 9):
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break