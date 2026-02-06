import mss
import time
import mss.tools
import main
import os
import shutil
import moviepy.video.io.ImageSequenceClip

def record(t, dir="screens", remove=True):
    if remove:
        i = 0
        while True:
            try:
                os.remove(f"{dir}/{i}.png")
                i+=1
            except:
                break
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

def renderFrames(inVid="bad-apple.mp4", fps=10):
    i = 0
    while True:
        try:
            print("remove")
            os.remove(f"{i}.png")
            i+=1
        except:
            print("broke")
            break
    for i in range(int(main.getVidLength(inVid)*fps)):
        main.render(inVid, f"{i}", t=i/fps)

def render(fps=10):
    frames = [int(f[:-4]) for f in os.listdir(".") if os.path.isfile(f) and f.endswith(".png")]
    frames.sort()
    frameName = [str(i)+".png" for i in frames]
    # print(frameName)
    # print(frames)
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(frameName, fps)
    clip.write_videofile("output.mp4")

renderFrames()