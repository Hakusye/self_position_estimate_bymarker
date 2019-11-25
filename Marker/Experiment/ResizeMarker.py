import cv2

file_path="../marker_images/"
img = cv2.imread(file_path + "marker.png")
img = cv2.resize(img,(900,780))
cv2.imshow("resize",img)
cv2.waitKey(1000)
cv2.imwrite(file_path + "900_780_marker.png",img)
