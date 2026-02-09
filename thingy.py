import mss
import time
import mss.tools
import main
import os
import shutil
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
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
    for i in tqdm(range(int(main.getVidLength(inVid)*fps)), desc="Rendering frames...", unit="frames"):
        main.render(inVid, f"{i}", t=i/fps)

def render(inputVid, fps=10, output="output.mp4"):
    frames = [int(f[:-4]) for f in os.listdir(".") if os.path.isfile(f) and f.endswith(".png")]
    frames.sort()
    frameName = [str(i)+".png" for i in frames]
    clip = ImageSequenceClip(frameName, fps)

    inputClip = VideoFileClip(inputVid)
    audio = inputClip.audio.subclipped(0, clip.duration)

    clip = clip.with_audio(audio)

    clip.write_videofile(output,codec="libx264",audio_codec="aac",fps=fps)
    clip.close()
    inputClip.close()

render("bad-apple.mp4")