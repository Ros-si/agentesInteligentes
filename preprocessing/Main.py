import cv2
import Client
import threading
import read_video

x = threading.Thread(target=Client.start_connection)
x.start()

imagen = cv2.imread("../img/figura1.jpg")
w, h = imagen.shape[:2]
scala = 600 / w
w = round(w * scala)
h = round(h * scala)
bgr = cv2.resize(imagen,(h, w))
cv2.imwrite("../img/figura.jpg", bgr)

Client.refresh()