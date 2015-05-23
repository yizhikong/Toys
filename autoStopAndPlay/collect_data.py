import cv2
import time
# get the camera of the computer
cap = cv2.VideoCapture(0)
print cap.isOpened()
t = 500
while(t):
    t -= 1
    # take a photo
    ret, frame = cap.read()
    print ret
    height, width, depth = frame.shape
    # resize it and store it
    frame = cv2.resize(frame, (32, 24))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # you should not look at the screen while taking these photo
    # for getting looking photo, you should change the filename as "data/look"
    cv2.imwrite("data/notlook" + repr(t) + ".png", gray)
    # cv2.imwrite("data/look" + repr(t) + ".png", gray) ===========================>
    #time.sleep(2)