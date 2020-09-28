import numpy as np
import cv2
import multiprocessing
import sys

def isoblob(args):
    imagename = args[0]
    blobsize = args[1]
    bordersize = args[2]

    image = cv2.imread(f'{imagename}.bmp', 1)
    (h, w) = image.shape[:2]

    side = blobsize + bordersize
    result = image.copy()

    for x in range(0, w, 1):
        for y in range(0, h, 1):
            if image[y, x, 2] > 250 and image[y, x, 0] < 10 and image[y, x, 0] < 10:
                redcrop = image[y - side: y + side, x - side: x + side, 2]
                othercrop = image[y - side: y + side, x - side: x + side, 0:2]
                if (np.sum(redcrop) >= 255) and (np.sum(othercrop) <= 50):
                    result[y - side: y + side, x - side: x + side, 0:3] = (0, 255, 0)

    cv2.imwrite(f'{imagename}_MARKUP.bmp', result)
    markplate = cv2.imread(f'{imagename}.bmp', 0)
    markplate = cv2.cvtColor(markplate, cv2.COLOR_GRAY2BGR)
    markplate_copy = markplate.copy()
    markplate[np.where((result[:, :, 1] == 255) & (result[:, :, 0] == 0))] = np.asarray([0, 0, 255]).astype(np.uint8)
    markplate_copy[np.where((result[:, :, 1] == 255) & (result[:, :, 0] == 0))] += np.asarray([0, 0, 100])\
        .astype(np.uint8)

    factor = 8
    att_window = [markplate.shape[0] // factor, markplate.shape[1] // factor]
    border = 3

    for x in range(factor):
        for y in range(factor):
            X = x * att_window[0]
            Y = y * att_window[1]
            crop = markplate[X: X + att_window[0], Y: Y + att_window[1], 0:3]
            detect_red = np.where((crop[:, :, 2] == 255) & (crop[:, :, 0] == 0), 1, 0)
            # print(np.sum(detect_red))
            if np.sum(detect_red) > 1:
                markplate_copy[X: X + border, Y: Y + att_window[1], 2] = 255
                markplate_copy[X + att_window[0] - border: X + att_window[0], Y: Y + att_window[1], 2] = 255
                markplate_copy[X: X + att_window[0], Y: Y + border, 2] = 255
                markplate_copy[X: X + att_window[0], Y + att_window[1] - border: Y + att_window[1], 2] = 255

    cv2.imwrite(f'{imagename}_ATT_FILTERED.bmp', markplate_copy)


def main():
    blobs = [['COMPARISON_MASK', 1, 1], ['COMPARISON', 2, 4]]
    # blobs = [['COMPARISON', 2, 3]]
    pool = multiprocessing.Pool(4)
    pool.map(isoblob, blobs)
    pool.close()


if __name__ == '__main__':
    main()
    sys.stdout.write('\r9')
    sys.stdout.flush()


