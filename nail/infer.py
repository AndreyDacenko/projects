from keras.models import model_from_yaml
from keras.models import Sequential
import cv2
import numpy as np
import os
import sys

model = Sequential()

image_resize = (299, 299)
imw = image_resize[0]
imh = image_resize[1]

# target_file = './current1.jpg'

target_file = os.environ["APPDATA"] + "\\app\\images\\crop1.jpg"
save = os.environ["APPDATA"] + "\\app\\images\\"
base_img = cv2.imread(target_file, 1)


def load():
    global model
    yaml_file = open('C:\\Users\\Admin\\Desktop\\RightVersion\\Electron\\nails\\nail\\nails\\[NAIL]model_conv.yaml',
                     'r')
    loaded_model_yaml = yaml_file.read()
    yaml_file.close()
    model = model_from_yaml(loaded_model_yaml)
    model.load_weights('C:\\Users\\Admin\\Desktop\\RightVersion\\Electron\\nails\\nail\\nails\\[NAIL]model_conv.h5')

def crop(x, y):
    global map
    crop_img = base_img[y: 62 + y, x: 62 + x, 0:3]
    resized = cv2.resize(crop_img, image_resize)
    resized = (resized[..., ::-1].astype(np.float32)) / 255.0
    # print(resized.shape)
    reshaped = resized.reshape(1, imh, imw, 3)
    out = model.predict(reshaped)  # prediction
    print(f'OUT:{out}')
    # if out[0][1][0] > 0.5:
    #     cv2.rectangle(base_img, (x, y), (x + 62, y + 62), (0, 255, 0), 1)
    #
    #     map[y][x] = out[0][1][0]

# def check():
#
#
#     cv2.imwrite(save + f'result[{out[0][0]:.2f}][{out[0][1]:.2f}][{out[0][2]:.2f}].jpg'
#                 , base_img)
#     cv2.imwrite(save + 'relize.jpg', base_img)


x = 0
y = 0
maxWidth = base_img.shape[1]
maxHeight = base_img.shape[0]
# print(maxWidth,maxHeight)
map = np.zeros((maxHeight, maxWidth))


if __name__ == '__main__':
    print(f'Main: {x}, {y}')
    load()
    # model.summary()

    while y < (maxHeight - 62):
        x = 0
        while x < (maxWidth - 62):
            crop(x, y)
            x += 62
        y += 62

cv2.imwrite('map.jpg', map * 255)
cv2.imwrite("result.jpg", base_img)
# print('all ok')
sys.stdout.write('\r6')
sys.stdout.flush()
