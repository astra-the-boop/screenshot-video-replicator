import cv2
import numpy as np
import glob
import os

x = 40
y = 22

tileNorm = 22


def loadFrame(path="bad-apple.mp4", t=0.25):
    global frame
    cap = cv2.VideoCapture(path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    target = int(total * t)

    i = 0
    f = None
    while True:
        ret, f = cap.read()
        if not ret:
            break
        if i == target:
            frame = f
            break
        i += 1
    cap.release()
    return frame


def tileSplit(frame, gx, gy):
    h, w, _ = frame.shape
    tileWidth = w // gx
    tileHeight = h // gy

    tiles = []

    for yy in range(gy):
        for xx in range(gx):
            tile = frame[
                   yy * tileHeight:(yy + 1) * tileHeight,
                   xx * tileWidth:(xx + 1) * tileWidth
                   ]
            tiles.append(tile)

    return tiles, tileWidth, tileHeight


def cropTile(img, tileX, tileY, gx, gy, w, h):
    H, W, _ = img.shape

    rx = tileX / gx
    ry = tileY / gy

    cx = int(rx * (W - w))
    cy = int(ry * (H - h))

    return img[cy:cy + h, cx:cx + w]


def normalize(img, size=tileNorm):
    img = cv2.resize(img, (size, size))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    return img


def loadRecord(folder):
    imgs = []
    for path in glob.glob(folder + "/*.png"):
        img = cv2.imread(path)
        if img is not None:
            imgs.append(img)

    return imgs


videoFrame = loadFrame("bad-apple.mp4")
videoTiles, tileW, tileH = tileSplit(videoFrame, x, y)
videoTilesN = [normalize(t) for t in videoTiles]

screens = loadRecord("screens")
screenTilesN = []
screenTilesRaw = []

for s in screens:
    tiles, _, _ = tileSplit(s, x, y)
    for t in tiles:
        screenTilesRaw.append(t)
        screenTilesN.append(normalize(t))


def distance(a, b):
    return np.mean((a.astype(np.float32) - b.astype(np.float32)) ** 2)


matches = []

tilesInScreen = x * y
for idx, vtil in enumerate(videoTilesN):
    tilesPos = idx % tilesInScreen
    best = -1
    bestDistance = float("inf")

    for s in range(len(screens)):
        candidate = screenTilesN[s * tilesInScreen + tilesPos]
        d = distance(vtil, candidate)
        if d < bestDistance:
            bestDistance = d
            best = s
    matches.append(best)

out = np.zeros(
    (y * tileH, x * tileW, 3), dtype=np.uint8
)

i = 0
for yy in range(y):
    for xx in range(x):
        src = screenTilesRaw[matches[i] * tilesInScreen + i]
        reSrc = cv2.resize(src, (tileW, tileH), interpolation=cv2.INTER_AREA)
        out[
        yy * tileH:(yy + 1) * tileH,
        xx * tileW:(xx + 1) * tileW
        ] = reSrc

        i += 1

cv2.imwrite("mosaic.png", out)