import cv2
import numpy as np
import glob

x = 40
y = 22

tileNorm = 22

def loadFrame(path="bad-apple.mp4", t=0.25):
    global frame
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

def tileSplit(frame, gx, gy):
    h, w, _ = frame.shape
    tileWidth = w // gx
    tileHeight = h // gy

    tiles = []

    for y in range(gy):
        for x in range(gx):
            tile = frame[
                y*tileHeight:(y+1)*tileWidth,
                x*tileWidth:(x+1)*tileWidth
            ]
            tiles.append(tile)

    return tiles, tileWidth, tileHeight

def normalize(img, size=tileNorm):
    img = cv2.resize(img, (size, size))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    return img

def loadRecord(folder):
    imgs = []
    for path in glob.glob(folder + "/*.png"):
        imgs.append(cv2.imread(path))

    return imgs

videoFrame = loadFrame("bad-apple.mp4")
videoTiles, tileW, tileH = tileSplit(videoFrame, x, y)
videoTilesN = [normalize(t) for t in videoTiles]

screens = loadRecord("screens")
screenTilesN = [normalize(s) for s in screens]

def distance(a,b):
    return np.mean((a.astype(np.float32) - b.astype(np.float32))**2)

matches = []

for i in videoTilesN:
    best = None
    bestDistance = float("inf")
    for j in screenTilesN:
        d = distance(i,j)
        if d<bestDistance:
            bestDistance = d
            best = j

out = np.zeros(
    (y * tileH, x * tileW, 3),dtype=np.uint8
)

i=0
for yy in range(y):
    for xx in range(x):
        tile = cv2.resize(matches[i], (tileW, tileH))
        out[
            yy*tileH:(yy+1)*tileH,
            xx*tileW:(xx+1)*tileW
        ] = tile
        i+=1

cv2.imwrite("mosaic.png", out)