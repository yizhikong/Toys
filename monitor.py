# -*- coding: cp936 -*-
import cv2
import time
import numpy as np
import os
import itchat
import threading
import facedetect

class Monitor(object):

    def __init__(self, sender):
        # get camera
        self.cap = cv2.VideoCapture(0)
        if self.cap.isOpened():
            print 'Open camera succeeds!'
        else:
            print 'Fail to open camera!'

        # 0 means normal, 1 means abnormal
        self.status = 0
        self.work = True
        self.setSample()
        self.sender = sender
        self.sendTo = 'filehelper'
        self.CHECK_INTERVAL = 2
        self.lastCheckTime = time.time()
        self.monitorThread = threading.Thread(target = self.monitor, args = ())
        self.monitorThread.start()

    def setSample(self):
        print 'Begin to take sample'
        # get lots of sample
        samples = []
        while len(samples) < 50:
            result, image = self.cap.read()
            samples.append(np.array(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), dtype='int'))
        # cut the head because those images are fuzzy
        samples = samples[len(samples) / 2:]

        # take the aver image as sample
        self.sample = np.array(sum(samples) / len(samples), dtype='uint8')
        self.pixelsNum = self.sample.shape[0] * self.sample.shape[1]

        print 'End of taking sample'

    # compare with self.sample
    def isDifferent(self, img):
        absImg = abs(img - self.sample)
        changes = absImg[absImg > 30]
        if len(changes) > self.pixelsNum * 0.05:
            return True
        else:
            return False

    # monitor
    def monitor(self):
        self.sender.sendMsg('[Monitor is working...]', toUserName = self.sendTo)
        while self.work:
            result, image = self.cap.read()
            gray = np.array(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), dtype='int')
            if self.isDifferent(gray):
                if self.status == 0:
                    self.sender.sendMsg('[Alert!]', toUserName = self.sendTo)
                    #self.check()
                    self.status = 1
                elif time.time() - self.lastCheckTime > self.CHECK_INTERVAL:
                    self.lastCheckTime = time.time()
                    cv2.imwrite('face.jpg', image)
                    binaryImg = open('face.jpg', 'rb').read()
                    if len(facedetect.microsoft_detect2(binaryImg)) > 0:
                        self.check()
            else:
                if self.status == 1:
                    self.sender.sendMsg('[All clear]', toUserName = self.sendTo)
                    self.status = 0

    # should call when something happen, for example, user inputs a command
    def check(self):
        # get camera image
        result, image = self.cap.read()
        # save image
        imageName = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + '.jpg'
        cv2.imwrite(imageName, image)
        # send use sender
        self.sender.sendImg(imageName, toUserName = self.sendTo)

    # start monitor thread
    def start(self):
        if not self.monitorThread.is_alive():
            self.work = True
            self.monitorThread = threading.Thread(target = self.monitor, args = ())
            self.monitorThread.start()

    # stop monitor
    def stop(self):
        if self.monitorThread.is_alive():
            self.work = False
            self.sender.sendMsg('[Monitor has stopped]', toUserName = self.sendTo)

    # reset sample
    def resetSample(self):
        self.work = False
        self.setSample()
        self.monitorThread = threading.Thread(target = self.monitor, args = ())
        self.start()

class WeChat(object):
    # store command - function
    command = None

    def __init__(self):
        # login wechat
        print 'Please login wechat by scan QR Code:'
        itchat.auto_login(enableCmdQR = True, hotReload = True)

    def addCommand(self, cmd, func):
        if WeChat.command == None:
            WeChat.command = {}
        WeChat.command[cmd] = func

    def sendMsg(self, msg, toUserName = None):
        itchat.send(msg, toUserName = toUserName)

    def sendImg(self, fileName, toUserName = None):
        itchat.send('@img@' + fileName, toUserName = toUserName)

    @itchat.msg_register(['Text'])
    def command(msg):
        # exclude
        if msg['Type'] != 'Text' or msg['ToUserName'] != 'filehelper':
            return
        # run command
        if msg['Content'] in WeChat.command:
            WeChat.command[msg['Content']]()

if __name__ == '__main__':
    yzkk = WeChat()
    mon = Monitor(yzkk)
    yzkk.addCommand('check', mon.check)
    yzkk.addCommand('start', mon.start)
    yzkk.addCommand('stop', mon.stop)
    yzkk.addCommand('resetSample', mon.resetSample)
    itchat.run()
