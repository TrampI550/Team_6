import cv2
import numpy as np

colors_dict = {
    'Зелёный': {'min': 30, 'max': 85}, 'Зеленый': {'min': 30, 'max': 85},
    'Красный': {'min': 160, 'max': 180},
    'Оранжевый': {'min': 10, 'max': 25},
    'Жёлтый': {'min': 20, 'max': 40}, 'Желтый': {'min': 20, 'max': 40},
    'Голубой': {'min': 80, 'max': 110},
    'Синий': {'min': 100, 'max': 135},
    'Фиолетовый': {'min': 135, 'max': 160}
    }


def Negative_Filter(img):
    return cv2.bitwise_not(img)


def Gray_Filter(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def Mean_Shift_Filter(img):
    return cv2.pyrMeanShiftFiltering(img, 15, 50, 1)


def Color_Range_Filter(img, color: str):
    # img = cv2.bilateralFilter(img,9,151,151)
    for i in range(2):
        img = cv2.bilateralFilter(img, 9, 75, 75)
    hsv_min = np.array((colors_dict[color]['min'], 100, 20), np.uint8)
    hsv_max = np.array((colors_dict[color]['max'], 255, 255), np.uint8)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_res = cv2.inRange(hsv, hsv_min, hsv_max)
    return img_res


def Gamma_Num(num):
    return float(num)


def Gamma_Filter(img, gamma: float):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(img, table)


def Pixel_Filter(img):
    orig_height, orig_width = img.shape[:2]
    small_height, small_width = orig_height // 4, orig_width // 4
    img_res = cv2.resize(img, (small_width, small_height), interpolation=cv2.INTER_LINEAR)
    data = img_res.reshape((-1, 3))
    data = np.float32(data)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness, labels, centers = cv2.kmeans(data, 20, None, criteria, 10, flags)
    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    img_res = res.reshape(img_res.shape)
    img_res = cv2.resize(img_res, (orig_width, orig_height), interpolation=cv2.INTER_NEAREST)
    return img_res


if __name__ == '__main__':
    pass

