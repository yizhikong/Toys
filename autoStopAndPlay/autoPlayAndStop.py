import cv2
import time
import numpy as np
import math
import win32api
import win32con

class sigmoid(object):
    def __init__(self, weight):
        self.weight = weight.copy()

    def output(self, data):
        dotRes = self.weight.dot(data)
        return 1 / (1 + math.exp(-dotRes))

class BPnet(object):
    def __init__(self, filename, n_hidden, n_out):
        self.hidden = []
        self.out = []
        f = open(filename, "r")
        for h in range(n_hidden):
            weight = f.readline().strip().split(" ")
            self.hidden.append(sigmoid(np.array(weight, dtype="float")))
        for o in range(n_out):
            weight = f.readline().strip().split(" ")
            self.out.append(sigmoid(np.array(weight, dtype="float")))

    def output(self, image):
        outputOfHidden = []
        for h in self.hidden:
            outputOfHidden.append(h.output(image))
        outputOfHidden = np.array(outputOfHidden)
        finalOutput = []
        for o in self.out:
            finalOutput.append(o.output(outputOfHidden))
        if finalOutput[1] > finalOutput[0]:
            return 1
        else:
            return 0

if __name__ == "__main__":
    net = BPnet("net.txt", 26, 2)
    # open the camera
    cap = cv2.VideoCapture(0)
    print cap.isOpened()
    status = "looking"
    while True:
        # take a photo
        result, image = cap.read()
        height, width, depth = image.shape
        # resize it
        image = cv2.resize(image, (32, 24))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # deal with the pixel, make it as the input of BPnet
        pixel = []
        heigh, width = gray.shape
        gray = gray / 255.0
        for h in range(heigh):
            for w in range(width):
                pixel.append(gray[h][w])

        # check the status and take action
        if net.output(np.array(pixel, dtype="float")):
            if status != "looking":
                status = "looking"
                # press space to continue playing
                win32api.keybd_event(32,0,0,0)
            print "looking"
        else:
            if status != "not looking":
                status = "not looking"
                # press space to stop playing
                win32api.keybd_event(32,0,0,0)
            print "not looking"