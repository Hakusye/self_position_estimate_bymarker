from PIL import Image
import numpy as np
import time
import cv2
import os.path as osp
from pprint import pprint
import random
import glob

def CenterOfGravity(points):
    #points = points.astype(np.int32)
    sumx,sumy = 0.0,0.0
    for i in range(4):
        sumx += points[0][0][i][0]
        sumy += points[0][0][i][1]
    return int(sumx/4),int(sumy/4)

def MinMaxXY(points):
    minx = min([points[0][0][i][0] for i in range(4)])
    maxx = max([points[0][0][i][0] for i in range(4)])
    miny = min([points[0][0][i][1] for i in range(4)])
    maxy = max([points[0][0][i][1] for i in range(4)])
    return minx,maxx,miny,maxy

def PredictedPositionOfCam(image_path,cam2cam_range_yx = [10,10],num_cam_yx = [0,0],range_data="InputRangeData.txt"):
    #prepare
    aruco = cv2.aruco
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    image = cv2.imread(image_path)
    image_range_yx = [image.shape[0],image.shape[1]]
    G = [0,0]
    predict_range_yxd = []
    for i in open(range_data,'r').readlines():
        predict_range_yxd.append(float(i.rstrip('\n')))

    #calc
    corners, ids, rejectedImgPoints = aruco.detectMarkers(image, dictionary) #マーカ
    G[0],G[1] = CenterOfGravity(corners)
    output_range_yx = [0,0]
    for i in range(2):
        output_range_yx[i] += cam2cam_range_yx[i] * num_cam_yx[i] #[y,x]のcam[0,0]座標の位置(cm)
        output_range_yx[i] += G[i] * predict_range_yxd[i] / image_range_yx[i] #QRコードの中心座標(cm)
    
    return output_range_yx #(cm)
    
def MakeDatapathPositionList(rootpath="images/num",est=".png"):
    return glob.glob(rootpath + '*_cam*' + est)

    


    
