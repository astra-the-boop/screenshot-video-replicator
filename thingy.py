import mss
import time
import mss.tools
import main

t = 30

print("recording")
# with mss.mss() as sct:
#     monitor = sct.monitors[1]
#     for i in range(2*t):
#         screenshot = sct.grab(monitor)
#         mss.tools.to_png(screenshot.rgb, screenshot.size, output=f"screens/{i}.png")
#         time.sleep(0.5)

for i in range(int(main.getVidLength("bad-apple.mp4")*10)):
    main.render("bad-apple.mp4", f"{i}", t=i/100)
