import cv2

def arGenerator():
    fileName = "../maker_images/ar.png"
    generator = aruco.drawMarker(dictionary, 0, 100)
    generator = cv2.resize(generator,(780,780))
    cv2.imwrite(fileName, generator)
    img = cv2.imread(fileName)
    #cv2.imshow('ArMaker',img)
    cv2.waitKey(0)


if __name__ == "__main__":
    aruco = cv2.aruco #arucoライブラリ
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    print(type(dictionary))
    arGenerator()
