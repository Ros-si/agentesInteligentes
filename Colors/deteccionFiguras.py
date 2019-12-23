import cv2
import numpy as np
import math

    #rojo
rojoBajo1 = np.array([0, 100, 20], np.uint8)
rojoAlto1 = np.array([10, 255, 255], np.uint8)
rojoBajo2 = np.array([175, 100, 20], np.uint8)
rojoAlto2 = np.array([180, 255, 255], np.uint8)

    #naranja
naranjaBajo = np.array([11, 100, 20], np.uint8)
naranjaAlto = np.array([19, 255, 255], np.uint8)

    #amarillo
amarilloBajo = np.array([20, 100, 20], np.uint8)
amarilloAlto = np.array([32, 255, 255], np.uint8)

    #Verde
verdeBajo = np.array([36, 100, 20], np.uint8)
verdeAlto = np.array([70, 255, 255], np.uint8)

    #Violeta 
violetaBajo = np.array([130, 100, 20], np.uint8)
violetaAlto = np.array([145, 100, 255], np.uint8)

    #Rosado
rosaBajo = np.array([146, 100, 20], np.uint8)
rosaAlto = np.array([170, 255, 255], np.uint8)

def start(path_img):
    image = cv2.imread(path_img)

    w, h = image.shape[:2]
    scala = 600 / w
    w = round(w * scala)
    h = round(h * scala)
    image = cv2.resize(image,(h, w))

    imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    grises = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    canny = cv2.Canny(grises, 10, 150)
    canny = cv2.dilate(canny, None, iterations=1)
    canny = cv2.erode(canny, None, iterations=1)

    _,th=cv2.threshold(grises,240,255,cv2.THRESH_BINARY_INV)

    cnts,_ =cv2.findContours(th,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    #cnts,_ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print('tamanio', len(cnts))
    cv2.drawContours(image, cnts, -1,(0, 0, 0),2)
    print("Numeros de contornos encontrados: ", len(cnts))

    for c in cnts:
    # print(str(c) +"\t valor de c")
        epsilon = 0.015*cv2.arcLength(c, True)
        #print(str(cv2.arcLength(c, True)))
        approx = cv2.approxPolyDP(c, epsilon, True)
        #print(str(len(approx)) +"\t Vertice")
        x, y, w, h =cv2.boundingRect(approx)
        cv2.drawContours(image,[approx],0,(255,105,180),3)

        #triangulo
        if len(approx) == 3:
            cv2.putText(image, "Triangulo", (x, y-5), 1, 1,(0, 0, 50), 2)

        #cuadrado
        if len(approx) == 4:
            aspect_ratio = float(w)/h
            #print("El aspect_ratio= ",aspect_ratio)
            if aspect_ratio >=1.0 and aspect_ratio <= 1.089:
                cv2.putText(image, "Cuadrado", 	(x, y-5), 1, 1,(0,0,50), 2)[1]
            
            else: 
                cv2.putText(image, "Rectangulo", (x ,y-5), 1, 1,( 0, 0, 50), 2)
        
        #Circulo
        vert = len(approx)
        if vert >= 8 and vert != 10:
            if (int(math.floor(w/10)) == int(math.floor(h/10))):
                cv2.putText(image, "Circulo", (x, y-5),1 ,1,(0, 0, 50), 2)	

    #Muestra las mascaras de los colores buscados
    maskRojo1 = cv2.inRange(imageHSV, rojoBajo1, rojoAlto1)
    maskRojo2 = cv2.inRange(imageHSV, rojoBajo2, rojoAlto2)
    maskRojo = cv2.add(maskRojo1, maskRojo2)
    cnts,_ = cv2.findContours(maskRojo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print('tamanio colores de figuras en Rojo: ', len(cnts))
    maskNaranja = cv2.inRange(imageHSV, naranjaBajo, naranjaAlto)
    cnts,_ = cv2.findContours(maskNaranja, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print('tamanio colores de figuras en Naranja', len(cnts))
    maskAmarillo =cv2.inRange(imageHSV, amarilloBajo, amarilloAlto)
    cnts,_ = cv2.findContours(maskAmarillo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print('tamanio  colores de figuras en Amarillo', len(cnts))
    maskVerde = cv2.inRange(imageHSV, verdeBajo, verdeAlto)
    cnts,_ = cv2.findContours(maskVerde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print('tamanio colores de figuras en Verde ', len(cnts))
    maskVioleta = cv2.inRange(imageHSV, violetaBajo, violetaAlto)
    cnts,_ = cv2.findContours(maskVioleta, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print('tamanio colores de figuras en  Violeta', len(cnts))
    maskRosa = cv2.inRange(imageHSV, rosaBajo, rosaAlto)
    cnts,_ = cv2.findContours(maskRosa, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print('tamanio colores de figuras en Rosa', len(cnts))

    contornosAmarillo = cv2.findContours(maskAmarillo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]

    cv2.imshow(	"IMAGEN ORIGINAL", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
