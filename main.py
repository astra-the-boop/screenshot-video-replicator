import time
import mss
import numpy as np
import cv2

ref="bad-apple.mp4"

def capture(dur=10, fps=6):
    frames = []
    interval = 1/fps

    with mss.mss() as sct:
        monitor = sct.monitors[1]
        start = time.time()
        while time.time() - start < dur:
            img = sct.grab(monitor)
            frame = np.array(img)[:,:,:3]
            frames.append(frame)
            time.sleep(interval)

    return frames

def sample(path, count):
    cap = cv2.VideoCapture(path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    indices = np.linspace(0,total-1, count).astype(int)

    frames= []
    frameI = 0
    targetI=0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frameI==indices[targetI]:
            frames.append(frame)
            targetI +=1
            if targetI >=len(indices):
                break
        frameI+=1
    cap.release()
    return frames

def normalize(frame, size=32):
    frame = cv2.resize(frame, (size, size))
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(grey, 50, 160)

    frame[edges>0] = (0,0,0)
    return frame


screens = capture(5,2)
videoTargets = sample(ref, len(screens))
screensN=[normalize(i) for i in screens]
targetN = [normalize(i) for i in videoTargets]


cell = 32
cols = 10
rows = len(screensN)//cols+1

canvas = np.zeros((rows*cell, cols*cell, 3), dtype=np.uint8)
for i, frames in enumerate(screensN):
    r = i // cols
    c = i % cols
    canvas[r * cell:(r+1), c * cell:(c + 1) * cell] = frames

cv2.imwrite("grid.png", canvas)