import cv2
import CompareImage
import os 
import glob 
import Client
import threading

Client.start_connection


files = glob.glob('img_video/*') 
for f in files: 
    os.remove(f)


vidcap = cv2.VideoCapture('video.mp4')

def comparar(img1,img2,img_out):
    image_difference = CompareImage.compare_image(img1,img2)
    if( image_difference > 0.006):
        img_out = img_out[:, 240:-240]
        path = "../img/image"+str(count)+".jpg"
        cv2.imwrite(path, img_out)
        print(path) 
        x = threading.Thread(target=Client.refresh(path))
        x.start()

def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        cv2.imwrite("img_video/image"+str(count)+".jpg", image)     # save frame as JPG file
        imgae2 = image[0:127, 240:381] 
        cv2.imwrite("img_video/image"+str(count)+".0.jpg", imgae2)  
        if(count > 1):
            comparar("img_video/image"+str(count-1)+".0.jpg","img_video/image"+str(count)+".0.jpg",image)
        else:
            image = image[:, 240:-240]
            path = "../img/image"+str(count)+".jpg"
            cv2.imwrite(path, image) 
            print(path) 
            x = threading.Thread(target=Client.refresh(path))
            x.start()
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

