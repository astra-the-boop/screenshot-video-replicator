import mss
import time
import mss.tools
import main
import os
import shutil
import moviepy.video.io.ImageSequenceClip
from tqdm import tqdm

def record(t, dir="screens", remove=True):
    if remove:
        i = 0
        while True:
            try:
                os.remove(f"{dir}/{i}.png")
                i+=1
            except FileNotFoundError:
                break
    try:
        shutil.rmtree("screens")
    except OSError as e:
        print(f"{e.strerror}")

    with mss.mss() as sct:
        monitor = sct.monitors[1]
        for i in tqdm(range(2*t), desc="Recording screen...", unit=" screenshots"):
            screenshot = sct.grab(monitor)
            try:
                mss.tools.to_png(screenshot.rgb, screenshot.size, output=f"{dir}/{i}.png")
            except FileNotFoundError:
                os.mkdir(f"{dir}")
            time.sleep(0.5)

def renderFrames(inVid="bad-apple.mp4", fps=10):
    i = 0
    while True:
        try:
            print("remove")
            os.remove(f"{i}.png")
            i+=1
        except FileNotFoundError as e:
            print(e)
            break
    for i in range(int(main.getVidLength(inVid)*fps)):
        main.render(inVid, f"{i}", t=i/fps)

def render(fps=10, output="output.mp4"):
    frames = [int(f[:-4]) for f in os.listdir(".") if os.path.isfile(f) and f.endswith(".png")]
    frames.sort()
    frameName = [str(i)+".png" for i in frames]
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(frameName, fps)
    clip.write_videofile(output)