from PIL import Image
import numpy as np
import time
import cv2
from pprint import pprint
import Markerlib
import re

if __name__ == "__main__":
    aruco = cv2.aruco
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    y_num_cam = 1 #今はてきとー
    x_num_cam = 4 #てきとー(使わないけど見た目的に)
    cam2cam_range_yx = [80,80] #(cm)
    image_path = Markerlib.MakeDatapathPositionList()
    f = open('PositionListLabel.txt','w')
    positionlist = [] 
    for path in image_path:
        cam_position = [0,0]
        label = re.findall('[0-9]+',path)
        #print(label)
        cam_position[0] = int(label[1]) % y_num_cam
        cam_position[1] = int(int(label[1]) / y_num_cam)

        py,px = Markerlib.PredictedPositionOfCam(
            image_path = path, cam2cam_range_yx = cam2cam_range_yx, num_cam_yx = cam_position)
        positionlist.append([label[0],py,px])
        print(label[0] + "\n" + str(py) + "\n" + str(px))
    positionlist.sort()
    for row in positionlist:
        f.write("\n" + str(row[0]) + " " + str(row[1]) + " " + str(row[2]))

    f.close()
    

