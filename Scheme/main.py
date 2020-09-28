import numpy as np
import cv2
import multiprocessing
import sys

image_path = open("path_to_image.txt", encoding = 'utf-8')
path_to_image = image_path.read()
image_path.close()

mask_path = open("path_to_mask.txt", encoding = 'utf-8')
path_to_mask = mask_path.read()
mask_path.close()

# MASK_path = './MASK.jpg'
# PAN_path = './PAN.jpg'
MASK_path = path_to_mask
PAN_path = path_to_image
CORRECTED_path = './CORRECTED.jpg'
shifted_mask = ''
shifted_pan = ''


def equalize(im1, im2):
    # sys.stdout.write(f'Got image 1 of shape: {im1.shape} and image 2 of shape: {im2.shape}\r')
    # sys.stdout.flush()
    score1, score2 = sum(im1.shape), sum(im2.shape)
    if score1 > score2:
        # sys.stdout.write(f'im1 found to be largest with the shape of {im1.shape}\r')
        # sys.stdout.flush()
        im1 = cv2.resize(im1, im2.shape[::-1], interpolation=cv2.INTER_LANCZOS4)
    else:
        # sys.stdout.write(f'im2 found to be largest with the shape of {im2.shape}\r')
        # sys.stdout.flush()
        im2 = cv2.resize(im2, im1.shape[::-1], interpolation=cv2.INTER_LANCZOS4)
    # sys.stdout.write(f'Sending image 1 of shape: {im1.shape} and image 2 of shape: {im2.shape}\r')
    # sys.stdout.flush()
    return im1, im2


def invertBW(image):
    # image = 255 * (image > 30)
    return 255 - image


def correctAngleProjection(image, limit=1., delta=0.02):
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)

    def find_score(_image, _angle):
        _M = cv2.getRotationMatrix2D(center, angle, 1.0)
        _rotated = cv2.warpAffine(_image.astype(np.uint8), _M, (w, h))
        _hist = np.sum(_rotated, axis=1)
        _score = np.sum((_hist[1:] - _hist[:-1]) ** 2)
        return _hist, _score

    angles = np.arange(-limit, limit + delta, delta)
    scores = []
    for angle in angles:
        hist, score = find_score(image, angle)
        scores.append(score)

    best_score = max(scores)
    best_angle = angles[scores.index(best_score)]
    # print(f'Best angle: {best_angle}\r')

    M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
    rotated = cv2.warpAffine(image.astype(np.uint8), M, (w, h))
    return rotated


def img_diff(gauge, image, f_range=4):
    # def plot_wb(wbimage):
    #     plt.axis('off')
    #     plt.imshow(wbimage, cmap='gray', vmin=0, vmax=255)
    #     plt.show()

    husk = np.zeros(gauge.shape)

    gauge = cv2.normalize(gauge, husk, 0, 255, cv2.NORM_MINMAX)
    # _, gauge = cv2.threshold(gauge, 127, 255, cv2.THRESH_BINARY)
    gauge = np.where(gauge > 127, 255, 0)

    image = cv2.normalize(image, husk, 0, 255, cv2.NORM_MINMAX)
    # _, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    image = np.where(image > 127, 255, 0)

    diff = np.subtract(gauge, image)
    # diff = gauge - image
    ################################################################
    filtered_gauge = np.where(diff > 0, diff, 0)  # gauge filtration
    # filtered_gauge = np.abs(diff)
    ###############################################################
    # plot_wb(filtered_gauge)
    if f_range != 0:
        #######              Filtering close details             #######
        fmax, smax = filtered_gauge.shape
        for fdim in range(fmax):
            for sdim in range(smax):
                if gauge[fdim, sdim] == 0:
                    filtered_gauge[fdim - f_range:fdim + f_range, sdim - f_range:sdim + f_range] = 0
        ################################################################
    # plot_wb(filtered_gauge)
    return filtered_gauge


def align(image1, image2, maxrange=5):
    shift, value = 0, image1.shape[0] * image1.shape[0] * 255

    husk = np.zeros(image1.shape)

    image1 = cv2.normalize(image1, husk, 0, 255, cv2.NORM_MINMAX)
    # _, image1 = cv2.threshold(image1, 127, 255, cv2.THRESH_BINARY)
    image1 = np.where(image1 > 127, 255., 0)

    image2 = cv2.normalize(image2, husk, 0, 255, cv2.NORM_MINMAX)
    # _, image2 = cv2.threshold(image2, 127, 255, cv2.THRESH_BINARY)
    image2 = np.where(image2 > 127, 255., 0)

    x_shifts, y_shifts = range(-maxrange, maxrange), range(-maxrange, maxrange)

    num_rows, num_cols = image2.shape[:2]

    for x in x_shifts:
        for y in y_shifts:
            translation_matrix = np.float32([[1, 0, x], [0, 1, y]])
            image2_translated = cv2.warpAffine(image2, translation_matrix, (num_cols, num_rows))
            diff = np.subtract(image1, image2_translated)
            ################################################################
            diff = np.where(diff > 0, diff, 0)  # filtration
            ###############################################################
            curr = np.sum(diff)
            if curr < value:
                value = curr
                shift = (x, y)
                # print(f'for shift of {(x, y)}, value is {curr}\r')

    translation_matrix = np.float32([[1, 0, shift[0]], [0, 1, shift[1]]])
    shifted = cv2.warpAffine(image2, translation_matrix, (num_cols, num_rows))

    return shifted, shift


def diffwrap(inbind):
    base = inbind[0]
    aux = inbind[1]
    tolerance = inbind[2]
    comment = inbind[3]
    diff = img_diff((255 - base), aux, tolerance)
    # print(f'Saving result for tolerance = {tolerance}\r')
    cv2.imwrite(f'./DIFF[tolerance.{tolerance}{comment}].jpg', diff)


# def comparison(compare_to, name='COMPARISON'):
def comparison(args):
    compare_to = args[0]
    name = args[1]

    base = cv2.imread(MASK_path, 1)
    base = 255 - base

    highlight = cv2.imread(f'./DIFF[tolerance.{compare_to}].jpg', 0)

    base, highlight = equalize(base, highlight)

    display = np.zeros(base.shape)

    display[:, :, 0:2] = base[:, :, 0:2]
    display[:, :, 2] = np.where(highlight > 127, highlight, base[:, :, 2])

    display[np.where((highlight > 127) & (base[:, :, 2] > 127))] = [153, 153, 100]

    display = np.where(display > 127, 255, 0)

    display[np.where((display > [250, 250, 250]).all(axis=2))] = [100, 100, 100]
    cv2.imwrite(f'./{name}.bmp', display)


def missing(args):
    compare_to = args[0]
    name = args[1]

    base = cv2.imread(CORRECTED_path, 1)
    base = 255 - base

    highlight = cv2.imread(f'./DIFF[tolerance.{compare_to}.MASK_FIRST].jpg', 0)

    base, highlight = equalize(base, highlight)

    display = np.zeros(base.shape)

    display[:, :, 0:2] = base[:, :, 0:2]
    display[:, :, 2] = np.where(highlight > 127, highlight, base[:, :, 2])

    # display[np.where((highlight > 127) & (base[:, :, 2] > 127))] = [153, 153, 100]

    display = np.where(display > 127, 255, 0)

    display[np.where((display > [250, 250, 250]).all(axis=2))] = [100, 100, 100]
    cv2.imwrite(f'./{name}.bmp', display)


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
            # X, Y = x * side, y * side
            # print(f'X: {X}, Y: {Y}')
            if image[y, x, 2] > 200:
                redcrop = image[y - side: y + side, x - side: x + side, 2]
                othercrop = image[y - side: y + side, x - side: x + side, 0:2]
                # print(f'redcrop: {np.sum(redcrop)}, othercrop: {np.sum(othercrop)}')
                if (np.sum(redcrop) > 50) and (np.sum(othercrop) < 200):
                    temp_side = side + 1
                    redcrop = image[y - temp_side: y + temp_side, x - temp_side: x + temp_side, 2]
                    othercrop = image[y - temp_side: y + temp_side, x - temp_side: x + temp_side, 0:2]
                    if (np.sum(redcrop) >= 255) and (np.sum(othercrop) <= 255):
                        result[y - temp_side: y + temp_side, x - temp_side: x + temp_side, 0:3] = (0, 255, 0)

    cv2.imwrite(f'{imagename}_MARKUP.bmp', result)
    markplate = cv2.imread(f'{imagename}.bmp', 0)
    markplate = cv2.cvtColor(markplate, cv2.COLOR_GRAY2BGR)
    markplate[np.where((result[:, :, 1] == 255) & (result[:, :, 0] == 0))] += np.asarray([0, 0, 100]).astype(np.uint8)
    cv2.imwrite(f'{imagename}_ATTENTION.bmp', markplate)


def main():
    global shifted_mask, shifted_pan
    MASK = cv2.imread(MASK_path, 0)
    PAN = cv2.imread(PAN_path, 0)

    sys.stdout.write(f'{1:2d}\r')
    sys.stdout.flush()

    MASK, PAN = equalize(MASK, PAN)

    corrected = correctAngleProjection(PAN, 0.25, 0.01)
    cv2.imwrite('./skew_corrected.jpg', corrected)

    PAN = invertBW(corrected)
    cv2.imwrite('./PAN_inverted.jpg', PAN)

    PAN = cv2.imread(CORRECTED_path, 0)
    MASK, PAN = equalize(MASK, PAN)

    sys.stdout.write(f'{2:2d}\r')
    sys.stdout.flush()

    MASK_sh, fshift = align((255 - PAN), (255 - MASK), 5)
    cv2.imwrite(f'./shiftedMASK[{fshift}].jpg', MASK_sh)
    shifted_mask = f'./shiftedMASK[{fshift}].jpg'

    differences = [[PAN, MASK_sh, 0, ''], [PAN, MASK_sh, 1, ''], [PAN, MASK_sh, 2, ''],
                   [PAN, MASK_sh, 4, '']]

    sys.stdout.write(f'{3:2d}\r')
    sys.stdout.flush()

    pool = multiprocessing.Pool(4)
    pool.map(diffwrap, differences)
    pool.close()

    PAN_sh, fshift = align((255 - MASK), (255 - PAN), 5)
    cv2.imwrite(f'./shiftedPAN[{fshift}].jpg', PAN_sh)
    shifted_pan = f'./shiftedPAN[{fshift}].jpg'

    differences = [[MASK, PAN_sh, 0, '.MASK_FIRST'], [MASK, PAN_sh, 1, '.MASK_FIRST'],
                   [MASK, PAN_sh, 2, '.MASK_FIRST'], [MASK, PAN_sh, 4, '.MASK_FIRST']]
    
    sys.stdout.write(f'{4:2d}\r')
    sys.stdout.flush()
    pool = multiprocessing.Pool(4)
    pool.map(diffwrap, differences)
    pool.close()

    # print('Starting comparison\r')
    compares = [[1, 'COMPARISON'], [2, 'COMPARISON_2'], [4, 'COMPARISON_4'], [0, 'COMPARISON_0']]

    sys.stdout.write(f'{5:2d}\r')
    sys.stdout.flush()
    pool = multiprocessing.Pool(4)
    pool.map(comparison, compares)
    pool.close()

    # comparison(1)
    # comparison(2, 'COMPARISON_2')
    # comparison(4, 'COMPARISON_4')
    # comparison(0, 'COMPARISON_0')

    # print('Looking for missing parts\r')
    missings = [[1, 'COMPARISON_MASK'], [2, 'COMPARISON_MASK_2'], [4, 'COMPARISON_MASK_4'], [0, 'COMPARISON_MASK_0']]

    sys.stdout.write(f'{6:2d}\r')
    sys.stdout.flush()
    pool = multiprocessing.Pool(4)
    pool.map(missing, missings)
    pool.close()

    # missing(1)
    # missing(2, 'COMPARISON_MASK_2')
    # missing(4, 'COMPARISON_MASK_4')
    # missing(0, 'COMPARISON_MASK_0')

    # print('Filtering noise\r')
    blobs = [['COMPARISON_MASK', 1, 0], ['COMPARISON', 2, 0]]

    sys.stdout.write(f'{7:2d}\r')
    sys.stdout.flush()
    pool = multiprocessing.Pool(4)
    pool.map(isoblob, blobs)
    pool.close()

    sys.stdout.write(f'{8:2d}\r')
    sys.stdout.flush()
    # print('Finished work\r')
    # isoblob('COMPARISON_MASK', 1, 0)
    # isoblob('COMPARISON', 2, 0)


if __name__ == '__main__':
    main()
