import cv2

def arReader():
    cap = cv2.VideoCapture(0) #ビデオキャプチャの開始
    while True:
        ret, frame = cap.read() #ビデオキャプチャから画像を取得
        Height, Width = frame.shape[:2] #sizeを取得
        img = cv2.resize(frame,(int(Width/3),int(Height/3)))
        corners, ids, rejectedImgPoints = aruco.detectMarkers(img, dictionary) #マーカ
        aruco.drawDetectedMarkers(img, corners, ids, (0,255,0))
        cv2.imshow('drawDetectedMarkers', img)
        if cv2.waitKey(1) == 27:
            break
    cap.release() #ビデオキャプチャのメモリ解放
    cv2.destroyAllWindows() #すべてのウィンドウを閉じる

if __name__ == "__main__":
    aruco = cv2.aruco #arucoライブラリ
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    arReader()
