import cv2
import numpy as np
import os
import sys
import requests
from timeit import default_timer as timer
import concurrent.futures

# model = Sequential()

# target_file = './current1.jpg'
url = f"http://localhost:8000/check"
content_type = 'image/jpeg'
header = {'content-type': content_type}

target_file = os.environ["APPDATA"] + "\\app\\images\\resize1.jpg"
save = os.environ["APPDATA"] + "\\app\\images\\"
base_img = cv2.imread(target_file, 1)

# print(maxWidth,maxHeight)


x = 0
y = 0
maxWidth = base_img.shape[1]
maxHeight = base_img.shape[0]

map = np.zeros((maxHeight, maxWidth))
# bolezn_list = [0, 0, 0]

i = 0




def check(coords):
    x = coords[0]
    y = coords[1]
    # global map
    # global bolezn_list
    crop_img = base_img[y: 300 + y, x: 300 + x]

    _, encoded = cv2.imencode('.jpg', crop_img)

    r = requests.post(url, data=encoded.tostring(), headers=header)

    r = [float(x) for x in r.json()]

    # cv2.imwrite(save + 'relize' + i + '.jpg', crop_img)

    # i += 1

    # if (r[0] > 0.75) or (r[1] > 0.75):
    #     # cv2.rectangle(base_img, (x, y), (x + 300, y + 300), (0, 255, 0), 1)
    #     map[y][x] = max(r[0], r[1])
    #     # bolezn_list.append([r[0], r[1], r[2]])
    #     if (max(r[0], r[1])) > (max(bolezn_list)):
    #         bolezn_list = [r[0], r[1], r[2]]

    return r
    # print(out[0][0], out[0][1])

    # data = r.json()
    # print(data)


if __name__ == '__main__':
    # check()

    with open('config.txt', 'r') as f:
        nums = f.read().splitlines()
    # print(nums[0], nums[1])
    maxResult = []
    bolezni = []
    resultMax = (0, 0, (0, 0, 0))

    while y < maxHeight - int(nums[3]):
        row = []
        x = 0
        while x < maxWidth - int(nums[2]):
            # check(x, y)
            row.append((x, y))
            # x += 60
            x += int(nums[0])
        with concurrent.futures.ThreadPoolExecutor(max_workers=9) as executor:
            result = executor.map(check, row)
        listRes = list(result)
        listRes = [tuple(val) for val in listRes]
        # print(listRes)
        # print(len(listRes))
        listResult = [0, 0, 0]
        xcoord = -1

        for i, value in enumerate(listRes):
            # print(f'val: {value}, max: {max(value[0], value[1])}')
            if max(listResult[0], listResult[1]) < max(value[0], value[1]):
                listResult = value
                xcoord = i
        maxResult.append((xcoord * int(nums[0]), y, listResult))
        # print(listResult)
        # y += 60
        y += int(nums[1])

    # [print(f'{entry}') for entry in maxResult]
    for val in maxResult:
        if max(resultMax[2]) < max(val[2]):
            resultMax = val
    # print(f'Absolute maximum: {resultMax}')

    for y in range(maxHeight):
        if y == resultMax[1]:
            for x in range(maxWidth):
                if x == resultMax[0]:
                    map[y][x] = max(resultMax[2][0], resultMax[2][1])
                    bolezni = resultMax[2]
                    # print(resultMax[2][1])
                    # print(map[y][x])

    for y in range(maxHeight):
        for x in range(maxWidth):
            if map[y][x] > 0.78:
                cv2.rectangle(base_img, (x, y), (x + int(nums[2]), y + int(nums[3])), (0, 0, 255), 2)


my_file = open('bolezni.txt', 'w')
try:
    my_file.write(f'[{bolezni[0]:.2f}][{bolezni[1]:.2f}][{bolezni[2]:.2f}]')
except IndexError:
    my_file.write(f'[0][0][1]')
my_file.close()
# cv2.imwrite("map.jpg", map * 255)
cv2.imwrite(save + 'relize.jpg', base_img)

sys.stdout.write('\r6')
sys.stdout.flush()


    # maximum = 0
    # for y in range(maxHeight):
    #     for x in range(maxWidth):
    #         if map[y][x] > maximum:
    #             maximum = map[y][x]
    #
    # for y in range(maxHeight):
    #     for x in range(maxWidth):
    #         if map[y][x] < maximum:
    #             map[y][x] = 0
    #
    # for y in range(maxHeight):
    #     for x in range(maxWidth):
    #         if map[y][x] > 0.9:
    #             cv2.rectangle(base_img, (x, y), (x + 300, y + 300), (0, 0, 255), 2)

# print(maximum)
# print(bolezn_list)
#
# my_file = open('bolezni.txt', 'w')
#
# try:
#     my_file.write(f'[{bolezn_list[0]:.2f}][{bolezn_list[1]:.2f}][{bolezn_list[2]:.2f}]')
# except IndexError:
#     my_file.write(f'[0][0][1]')
# my_file.close()
#
# cv2.imwrite(save + 'relize.jpg', base_img)
# # cv2.imwrite("map.jpg", map * 255)
# sys.stdout.write('\r6')
# sys.stdout.flush()
