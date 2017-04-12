import cv2
import time
import numpy as np
import math
import win32api
import win32con

# a threadsold, make the program not easy to turn "looking" to "not looking"
ENSURE_COUNT = 4
LOOKING = 'looking'
NOT_LOOKING = 'not looking'

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
        return finalOutput[1] > finalOutput[0]

if __name__ == "__main__":
    net = BPnet("net.txt", 26, 2)
    # open the camera
    cap = cv2.VideoCapture(0)
    #print cap.isOpened()
    status = LOOKING
    counter = 0
    while True:
        # take a photo
        result, image = cap.read()
        height, width, depth = image.shape
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # gray = cv2.equalizeHist(gray)

        # deal with the pixel, make it as the input of BPnet
        gray = cv2.resize(gray, (32, 24))
        pixel = []
        heigh, width = gray.shape
        gray = gray / 255.0
        for h in range(heigh):
            for w in range(width):
                pixel.append(gray[h][w])
        # use neural network
        result = net.output(np.array(pixel, dtype="float"))

        # check the status and take action
        if result:
            if status is NOT_LOOKING:
                status, counter = LOOKING, 0
                # press space to continue playing
                win32api.keybd_event(32,0,0,0)
        else:
            if status is LOOKING:
                if counter + 1 >= ENSURE_COUNT:
                    status = NOT_LOOKING
                    # press space to stop playing
                    win32api.keybd_event(32,0,0,0)
                    counter = 0
                else:
                    counter += 1
        print status 