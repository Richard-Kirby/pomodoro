#!/usr/bin/env python3
import time
import pigpio
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
    (33, 50, 323, 340),
    (330, 50, 620, 340),
    (630, 50, 920, 340),
    (930, 50, 1220, 340),
    (33, 355, 323, 635),
    (330, 355, 620, 635),
    (628, 357, 918, 637),
    (930, 350, 1220, 610),
    (60, 650, 320, 910),
    (350, 650, 610, 910),
    (650, 650, 910, 910),
    (950, 650, 1210, 910),
    (60, 950, 320, 1210),
    (350, 950, 610, 1210),
    (650, 950, 910, 1210),
    (950, 950, 1210, 1210),
    (60, 1250, 320, 1510),
    (350, 1250, 610, 1510),
    (650, 1250, 910, 1510),
    (950, 1250, 1210, 1510),
    (60, 1550, 320, 1810),
    (350, 1550, 610, 1810),
    (650, 1550, 910, 1810),
    (950, 1550, 1210, 1810)]

    for i in range(len(img_crop)):
        img = org_img.crop(img_crop[i])
        #print(f"Image size {img.size}")
        img = img.resize((int(DisplayHATMini.HEIGHT), int(DisplayHATMini.HEIGHT)), Image.LANCZOS)
        #img.show()
        img.save(f"image{i}.jpg")
        buffer.paste(img, (int((DisplayHATMini.WIDTH - DisplayHATMini.HEIGHT)/2), 0))
        buffer.save(f"buffer{i}.jpg")
        #buffer.paste(img, (0, 0))
        draw = ImageDraw.Draw(buffer)
        draw_icons(buffer)
        draw.text((10, 70), f"Image {i}", font=font, fill=(255, 0, 0))
        displayhatmini.display()
        time.sleep(1)


#pi = pigpio.pi()
#pi.set_pull_up_down(19, pigpio.PUD_UP)

while True:
    displayhatmini.display()
    displayhatmini.set_backlight(brightness)
    #print(f"Old A 5 {pi.read(5)},New A 19 {pi.read(19)}, B 6 {pi.read(6)}, X 16 {pi.read(16)},Y 24 {pi.read(24)}")
    time.sleep(1.0/30)
