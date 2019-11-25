from PIL import Image
import numpy as np
import time
import cv2
import math
import Markerlib
import queue

#####測り方雑だけどだいたい良い感じにできた
if __name__ == "__main__":
	aruco = cv2.aruco
	dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
	cap = cv2.VideoCapture(0)
	img, frame = cap.read()
	StandardDistance = 63.6#(cm) 
	MarkerSize = 13.8 #(cm)
	StandardArea = 80.0 * 86.0 
	StandardAreaX = 80.0 
	ApparentSize = 0.0
	ApparentSizeX = 0.0
	cnt=0
	xst = math.radians(120.0)
	#yst = math.radians(30.0)
	
	while True:
		cnt+=1
		img, frame = cap.read()
		frame = cv2.resize(frame, (int(frame.shape[1]/2), int(frame.shape[0]/2)))
		corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, dictionary) #マーカ
		if(str(type(ids)) != "<class 'NoneType'>"):
			corners = np.array(corners)
			minx,maxx,miny,maxy = Markerlib.MinMaxXY(corners)
			#print("maxx:"+str(maxx)+",minx:"+str(minx)+",maxy:"+str(maxy)+",miny:"+str(miny))
			Gx,Gy = Markerlib.CenterOfGravity(corners)
			ApparentSize = (maxx-minx) * (maxy-miny)
			ApparentSizeX = maxx - minx
			Predicted = StandardDistance * (StandardAreaX/ApparentSizeX)
			Xrange = 2 * Predicted * math.tan(xst/2)
			Yrange = Xrange * 9.0 / 16.0
			print("Yrange:" + str(Yrange) + "cm Xrange:" + str(Xrange) + "cm Predicted:" + str(Predicted) + "cm")
			frame[Gy-2:Gy+3,Gx-2:Gx+3] = [0,0,255]
		cv2.imshow('GPU', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
		          break
			  
	Xrange = 2 * Predicted * math.tan(xst/2)
	Yrange = Xrange * 9.0 / 16.0
	f = open('InputRangeData.txt','w')
	f.write(str(Yrange)+"\n"+str(Xrange)+"\n"+str(Predicted))
	print("Yrange:" + str(Yrange) + "cm Xrange:" + str(Xrange) + "cm Predicted:" + str(Predicted) + "cm")
	f.close()