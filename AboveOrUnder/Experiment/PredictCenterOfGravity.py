from PIL import Image
import numpy as np
import time
import cv2
from pprint import pprint

def CenterOfGravity(points):
    points = points.astype(np.int32)
    sumx,sumy = 0.0,0.0
    for i in range(4):
        sumx += points[i][0][0]
        sumy += points[i][0][1]
    return int(sumx/4),int(sumy/4)


if __name__ == "__main__":
    capL = cv2.VideoCapture(0)
    capR = cv2.VideoCapture(1)
    #1/4インチとしてやる。あってるかは怪しい
    pixToum = 2.8 #1pixel => 2.8μm
    cmToum = 10000
    T = 10 * 1e4 # 71450 pixel  cm ->μm
    fx = 20 * 1e4 #142900 pixel cm ->μm
    qr = cv2.QRCodeDetector()
    Z = 1e9
    preZ = 1e9
    Adjust = 0.5 #定数調整
    fx = np.load("mtxR.npy")[0][0]

    while True:
        imgL, frameL = capL.read()
        imgR,frameR = capR.read()
        GxL,GyL,GxR,GyR = False,False,False,False
        ### QRコードの座標取得.重心決めるときに使う
        data, points, straight_qrcode = qr.detectAndDecode(frameL)
        if(str(type(points)) != "<class 'NoneType'>"):
            GxL,GyL = CenterOfGravity(points)
        data, points, straight_qrcode = qr.detectAndDecode(frameR)
        if(str(type(points)) != "<class 'NoneType'>"):
            GxR,GyR = CenterOfGravity(points)
        
        if(GxL and GxR):
            Z = fx * (T/pixToum)/((GxL - GxR))*Adjust
            frameL[GyL-2:GyL+3,GxL-2:GxL+3] = [0,0,255]
            frameR[GyR-2:GyR+3,GxR-2:GxR+3] = [0,0,255]
        cv2.imshow('frameL', frameL)
        cv2.imshow('frameR', frameR)
    cap.release()
    cv2.destroyAllWindows()
