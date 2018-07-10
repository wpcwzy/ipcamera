import cv2
import time
import requests

nowTime = time.time()
videoStartTime = nowTime
videoMaxNum = 64
nowTime = time.time()
videoNum = 0
videoTime = 600

output = cv2.VideoWriter(str(videoNum) + '.avi', 4, 4, (640, 480))
video = cv2.VideoCapture('http://192.168.0.126:81/videostream.cgi?user=raspberry&pwd=pi')
print "Is video Opened:"+str(video.isOpened())


def PTZ(model):
    if model == 1:
        requests.post("http://192.168.0.126:81/decoder_control.cgi?user=raspberry&pwd=pi&command=0")
    if model == 2:
        requests.post("http://192.168.0.126:81/decoder_control.cgi?user=raspberry&pwd=pi&command=4")
    if model == 3:
        requests.post("http://192.168.0.126:81/decoder_control.cgi?user=raspberry&pwd=pi&command=2")
    if model == 4:
        requests.post("http://192.168.0.126:81/decoder_control.cgi?user=raspberry&pwd=pi&command=6")
    if model == 5:
        requests.post("http://192.168.0.126:81/decoder_control.cgi?user=raspberry&pwd=pi&command=1")



if __name__=='__main__':
    while (video.isOpened() & output.isOpened()):
        isSuccess, frame = video.read()
        cv2.imshow('frame', frame)
        output.write(frame)
        nowTime = time.time()
        if nowTime - videoStartTime >= videoTime:
            output.release
            temp = videoNum + 1
            videoNum = temp
            if videoNum >= videoMaxNum:
                videoNum = 0
            output = cv2.VideoWriter(str(videoNum) + '.avi', 4, 7, (640, 480))
            videoStartTime = nowTime
        pressedKey = cv2.waitKey(1)
        if pressedKey == 113:  # q
            break
        if pressedKey == 119:  #w
            print "PTZ up"
            PTZ(1)
        if pressedKey == 97:  #a
            print "PTZ left"
            PTZ(2)
        if pressedKey == 115:  #s
            print "PTZ down"
            PTZ(3)
        if pressedKey == 100:  #d
            print "PTZ right"
            PTZ(4)
        if pressedKey == 122:  #z
            print "PTZ stop"
            PTZ(5)

    video.release()
    output.release()
    cv2.destroyAllWindows()