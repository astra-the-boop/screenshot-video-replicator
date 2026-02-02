import cv2

x = 40
y = 22

tileNorm = 22

def loadFrame(path="bad-apple.mp4", t=0.25):
    cap = cv2.VideoCapture(path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    target = int(total * t)

    i=0
    f = None
    while True:
        ret, f = cap.read()
        if not ret:
            break
        if i==target:
            frame = f
            break
        i+=1
    cap.release()
    return frame