import time
import mss
import numpy as np
import cv2

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
