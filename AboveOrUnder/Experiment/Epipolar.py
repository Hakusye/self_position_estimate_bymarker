from PIL import Image
import numpy as np
import time
import cv2

def drawlines(img1,img2,lines,pts1,pts2):
    ''' img1 - img2上の点に対応するエピポーラ線を描画する画像
        lines - 対応するエピポーラ線 '''
    c = img1.shape[1]
    #img1 = cv2.cvtColor(img1,cv2.COLOR_GRAY2BGR)
    #img2 = cv2.cvtColor(img2,cv2.COLOR_GRAY2BGR)
    for r,pt1,pt2 in zip(lines,pts1,pts2):
        color = tuple(np.random.randint(0,255,3).tolist())
        x0,y0 = map(int, [0, -r[2]/r[1] ])
        x1,y1 = map(int, [c, -(r[2]+r[0]*c)/r[1] ])
        img1 = cv2.line(img1, (x0,y0), (x1,y1), color,1)
        img1 = cv2.circle(img1,tuple(pt1),5,color,-1)
        img2 = cv2.circle(img2,tuple(pt2),5,color,-1)
    return img1,img2

if __name__ == "__main__":
	cap1 = cv2.VideoCapture(0)
	cap2 = cv2.VideoCapture(1)
	img1, frame1 = cap1.read()
	img2, frame2 = cap2.read()
	cnt=0

	while True:
		img1,frame1 = cap1.read() # frameは抜いた
		img2,frame2 = cap2.read()
		frame1 = cv2.resize(frame1, (int(frame1.shape[1]/2), int(frame1.shape[0]/2)))
		frame2 = cv2.resize(frame2, (int(frame2.shape[1]/2), int(frame2.shape[0]/2)))
		#qr = cv2.QRCodeDetector() 使うかわからない
		#data, points, straight_qrcode = qr.detectAndDecode(frame)
		sift = cv2.xfeatures2d.SIFT_create()
		#frame1= cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
		#frame2= cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
		#特徴量検出
		kp1,des1 = sift.detectAndCompute(frame1,None)
		kp2,des2 = sift.detectAndCompute(frame2,None)
		# 対応点探索のためのFLANNパラメタ
		FLANN_INDEX_KDTREE = 0
		index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees = 5)
		search_params = dict(checks=50)
		# 対応点検出
		flann = cv2.FlannBasedMatcher(index_params,search_params)
		matches = flann.knnMatch(des1,des2,k=2)

		good = [] #対応点のあるpts
		pts1 = [] #1camからみた対応点の位置
		pts2 = [] #2camからみた対応点の位置

	# Loweの論文に記載されている特徴量の類似度の比に基づくマッチングの評価
		for i,(m,n) in enumerate(matches):
		    if m.distance < 0.8*n.distance:
		        good.append(m)
		        pts2.append(kp2[m.trainIdx].pt)
		        pts1.append(kp1[m.queryIdx].pt)
		pts1 = np.int32(pts1)
		pts2 = np.int32(pts2)
		F, mask = cv2.findFundamentalMat(pts1,pts2,cv2.FM_LMEDS)
		#print("F:"+str(F))#+","+"mask:"+str(mask))
	# 外れ値を取り除く
		pts1 = pts1[mask.ravel()==1]
		pts2 = pts2[mask.ravel()==1]
		# 右画像(二番目の画像)中の点に対応するエピポーラ線の計算
# 計算したエピポーラ線を左画像に描画
		lines1 = cv2.computeCorrespondEpilines(pts2.reshape(-1,1,2), 2,F)
		lines1 = lines1.reshape(-1,3)
		#print(frame1.shape)
		img5,img6 = drawlines(frame1,frame2,lines1,pts1,pts2)

		# 左画像(一番目の画像)中の点に対応するエピポーラ線の計算
		# 計算したエピポーラ線を右画像に描画
		lines2 = cv2.computeCorrespondEpilines(pts1.reshape(-1,1,2), 1,F)
		lines2 = lines2.reshape(-1,3)
		img3,img4 = drawlines(frame2,frame1,lines2,pts2,pts1)

		cv2.imshow('GPU', img5)
		cv2.imshow('noPU', img3)
		if cv2.waitKey(6000) & 0xFF == ord('q'):
		          break


	cap.release()
	cv2.destroyAllWindows()
