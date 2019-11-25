from PIL import Image
import numpy as np
import time
import cv2
import os.path as osp
from pprint import pprint
import random
import glob

def CenterOfGravity(points):
    points = points.astype(np.int32)
    sumx,sumy = 0.0,0.0
    for i in range(4):
        sumx += points[i][0][0]
        sumy += points[i][0][1]
    return int(sumx/4),int(sumy/4)


def PredictedPositionOfCam(image_path,cam2cam_range_yx = [10,10],num_cam_yx = [0,0],range_data="InputRangeData.txt"):
    #prepare 
    qr = cv2.QRCodeDetector()
    image = cv2.imread(image_path)
    image_range_yx = [image.shape[0],image.shape[1]]
    G = [0,0]
    predict_range_yxd = []
    for i in open(range_data,'r').readlines():
        predict_range_yxd.append(float(i.rstrip('\n')))

    #calc
    data, points, straight_qrcode = qr.detectAndDecode(image)
    G[0],G[1] = CenterOfGravity(points)
    output_range_yx = [0,0]
    for i in range(2):
        output_range_yx[i] += cam2cam_range_yx[i] * num_cam_yx[i] #[y,x]のcam[0,0]座標の位置(cm)
        output_range_yx[i] += G[i] * predict_range_yxd[i] / image_range_yx[i] #QRコードの中心座標(cm)
    
    return output_range_yx #(cm)
    
def MakeDatapathPositionList(rootpath="images/num",est=".png"):
    return glob.glob(rootpath + '*_cam*' + est)

    
def MotionDecected(frame,before=None):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if before is None:
        before = gray.copy().astype('float')
    # 現フレームと前フレームの加重平均を使うと良いらしい
    cv2.accumulateWeighted(gray, before, 0.5)
    mdframe = cv2.absdiff(gray, cv2.convertScaleAbs(before))

    # 動いているエリアの面積を計算してちょうどいい検出結果を抽出する
    thresh = cv2.threshold(mdframe, 3, 255, cv2.THRESH_BINARY)[1]
    # 輪郭データに変換しくれるfindContours
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    target = contours[0]
    for cnt in contours:
         #輪郭の面積を求めてくれるcontourArea
        area = cv2.contourArea(cnt)
        if max_area < area and area < 10000 and area > 1000:
            max_area = area
            target = cnt

    # 動いているエリアのうちそこそこの大きさのものがあればそれを矩形で表示する
    if max_area <= 1000:
        areaframe = frame
    else:
        # 諸般の事情で矩形検出とした。
        x,y,w,h = cv2.boundingRect(target) #x,y は始点,w,hは長さ
    #    areaframe = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
    return x+w/2,y+h/2
    #cv2.imshow('MotionDetected Area Frame', areaframe)
    # キー入力を1ms待って、k が27（ESC）だったらBreakする
    
