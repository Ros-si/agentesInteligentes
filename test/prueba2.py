import cv2
import numpy as np
from PIL import ImageChops
import CompareImage

vidcap = cv2.VideoCapture('video.mp4')

def comparar(img1, img2):
    #diferencia = cv2.subtract(img1,img2)
    picture1_norm = img1/np.sqrt(np.sum(img1**2))
    picture2_norm = img2/np.sqrt(np.sum(img2**2))
    diferencia = np.sum(picture2_norm*picture1_norm)
    #if( not np.any(diferencia)):
    print(diferencia)
    if( diferencia == 1.0):
        print("Son iguales")
    else:
        print("Son distintas")
def comparar2(img1,img2,img22):
    image_difference = CompareImage.compare_image(img1,img2)
    #print (image_difference)
    if( image_difference > 0.006):
        image1 = cv2.imread(img2)
        cv2.imwrite("../img/image"+str(count)+".jpg", img22) 
        print("Son distintas")
    #else:
    #    print("Son iguales")

def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if(count == 1):
        cv2.imwrite("../img/image"+str(count)+".jpg", image) 
    if hasFrames:
        cv2.imwrite("img_video/image"+str(count)+".jpg", image)     # save frame as JPG file
        imgae2 = image[0:127, 240:381] 
        cv2.imwrite("img_video/image"+str(count)+".0.jpg", imgae2)  
        if(count > 1):
            image1 = cv2.imread("img_video/image"+str(count-1)+".0.jpg")
            diff_total = cv2.absdiff(image1, imgae2)
            #if(np.sum())
            comparar2("img_video/image"+str(count-1)+".0.jpg","img_video/image"+str(count)+".0.jpg",image)
    return hasFrames
sec = 0
frameRate = 0.5 #//it will capture image in each 0.5 second
count=1
success = getFrame(sec)
while success:
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)

