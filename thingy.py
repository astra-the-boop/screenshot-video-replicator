import mss
import time
import mss.tools
import main
import os
import shutil
import moviepy.video.io.ImageSequenceClip

def record(t, dir="screens"):
    try:
        shutil.rmtree("screens")
    except OSError as e:
        print(f"{e.strerror}")
    print("recording")
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        for i in range(2*t):
            screenshot = sct.grab(monitor)
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=f"{dir}/{i}.png")
            time.sleep(0.5)

def renderFrames(inVid="bad-apple.mp4", dir="", fps=10):
    for i in range(int(main.getVidLength(inVid)*fps)):
        main.render(inVid, f"{dir}{"/" if dir else ""}{i}", t=i/fps)

def render(dir="", fps=10):
    frames = [f for f in os.listdir(".") if os.path.isfile(f) and f.endswith(".png")]
    frames.sort()
    # print(frames)
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(frames, fps)
    clip.write_videofile("output.mp4")

render()