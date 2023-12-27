#!/usr/bin/env python3
import time
# import pigpio
from displayhatmini import DisplayHATMini

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("""This example requires PIL/Pillow, try:

sudo apt install python3-pil

""")

width = DisplayHATMini.WIDTH
height = DisplayHATMini.HEIGHT
buffer = Image.new("RGB", (width, height), "BLACK")

font = ImageFont.load_default()

displayhatmini = DisplayHATMini(buffer, backlight_pwm=True)
displayhatmini.set_led(0.05, 0.05, 0.05)

brightness = 1.0


# Plumbing to convert Display HAT Mini button presses into pygame events
def button_callback(pin):
    global brightness

    # Only handle presses
    if not displayhatmini.read_button(pin):
        return

    if pin == displayhatmini.BUTTON_A:
        brightness += 0.1
        brightness = min(1, brightness)
        print("A Button")

    if pin == displayhatmini.BUTTON_B:
        brightness -= 0.1
        brightness = max(0, brightness)
        print("B Button")


displayhatmini.on_button_pressed(button_callback)

def draw_icons(buffer):
    buffer.paste(Image.open("icons/eject.png"),(0, 60), 0)
    buffer.paste(Image.open("icons/pause.png"),(280, 40), 0)
    buffer.paste(Image.open("icons/back-button.png"),(0, 200), 0)
    buffer.paste(Image.open("icons/next-button.png"),(280, 200), 0)


with Image.open("Moon_phases.jpg") as org_img:  #

    img_crop  = [
    (35, 50, 325, 340),  # 0
    (335, 50, 625, 340),
    (635, 50, 925, 340),
    (935, 50, 1225, 340),  # 3
    (33, 350, 323, 640),
    (330, 350, 620, 640 ),
    (638, 355, 918, 635),  # 6
    (940, 355, 1220, 635),
    (45, 660, 315, 930),
    (350, 660, 620, 930),  # 9
    (650, 660, 920, 930),
    (950, 660, 1220, 930),
    (50, 960, 320, 1230),  # 12
    (345, 960, 615, 1230),
    (650, 960, 920, 1230),
    (950, 960, 1220, 1230),  # 15
    (40, 1255, 310, 1525),
    (340, 1255, 610, 1525),
    (650, 1255, 920, 1525),  # 18
    (940, 1250, 1220, 1530),
    (40, 1550, 320, 1830),
    (340, 1550, 630, 1840),  # 21
    (640, 1550, 930, 1840),
    (950, 1550, 1240, 1840)]

    for i in range(len(img_crop)):
        img = org_img.crop(img_crop[i])
        #print(f"Image size {img.size}")
        img.save(f"preimage{i}.jpg")
        img = img.resize((int(DisplayHATMini.HEIGHT), int(DisplayHATMini.HEIGHT)), Image.LANCZOS)
        #img.show()
        buffer.paste(img, (int((DisplayHATMini.WIDTH - DisplayHATMini.HEIGHT)/2), 0))
        buffer.save(f"image{i}.jpg")
        #buffer.paste(img, (0, 0))
        draw = ImageDraw.Draw(buffer)
        # draw_icons(buffer)

        displayhatmini.display()
        input(f"Image {i} x {img_crop[i][2]-img_crop[i][0]} y {img_crop[i][3]-img_crop[i][1]} press enter")


#pi = pigpio.pi()
#pi.set_pull_up_down(19, pigpio.PUD_UP)

while True:
    displayhatmini.display()
    displayhatmini.set_backlight(brightness)
    #print(f"Old A 5 {pi.read(5)},New A 19 {pi.read(19)}, B 6 {pi.read(6)}, X 16 {pi.read(16)},Y 24 {pi.read(24)}")
    time.sleep(1.0/30)
