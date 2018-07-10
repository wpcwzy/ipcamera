import cv2
import time
import requests

videoStartTime = 0

output = cv2.VideoWriter('output.avi', 4, 8, (640, 480))
video = cv2.VideoCapture('http://192.168.0.126:81/videostream.cgi?user=raspberry&pwd=pi')
print "Is video Opened:"+str(video.isOpened())

def record():
    isSuccess, frame = video.read()
    cv2.imshow('frame', frame)
    output.write(frame)
    cleanup()

def cleanup():
    a = 1;


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
    while (video.isOpened()):
        record()
        nowTime = time.time()
        if cv2.waitKey(100) == ord('q'):
            break
        if cv2.waitKey(100) == ord('w'):
            print "PTZ up"
            PTZ(1)
        if cv2.waitKey(100) == ord('a'):
            print "PTZ left"
            PTZ(2)
        if cv2.waitKey(100) == ord('s'):
            print "PTZ down"
            PTZ(3)
        if cv2.waitKey(100) == ord('d'):
            print "PTZ right"
            PTZ(4)
        if cv2.waitKey(100) == ord('z'):
            print "PTZ stop"
            PTZ(5)

    video.release()
    output.release()
    cv2.destroyAllWindows()
