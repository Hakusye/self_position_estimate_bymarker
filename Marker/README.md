# 詳しい使い方は
../AboveOrUnder/README.mdをみて

# なにを編集したか記録に残す
"QRlib.py"->"Markerlib.py"

"GetCamRange.py" -> InputRangeData.txtにYrange,Xrange,height_Predictionを保存できるようになった

"photo.py" -> どのカメラにQRコードがみえているか判断できるようになった

# レンズの設定は手動で行なう必要あり
## 広角レンズの設定
xst = math.radians(120.0)
StandardDistance = 63.6#(cm) 
MarkerSize = 13.8 #(cm)
StandardArea = 80.0 * 86.0 
StandardAreaX = 80.0 