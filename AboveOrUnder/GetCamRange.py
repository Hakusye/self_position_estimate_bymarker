from PIL import Image
import numpy as np
import time
import cv2
import math
import QRlib
import queue

#####測り方雑だけどだいたい良い感じにできた
if __name__ == "__main__":
	cap = cv2.VideoCapture(0)
	img, frame = cap.read()
	StandardDistance = 28.0 # 実際測った距離17cm
	StandardArea = 262.0 * 256.0 # 上の時の面積

	StandardAreaX = 262.0 # 上の時の面積
	ApparentSize = 0.0
	cnt=0
	xst = math.radians(120.0)
	#yst = math.radians(30.0)
	que = queue.Queue()
	while True:
		cnt+=1
		img, frame = cap.read()
		frame = cv2.resize(frame, (int(frame.shape[1]/2), int(frame.shape[0]/2)))
		qr = cv2.QRCodeDetector()
		data, points, straight_qrcode = qr.detectAndDecode(frame)
		if(str(type(points)) != "<class 'NoneType'>"):
			points = points.astype(np.int32)
			minx = min([points[i][0][0] for i in range(4)])
			maxx = max([points[i][0][0] for i in range(4)])
			miny = min([points[i][0][1] for i in range(4)])
			maxy = max([points[i][0][1] for i in range(4)])
			print(str(minx)+ " " + str(maxx) + " " + str(miny) + " " + str(maxy))
			Gx,Gy = QRlib.CenterOfGravity(points)
			ApparentSize = (maxx-minx) * (maxy-miny)
			ApparentSizeX = (maxx-minx)
			Predicted = StandardDistance * (StandardAreaX/ApparentSizeX)
			Xrange = 2 * Predicted * math.tan(xst/2)
			Yrange = Xrange * 9.0 / 16.0
			#Yrange = 2 * Predicted * math.tan(yst/2)
			print("predicted distance:"+ str(Predicted) + "cm,Xrange:"+str(Xrange)+"cm,Yrange:"+str(Yrange))
			frame[Gy-2:Gy+3,Gx-2:Gx+3] = [0,0,255]
			que.put(Predicted)
			if(que.qsize()>=10):
				que.get()
		cv2.imshow('GPU', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
		          break
	maxi = 0
	while( que.empty() == False):
		tmp = que.get()
		if(maxi < tmp):
			maxi = tmp
	Predicted = maxi
	Xrange = 2 * Predicted * math.tan(xst/2)
	Yrange = Xrange * 9.0 / 16.0
	print("Yrange:" + str(Yrange) + "cm Xrange:" + str(Xrange) + "cm Predicted:" + str(Predicted) + "cm")
