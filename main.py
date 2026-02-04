import cv2
import numpy as np
import glob
import os

from requests.packages import target


def loadFrame(path="bad-apple.mp4", t=0.25):
    global frame
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise RuntimeError("Cannot open video file")
    fps = cap.get(cv2.CAP_PROP_FPS)
    target = int(t*fps)
    cap.set(cv2.CAP_PROP_POS_FRAMES, target)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise RuntimeError(f"Cannot read video file at time {t}s")
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


def normalize(img, size):
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

def render(path, exportAs, t=0, x=40, y=22, scale=10, tileNorm=22):
    print("rendering")
    videoFrame = loadFrame("bad-apple.mp4", t)
    videoTiles, tileW, tileH = tileSplit(videoFrame, x, y)
    videoTilesN = [normalize(t, tileNorm) for t in videoTiles]

    screens = loadRecord("screens")
    screenNorms = [normalize(s, tileNorm) for s in screens]
    matches = []
    for vtil in videoTilesN:
        best = -1
        bestDistance = float("inf")

        for j, sn in enumerate(screenNorms):
            d = distance(vtil, sn)
            if d < bestDistance:
                bestDistance = d
                best = j

        matches.append(best)

    out = np.zeros(
        (y * tileH * scale, x * tileW * scale, 3), dtype=np.uint8
    )

    i = 0
    for yy in range(y):
        for xx in range(x):
            src = screens[matches[i]]
            reSrc = cv2.resize(src, (tileW * scale, tileH * scale), interpolation=cv2.INTER_AREA)
            out[
            yy * tileH * scale:(yy + 1) * tileH * scale,
            xx * tileW * scale:(xx + 1) * tileW * scale
            ] = reSrc

            i += 1

    cv2.imwrite(f"{exportAs}.png", out)



def distance(a, b):
    return np.mean((a.astype(np.float32) - b.astype(np.float32)) ** 2)

def getVidLength(path):
    cap = cv2.VideoCapture(path)
    fps=cap.get(cv2.CAP_PROP_FPS)
    frameCount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    return frameCount/fps