import cv2
import os
import sys
import numpy as np
path = os.environ["APPDATA"] + "\\app\\images\\"
print(path)
img = cv2.imread("images/current1.jpg")
# crop1_img = img[0:495, 192:687]
# cv2.imwrite(path + "crop1.jpg", crop1_img)
# crop2_img = img[0:495, 110:770]
resize_img = cv2.resize(img, (660, 495))
cv2.imwrite(path + "resize1.jpg", resize_img)
# cv2.imwrite(path + "resize1.jpg", crop2_img)
sys.stdout.write('\r1')
sys.stdout.flush()