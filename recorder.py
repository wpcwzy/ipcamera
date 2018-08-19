# /usr/bin/env python
# -*- coding: UTF-8 -*-

import cv2
import time
import requests

nowTime = time.time()
videoStartTime = nowTime
videoMaxNum = 150  # around 15GB,25hours
nowTime = time.time()
videoNum = 0
videoTime = 600
fps = 0
framecount = 0

retryTime = 0
waitTime = 5
cameraName = "Camera 1"


video = cv2.VideoCapture('http://192.168.0.126:81/videostream.cgi?user=raspberry&pwd=pi')
logFile = "log.log"
print "Is video Opened:" + str(video.isOpened())

frameStartTime = time.time()
while (time.time() - frameStartTime <= 1):
    isSuccess, frame = video.read()
    fps = fps + 1
output = cv2.VideoWriter(str(videoNum) + '.avi', 4, fps, (640, 480))

def logger(string):
    log = open(logFile, "a")
    log.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "  " + string)
    log.close()


def PTZ(model):
    if model == 1:
        requests.post("http://192.168.0.126:81/decoder_control.cgi?user=raspberry&pwd=pi&command=0")
        logger("PTZ up\n")
    if model == 2:
        requests.post("http://192.168.0.126:81/decoder_control.cgi?user=raspberry&pwd=pi&command=4")
        logger("PTZ left\n")
    if model == 3:
        requests.post("http://192.168.0.126:81/decoder_control.cgi?user=raspberry&pwd=pi&command=2")
        logger("PTZ down\n")
    if model == 4:
        requests.post("http://192.168.0.126:81/decoder_control.cgi?user=raspberry&pwd=pi&command=6")
        logger("PTZ right\n")
    if model == 5:
        requests.post("http://192.168.0.126:81/decoder_control.cgi?user=raspberry&pwd=pi&command=1")
        logger("PTZ stop\n")

if __name__ == '__main__':
    try:
        while (not video.isOpened()):
            temp = retryTime + 1
            retryTime = temp
            output = cv2.VideoWriter(str(videoNum) + '.avi', 4, fps, (640, 480))
            video = cv2.VideoCapture('http://192.168.0.126:81/videostream.cgi?user=raspberry&pwd=pi')
            print("Camera Open Failed.Retry " + str(retryTime) + " Times")
            print("Sleep " + str(waitTime) + " seconds")
            logger("Camera Open Failed.Retry " + str(retryTime) + " Times\n")
            logger("Sleep " + str(waitTime) + " seconds\n")
            time.sleep(waitTime)
        logger("Camera opened\n")
        logger("Now Recording:0.avi\n")
        while (video.isOpened() & output.isOpened()):
            isSuccess, frame = video.read()
            cv2.putText(frame, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), (10, 470), cv2.FONT_HERSHEY_PLAIN,
                        1, (0, 0, 255), 2)  # Add time tag to the video
            cv2.putText(frame, cameraName, (550, 470), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255),
                        2)  # add name tag to the video
            cv2.imshow('frame', frame)
            output.write(frame)
            nowTime = time.time()
            if nowTime - videoStartTime >= videoTime:
                output.release
                temp = videoNum + 1
                videoNum = temp
                if videoNum >= videoMaxNum:
                    videoNum = 0
                fps = 0
                frameStartTime = time.time()
                while (time.time() - frameStartTime <= 1):
                    isSuccess, frame = video.read()
                    fps = fps + 1
                output = cv2.VideoWriter(str(videoNum) + '.avi', 4, fps, (640, 480))
                logger("Now Recording:" + str(videoNum) + ".avi\n")
                videoStartTime = nowTime
            pressedKey = cv2.waitKey(1)
            if pressedKey == 113:  # q
                break
                print "Manually Stop"
                logger("Manually Stop\n")
            if pressedKey == 119:  # w
                print "PTZ up"
                PTZ(1)
            if pressedKey == 97:  # a
                print "PTZ left"
                PTZ(2)
            if pressedKey == 115:  # s
                print "PTZ down"
                PTZ(3)
            if pressedKey == 100:  # d
                print "PTZ right"
                PTZ(4)
            if pressedKey == 122:  # z
                print "PTZ stop"
                PTZ(5)
    except Exception, e:
        logger(repr(e))
        print (repr(e))
    video.release()
    output.release()
    cv2.destroyAllWindows()
