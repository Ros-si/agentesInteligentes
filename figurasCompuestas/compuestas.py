import cv2
font =cv2.FONT_HERSHEY_COMPLEX
imgn =cv2.imread('figuras.jpg')
img=cv2.resize(imgn,(640,480))

gris=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
_,th=cv2.threshold(gris,240,255,cv2.THRESH_BINARY_INV)

_,cnts,_=cv2.findContours(th,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


#cv2.drawContours(img,cnts,-1,(255,0,0),2)
#print('contornos',len(cnts))
#cv2.imshow('compuestas',img)
#cv2.imshow('th',th)
#cv2.waitKey(0)
print('nro contornos:',len(cnts))
for c in cnts:
    approx=cv2.approxPolyDP(c,0.01*cv2.arcLength(c,True),True)
    x=approx.ravel()[0]
    y=approx.ravel()[1]

    if len(approx)==10:
        cv2.putText(img,"ESTRELLA",(x,y), font,0.4,(0))
    elif len(approx)==8:
        cv2.putText(img,"figura T",(x,y), font,0.4,(0))
    elif len(approx)==16:
        cv2.putText(img,"figura 8",(x,y), font,0.4,(0))
    print(len(approx))
    cv2.drawContours(img,[approx],0,(0,0,0),2)
#cv2.drawContours(img,cnts,-1,(0,0,0),2)
    cv2.imshow('imagen',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()