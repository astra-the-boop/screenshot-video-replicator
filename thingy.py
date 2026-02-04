import mss
import time
import mss.tools
import main
import os
import shutil

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

def render(inVid="bad-apple.mp4"):
    for i in range(int(main.getVidLength(input)*10)):
        main.render(input, f"{i}", t=i/10)