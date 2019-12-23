import cv2
import numpy as np
font =cv2.FONT_HERSHEY_COMPLEX
nrEstrellas=0
nrOcho=0
nrFigT=0

def start(path_img):
    font =cv2.FONT_HERSHEY_COMPLEX
    nrEstrellas=0
    nrOcho=0
    nrFigT=0
    imgn = cv2.imread(path_img)
    img=cv2.resize(imgn,(640,480))

    gris=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    _,th=cv2.threshold(gris,240,255,cv2.THRESH_BINARY_INV)

    cnts,_ =cv2.findContours(th,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    circles=cv2.HoughCircles(gris,cv2.HOUGH_GRADIENT,1,50,param1=50,param2=30,minRadius=0,maxRadius=0)
    circles=np.uint16(np.around(circles))
    for i in circles[0,:]:
        cv2.circle(gris,(i[0],i[1]),i[2],(0,255,0),2)
        cv2.circle(gris,(i[0],i[1]),2,(0,0,255),3)
        #cv2.imshow('circulos',gris)

    #cv2.drawContours(img,cnts,-1,(255,0,0),2)
    #print('contornos',len(cnts))
    #cv2.imshow('compuestas',img)
    #cv2.imshow('th',th)
    #cv2.waitKey(0)
    print('nro contornos:',len(cnts))
    for c in cnts:
        M=cv2.moments(c)
        approx=cv2.approxPolyDP(c,0.01*cv2.arcLength(c,True),True)
        x=approx.ravel()[0]
        y=approx.ravel()[1]

        if len(approx)==10:
            cv2.putText(img,"estrella",(x,y), font,0.4,(0))
            nrEstrellas=nrEstrellas+1
        elif len(approx)==8:
            cv2.putText(img,"figura T",(x,y), font,0.4,(0))
            nrFigT= nrFigT+1
        elif len(approx)==16:        
            cv2.putText(img,"figura 8",(x,y), font,0.4,(0))
            nrOcho=nrOcho+1
        print(len(approx))
        cv2.drawContours(img,[approx],0,(0,0,0),2)
    #cv2.drawContours(img,cnts,-1,(0,0,0),2)
    cv2.imshow('imagen',img)
    #  print('m', M)
    #    print("cantidad de Figuras estrellas: ", nrEstrellas)
    #   print("cantidad de Figuras Ocho: ", nrOcho)
    #  print("cantidad de Figuras T: ", nrFigT)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    