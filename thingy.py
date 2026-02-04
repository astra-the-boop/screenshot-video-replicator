import mss
import time
import mss.tools

t = 30

print("recording")
with mss.mss() as sct:
    monitor = sct.monitors[1]
    for i in range(2*t):
        screenshot = sct.grab(monitor)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=f"screens/{i}.png")
        time.sleep(0.5)

import main
