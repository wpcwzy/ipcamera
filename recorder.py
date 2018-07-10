import cv2

video = cv2.VideoCapture('http://192.168.0.126:81/videostream.cgi?user=raspberry&pwd=pi')
print "Is video Opened:"+str(video.isOpened())

def record():
    isSuccess, frame = video.read()
    cv2.imshow('frame', frame)
    print "record"
    output = cv2.VideoWriter('output.avi',4, 20, (640, 480))
    output.write(frame)
    cleanup()
def cleanup():
    print "cleanup"

if __name__=='__main__':
    while (video.isOpened()):
        record()

        if cv2.waitKey(1) == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()
