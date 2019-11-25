from PIL import Image
import numpy as np
import time
import cv2
from pprint import pprint
cap = cv2.VideoCapture(0)
img, frame = cap.read()
while True:
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
		frame[miny:(maxy+1),minx:(maxx+1),0] = 255
	cv2.imshow('GPU', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
	          break

cap.release()
cv2.destroyAllWindows()
