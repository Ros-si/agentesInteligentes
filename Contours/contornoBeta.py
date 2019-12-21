import cv2
import numpy as np


def start():
    imagen = cv2.imread("../img/figura.jpg")
    w, h = imagen.shape[:2]
    scala = 600 / w
    w = round(w * scala)
    h = round(h * scala)
    blues = imagen[:,:,0]
    bgr = cv2.resize(imagen,(h, w))
    cv2.imwrite("./nuevo.jpg", bgr)
    grises = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    _,th =  cv2.threshold(grises, 200, 255, cv2.THRESH_BINARY_INV)

    th2 = np.uint8((( grises * (grises < 250) ) > 0) * 255 )

    _, th_blues = cv2.threshold(blues, 40, 200, cv2.THRESH_BINARY_INV)
    cv2.imshow('th', th2)
    cv2.waitKey(0)
    #Para OpenCV 3
    cnts,_ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #Para OpenCV 4
        #cnts,_ = cv2.findContours(th, cv2.RETR_EXTERNAL,
        #  cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(imagen, cnts, -1, (255,0,0),2)
        #print('Contornos: ', len(cnts))
    font = cv2.FONT_HERSHEY_SIMPLEX
    i=0
    for c in cnts:
        M=cv2.moments(c)
        if M["m00"] == 0: 
            M["m00"] = 1
        x=int(M["m10"]/M["m00"])
        y=int(M['m01']/M['m00'])
        mensaje = 'Num :' + str(i+1)
        cv2.putText(bgr,mensaje,(x-40,y),font,0.75,
            (255,0,0),2,cv2.LINE_AA)
        cv2.drawContours(bgr, [c], 0, (255,0,0),2)
        print(type(bgr))
        cv2.imshow('Imagen', bgr)
        if cv2.waitKey(0) == ord('q'):
            break
        i = i+1
    cv2.destroyAllWindows()