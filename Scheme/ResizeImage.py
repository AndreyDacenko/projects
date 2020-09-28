import cv2
import sys

f = open("path_to_image.txt",mode = 'r',encoding = 'utf-8')
path_to_image = f.read()
f.close()
img = cv2.imread(path_to_image)
resize_img = cv2.resize(img, (3900, 3900))
cv2.imwrite("resizePAN.jpg", resize_img)
sys.stdout.write('\r9')
sys.stdout.flush()