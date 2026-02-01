import cv2

video = cv2.VideoCapture("bad-apple.mp4")

if not video.isOpened():
    raise RuntimeError("Could not open video")

frames = []
count = 0

while True:
    ret, frame = video.read()
    if not ret:
        break
    if count % 30 == 0:
        frames.append(frame)
    count += 1

video.release()
print(f"{len(frames)} frames")