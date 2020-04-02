import cv2
import difflib
import os
import numpy as np


# import cbr as cb
# Функция вычисления хэша
def CalcImageHash(image):
    '''Вычисление хэша'''
    width = image.shape[1]
    height = image.shape[0]
    threshold_image = binarize(image, 1)

    # Рассчитаем хэш
    _hash = ""
    for x in range(width):
        for y in range(height):
            val = threshold_image[y, x]
            if val == 255:
                _hash = _hash + "1"
            else:
                _hash = _hash + "0"

    return _hash


def CornerCount(image):
    '''Подсчёт углов'''
    operatedImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # изменить тип данных
    # установка 32-битной плавающей запятой
    operatedImage = np.float32(operatedImage)

    # применить метод cv2.cornerHarris
    # для определения углов с соответствующими
    # значения в качестве входных параметров
    dest = cv2.cornerHarris(operatedImage, 3, 23, 0.04)

    # Результаты отмечены через расширенные углы
    dest = cv2.dilate(dest, None)
    corners = 0
    maximum = dest.max()
    for ap in dest:
        for bp in ap:
            if bp > 0.1 * maximum:
                corners = corners + 1
    return corners


def binarize(image, koef):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Переведем в черно-белый формат
    avg = gray_image.mean() / koef  # Среднее значение (с отклонением) пикселя
    ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)  # Бинаризация по порогу
    return threshold_image


def img_cropper(image):
    '''Кадрирование изображения'''
    threshold_image = binarize(image, koef)
    width = image.shape[1]
    height = image.shape[0]
    for y in range(height):
        for x in range(width):
            val = threshold_image[y, x]
            if val < 255:
                break
        if val < 255:
            break
    for h in reversed(range(height)):
        for w in reversed(range(width)):
            val = threshold_image[h, w]
            if val < 255:
                break
        if val < 255:
            break
    for x in range(width):
        for y1 in range(height):
            val = threshold_image[y1, x]
            if val < 255:
                break
        if val < 255:
            break
    for w in reversed(range(width)):
        for h1 in reversed(range(height)):
            val = threshold_image[h1, w]
            if val < 255:
                break
        if val < 255:
            break
    return image[y:h, x:w]


def MatchesCounter(img1, img2):
    '''Подсчёт совпадающих пикселей(Размер картинок приведён к единому)'''
    mcnt = 0
    diffcnt = 0
    threshold_image = binarize(img1, koef)
    threshold_image_2 = binarize(img2, koef)
    for x in range(threshold_image.shape[1]):
        for y in range(threshold_image.shape[0]):
            if threshold_image[x, y] == 0 and threshold_image_2[x, y] == 0:
                mcnt = mcnt + 1
            if threshold_image[x, y] != threshold_image_2[x, y]:
                diffcnt = diffcnt + 1
    return (mcnt, diffcnt)  # /(threshold_image.shape[1]*threshold_image.shape[0])


def CompareHash(hash1, hash2):
    '''Сравнение хэшей'''
    l = len(hash1)
    i = 0
    count = 0
    while i < l:
        if hash1[i] != hash2[i]:
            count = count + 1
        i = i + 1
    return count


koef = 1.25
width = 100
height = 100
reals = []
forges = []
# msgn real
for root, dirs, files in os.walk("scr/real"):
    for filename in files:
        reals.append("scr/real/" + filename)
for a in reals[::5]:
    Matches = 0
    Diffs = width * height
    Mhash = Diffs
    OwnerId = 0
    tmp = 0
    thash = 0
    pic1 = cv2.imread(a)  # Прочитаем картинку
    pic1 = cv2.resize(img_cropper(pic1), (width, height), interpolation=cv2.INTER_AREA)  # Уменьшим картинку
    rex = reals.copy()
    rex.remove(a)
    for b in rex:
        pic2 = cv2.imread(b)  # Прочитаем картинку
        pic2 = cv2.resize(img_cropper(pic2), (width, height), interpolation=cv2.INTER_AREA)  # Уменьшим картинку
        tmp = MatchesCounter(pic1, pic2)
        hash1 = CalcImageHash(pic1)
        hash2 = CalcImageHash(pic2)
        thash = CompareHash(hash1, hash2)
        if thash < Mhash:
            Mhash = thash
            if tmp[0] > Matches:
                Matches = tmp[0]
                Diffs = width * height
                if tmp[1] < Diffs:
                    Diffs = tmp[1]
                    OwnerId = b.split("/")[-1][:3]
        print(a + " " + b)
        # print(hash1)
        # print(hash2)
        print("| Hash :" + str(thash) + "| Match: " + str(tmp[0]) + "| Diffs: " + str(tmp[1]) + "| Corners : " + str(
            CornerCount(pic1) - CornerCount(pic2)) + "|")
    print("| ExitParans  " + "| Hash :" + str(Mhash) + "| Match: " + str(Matches) + "| Diffs: " + str(Diffs) + "|")
    print("OwnerId:" + OwnerId)