# Казарян М.М., ВКБ23, Определение хозяина подписи
import cv2, os, numpy as np
#from matplotlib import pyplot as plt
k=200
def CalcImageHash(image):
    global k
    '''Вычисление хэша'''
    tohash = cv2.resize(image,(k,k))
    threshold_image = binarize(tohash)
    # Рассчитаем хэш
    _hash = ""
    for x in range(k):
        for y in range(k):
            val = threshold_image[y, x]
            if val == 255:
                _hash = _hash + "1"
            else:
                _hash = _hash + "0"

    return _hash

def CompareHash(hash1, hash2):
    '''Сравнение хэшей'''
    l = len(hash1)
    i = 0
    count = 0
    while i < l:
        if hash1[i] != hash2[i]:
            count = count + 1
        i = i + 1
    return 1-count/k**2

def pic_normalize(img):
    b = binarize(img)
    m = cv2.moments(cv2.bitwise_not(b), 1)
    c_p=(int(m['m10']/m['m00']),int(m['m01']/m['m00']))
    #cv2.circle(img,c_p,2,(0,0,255),-1)
    x = [c_p[0] for e in range(4)]
    y = [c_p[1] for e in range(4)]
    xe = [c_p[0] for e in range(4)]
    ye = [c_p[1] for e in range(4)]
    dist= 0
    for xp in reversed(range(c_p[0])):
        for yp in reversed(range(c_p[1])):  # отступ от центра к лв краю
            dst = dist_btw_pts((xp,yp),c_p)
            if dst>dist and (b[yp,xp]==0):
                dist = dst
                x[0]=xp; y[0]=yp
    dist = 0
    for xp in range(c_p[0],img.shape[1]):
        for yp in reversed(range(c_p[1])):  # отступ от центра к пв краю
            dst = dist_btw_pts((xp, yp), c_p)
            if dst > dist and (b[yp, xp] == 0):
                dist = dst
                x[1] = xp; y[1] = yp
    dist = 0
    for xp in reversed(range(c_p[0])):
        for yp in range(c_p[1],img.shape[0]):  # отступ от центра к лн краю
            dst = dist_btw_pts((xp, yp), c_p)
            if dst > dist and (b[yp, xp] == 0):
                dist = dst
                x[2] = xp; y[2] = yp
    dist = 0
    for xp in range(c_p[0],img.shape[1]):  # отступ от центра к пн краю
        for yp in range(c_p[1],img.shape[0]):
            dst = dist_btw_pts((xp,yp),c_p)
            if dst>dist and (b[yp,xp]==0):
                dist = dst
                x[3]=xp; y[3]=yp




    for yp in range(img.shape[0]):  # первая точка от лв
        for xp in range(img.shape[1]):
            if b[yp, xp] == 0:
                break
        if b[yp,xp]==0:
            break
    xe[0]=xp; ye[0]=yp
    for yp in reversed(range(img.shape[0])):  # первая точка от лв
        for xp in range(img.shape[1]):
            if b[yp, xp] == 0:
                break
        if b[yp,xp]==0:
            break
    xe[3]=xp; ye[3]=yp
    for xp in range(img.shape[1]):  # первая точка от лв
        for yp in range(img.shape[0]):
            if b[yp, xp] == 0:
                break
        if b[yp,xp]==0:
            break
    xe[2]=xp; ye[2]=yp
    for xp in reversed(range(img.shape[1])):  # первая точка от лв
        for yp in range(img.shape[0]):
            if b[yp, xp] == 0:
                break
        if b[yp,xp]==0:
            break
    xe[1]=xp; ye[1]=yp


    for xp,yp in zip(x,y):
        cv2.circle(img, (xp,yp), 3, (255, 0, 0), -1)
    pts1 = np.float32([[xp,yp] for xp,yp in zip(x,y)])
    pts2 = np.float32([[0,0],[img.shape[1],0],[0,img.shape[0]], [img.shape[1],img.shape[0]]])
    mper = cv2.getPerspectiveTransform(pts1,pts2) #Строим матрицу перехода
    return cv2.warpPerspective(img,mper,(img.shape[1],img.shape[0]))
def dist_btw_pts(p1,p2):
    return (np.power(np.abs(p1[0]-p2[0]),2) + np.power(np.abs(p1[1]-p2[1]),2))

def binarize(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Переведем в черно-белый формат
    avg = gray_image.mean() / 1.1  # Среднее значение (с отклонением) пикселя
    ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)  # Бинаризация по порогу
    return threshold_image

def accuum_hashes():
    b={}
    signs_db_path = "scr/real"
    for root, dirs, files in os.walk(signs_db_path):  # Пути к файлам из базы
        for i,filename in enumerate(files):
            b.update({filename[:5]: CalcImageHash(pic_normalize(cv2.imread(signs_db_path + "/" + filename)))})
            print("Накопление хэшей...{}%".format(int((i+1)/len(files)*100)),end='\r')
    print("\nХэши загружены")
    return b

def accuum_HuMoments():
    b={}
    signs_db_path = "scr/real"
    for root, dirs, files in os.walk(signs_db_path):  # Пути к файлам из базы
        for i,filename in enumerate(files):
            mom=cv2.HuMoments(cv2.moments(cv2.bitwise_not(binarize(cv2.resize(img_cropper(cv2.imread(signs_db_path + "/" + filename)), (k, k))))))
            mom = -1 * np.copysign(1.0, mom) * np.log10(abs(mom))
            b.update({filename[:5]: mom})
            print("Накопление моментов...{}%".format(int((i+1)/len(files)*100)),end='\r')
    print("\nМоменты загружены")
    return b

def compare(bim1,bim2):
    w, h = bim1.shape[::-1]
    sz=10
    k=0
    for x in range(0,w-sz,sz):
        for y in range(0,h-sz,sz):
            part=bim1[x:x+sz,y:y+sz]
            if 0 not in part:
                continue
            #cv2.imshow('cus', part)
            #if cv2.waitKey(0) & 0xff == 27:
            #    cv2.destroyAllWindows()
            wp, hp = part.shape[::-1]
            res = cv2.matchTemplate(bim2,part,cv2.TM_SQDIFF)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
            if (minLoc[0]+sz<=w and minLoc[1]+sz<=h and abs(minVal)<10):
                k+=1
    return k/(sz**2)
def accuum_contours():
    b={}
    signs_db_path = "scr/real"
    for root, dirs, files in os.walk(signs_db_path):  # Пути к файлам из базы
        for filename in files:
            contours, hierarchy = cv2.findContours(cv2.bitwise_not(binarize(cv2.imread(signs_db_path + "/" + filename))), 2, 1)
            b.update({filename[:5]: contours[0]})
    return b
def horlinecheck(img):
    binr = binarize(img)
    curcol=255-binr[0,0]
    k=0
    tmp=0
    line=0
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            if (binr[y,x]!=curcol) and (binr[y,x]<255):
                k+=1
            curcol=binr[y,x]
        if k>tmp:
            line=y
            tmp=k
        k=0
    cv2.line(img,(0,line),(img.shape[1],line),(128,0,0),1)
    return tmp
def peaks_count(img):
    '''Подсчёт вершин у подписи'''
    bimg=binarize(img)
    verhs=[]
    tmp=[0,bimg.shape[0]+1]
    prev = [0,bimg.shape[0]+1]
    sost=[1,1]
    for x in range(bimg.shape[1]):
        for y in range(bimg.shape[0]):
            if (bimg[y,x]==0):
                sost[1] = sost[0]
                if (y<prev[1]):
                    sost[0]=1
                elif (y==prev[1]):
                    sost[0]=0
                elif (y>prev[1]):
                    sost[0]=-1
                if (sost[0]==-1) and (sost[1]>-1):
                    verhs.append((prev[0], prev[1]))
                prev = [x, y]
                break
    for p in verhs:
        cv2.circle(img,p, 3, (0, 0, 255), -1)
    print(verhs)
    print(len(verhs))
    return img
def accuum_horlines():
    global k
    b = {}
    signs_db_path = "scr/real"
    for root, dirs, files in os.walk(signs_db_path):  # Пути к файлам из базы
        for i,filename in enumerate(files):
            b.update({filename[:5]: horlinecheck(cv2.imread(signs_db_path + "/" + filename))})
            print("Поиск пересечений с горизонтальной линией ...{}%".format(int((i+1) / len(files) * 100)), end='\r')
    return b
def cornercount(img):
    gray = binarize(img)
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)

    # result is dilated for marking the corners, not important
    dst = cv2.dilate(dst, None)

    # Threshold for an optimal value, it may vary depending on the image.
    max=dst.max()
    for cr in range(img.shape[1]):
        for cc in range(img.shape[0]):
            if dst[cc,cr] > 0.01 * max:
                cv2.circle(gray, (cr, cc), 3, (128, 0, 0), -1)
    #cv2.imshow('dst', gray)
    #if cv2.waitKey(0) & 0xff == 27:
    #    cv2.destroyAllWindows()
def skeletonization(img):
    img = cv2.resize(img,(img.shape[1]*4,img.shape[0]*4))
    img = cv2.bitwise_not(img)
    kernel = np.ones((2, 2), np.uint8)
    tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
    erosion = cv2.erode(img, kernel, iterations=1)
    erosion = cv2.bitwise_not(tophat)
    #cv2.imshow("skel", erosion)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

def img_cropper(image):
    '''Кадрирование изображения'''
    threshold_image = binarize(image)
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
def in_crop_col_points(bimg):
    '''Поиск точек касания на обрезаном изображении'''
    width = bimg.shape[1]
    height = bimg.shape[0]
    xtm=True
    xbm=True
    for c in range(width):
        if xtm and bimg[0,c]==0:
            xtm=False
            xtp=c
        if xbm and bimg[height-1,width-c-1]==0:
            xbm=False
            xbp=width-c
    xtm = True
    xbm = True
    for c in range(height):
        if xtm and bimg[height-c-1,0]==0:
            xtm=False
            ylp=height-c
        if xbm and bimg[c,width-1]==0:
            xbm=False
            yrp=c
    return [[xtp,0],[width,yrp],[0,ylp],[xbp,height]]
def rt(img):
    pic=img.copy()
    cnst=int(np.sqrt(pic.shape[1]*pic.shape[0])/5)
    kernel = np.ones((cnst, cnst), np.uint8)
    cnt, _ = cv2.findContours(cv2.morphologyEx(cv2.bitwise_not(binarize(pic)), cv2.MORPH_CLOSE, kernel), 1, 1)
    cont=cnt[0]
    x, y, w, h = cv2.boundingRect(cont)
    cv2.rectangle(pic, (x, y), (x + w, y + h), (0, 255, 0), 2)
    rect = cv2.minAreaRect(cont)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    print(box)
    cv2.drawContours(pic, [box], 0, (0, 0, 255), 2)
    return pic#cv2.morphologyEx(cv2.bitwise_not(binarize(pic)), cv2.MORPH_CLOSE, kernel)

def transform(img,ps):
    pts= np.float32(ps)
    ptsn= np.float32([[img.shape[1]/2,0],[img.shape[1],0],[0,img.shape[0]], [img.shape[1],img.shape[0]]])
    mper = cv2.getPerspectiveTransform(pts, ptsn)  # Строим матрицу перехода
    return cv2.warpPerspective(img, mper, (img.shape[1], img.shape[0]))

def cmp_all(pic):
    global k;
    b = {}
    img = cv2.resize(img_cropper(pic), (k, k))
    signs_db_path = "scr/real"
    for root, dirs, files in os.walk(signs_db_path):  # Пути к файлам из базы
        for i,filename in enumerate(files):
            b.update({filename[:5]: compare(binarize(img),binarize(cv2.resize(img_cropper(cv2.imread(signs_db_path + "/" + filename)), (k, k))))})
            print("Фрагментарное сравнение...{}%".format(int((i+1) / len(files) * 100)), end='\r')
    print("\nФрагменты загружены")
    return b
def dict_max_sort(dict):
    maximum=0
    ndict={}
    prevkey=''
    for key in dict:
        if (key[:3]==prevkey[:3]) or (prevkey==''):
            if dict[key]>0:
                maximum=dict[key]
        elif key[:3]!=prevkey[:3]:
            ndict.update({prevkey[:3]:maximum})
            maximum=0
        prevkey = key
    ndict.update({prevkey[:3]: maximum})
    return ndict
def owner_show(OwID):
    '''Расшифровка ID'''
    if os.path.exists("scr/key.txt"):
        OwKey = {}
        f = open('scr/key.txt', 'r', encoding='utf-8')
        for line in f:
            line = line.replace('\n', '').split(':')
            OwKey.update({line[0]: line[1]})
        f.close()
        val = OwKey.get(OwID)
        print("Расшифровка загружена успешно")
        if val == None:
            print("Данный id не содержится в расшифровке")
            return OwID
        else:
            return val
    else:
        return val
        
def verify(img,signlocind):
    global k;
    #img2 = cv2.imread('scr/real/00801008.png')
    #cv2.imshow('pic',rt(img))
    #cv2.imshow('pic2',rt(img2))
    g=cv2.resize(img_cropper(img),(k,k))
    #g2=cv2.resize(img_cropper(img2),(k,k))
    matches=cmp_all(img)
    pic=pic_normalize(img)
    #pic2=pic_normalize(img2)
    mom=cv2.HuMoments(cv2.moments(cv2.bitwise_not(binarize(g))))
    mom=-1* np.copysign(1.0, mom) * np.log10(abs(mom))
    horl=horlinecheck(img)
    cv2.waitKey()
    cv2.destroyAllWindows()
    hashes=accuum_hashes()
    HuMoments=accuum_HuMoments()
    Horls=accuum_horlines()
    contour,h= cv2.findContours(cv2.bitwise_not(binarize(img)),2,1)
    hof=CalcImageHash(pic)
    
    for key in hashes:
        hashes.update({key:CompareHash(hof, hashes.get(key))})
        HuMoments.update({key: 1 / (cv2.matchShapes(mom, HuMoments.get(key), cv2.CONTOURS_MATCH_I1, 0) + 1)})
        Horls.update({key:1/(np.sqrt(abs(horl-Horls[key])+1))})
        
    matches = dict_max_sort(matches)
    hashes=dict_max_sort(hashes)
    HuMoments=dict_max_sort(HuMoments)
    Horls=dict_max_sort(Horls)
    
    print('matches=',matches)
    print('hashes=',hashes)
    print('HuMoments=',HuMoments)
    print('Horlines=',Horls)
    newdict={key: matches[key]*5+hashes[key]+HuMoments[key]/2+Horls[key]/2 for key in hashes}
    print('result=',newdict)
    ko=''
    P=0
    
    for key in newdict:
        if P<newdict[key]:
            P=newdict[key]
            ko=key
            
    print(ko,' ',P)
    OWNER = owner_show(ko)
    print("Хозяин подписи {}: {}".format(signlocind, OWNER))
    return (signlocind, OWNER)
#verify(cv2.imread('scr/STI/3.png'),'sign1')