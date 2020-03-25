import cv2
import difflib
import os
import numpy as np
#import cbr as cb
#Функция вычисления хэша
def CalcImageHash(image,width,height):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #Переведем в черно-белый формат
    avg=gray_image.mean() #Среднее значение пикселя
    ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0) #Бинаризация по порогу
    
    #Рассчитаем хэш
    _hash=""
    for x in range(width):
        for y in range(height):
            val=threshold_image[y,x]
            if val==255:
                _hash=_hash+"1"
            else:
                _hash=_hash+"0"
            
    return _hash

def CornerCount(image):
    operatedImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
  
# изменить тип данных
# установка 32-битной плавающей запятой
    operatedImage = np.float32(operatedImage) 
  
# применить метод cv2.cornerHarris
# для определения углов с соответствующими
# значения в качестве входных параметров
    dest = cv2.cornerHarris(operatedImage, 2, 1, 0.05) 
  
# Результаты отмечены через расширенные углы
    dest = cv2.dilate(dest, None)
    corners = 0
    maximum = dest.max()
    for ap in dest:
        for bp in ap:
            if bp > 0.9 * maximum:
                corners = corners + 1
    return corners

def img_cropper(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #Переведем в черно-белый формат
    avg=gray_image.mean() #Среднее значение пикселя
    ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0) #Бинаризация по порогу
    width=image.shape[1]
    height=image.shape[0]
    for y in range(height):
        for x in range(width):
            val=threshold_image[y,x]
            if val<255:
                break
        if val<255:
            break
    for h in reversed(range(height)):
        for w in reversed(range(width)):
            val=threshold_image[h,w]
            if val<255:
                break
        if val<255:
            break
    for x in range(width):
        for y1 in range(height):
            val=threshold_image[y1,x]
            if val<255:
                break
        if val<255:
            break
    for w in reversed(range(width)):
        for h1 in reversed(range(height)):
            val=threshold_image[h1,w]
            if val<255:
                break
        if val<255:
            break   
    return image[y:h,x:w]
def CompareHash(hash1,hash2):
    l=len(hash1)
    i=0
    count=0
    while i<l:
        if hash1[i]!=hash2[i]:
            count=count+1
        i=i+1
    return count
width=100
height=100
reals=[]
forges=[]
for root, dirs, files in os.walk("scr/msgn"):  
    for filename in files:
        reals.append("scr/msgn/" + filename)
for a in reals:
    for b in reals:
        if a!=b:
            pic1=cv2.imread(a) #Прочитаем картинку
            pic2=cv2.imread(b) #Прочитаем картинку
            pic1 = cv2.resize(img_cropper(pic1), (width,height), interpolation = cv2.INTER_AREA) #Уменьшим картинку
            pic2 = cv2.resize(img_cropper(pic2), (width,height), interpolation = cv2.INTER_AREA) #Уменьшим картинку
            hash1=CalcImageHash(pic1,width,height)
            hash2=CalcImageHash(pic2,width,height)
            print(a+ " " + b)
            #print(hash1)
            #print(hash2)
            print(str(CompareHash(hash1, hash2))+"| "+ str(CornerCount(pic1))+"| "+str(CornerCount(pic2)))
cv2.imshow('Image with Borders', pic1)
if cv2.waitKey(0) & 0xff == 27: 
    cv2.destroyAllWindows() 
