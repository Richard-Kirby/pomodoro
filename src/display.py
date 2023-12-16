from __future__ import annotations

import time
import datetime
from abc import ABC, abstractmethod
import threading
import queue

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("""This example requires PIL/Pillow, try:

sudo apt install python3-pil

""")

from displayhatmini import DisplayHATMini
import test


class CurrentData:
    def __init__(self):
        self.current_time = None
        self.remaining_timer_s = None


# Abstract base class for displaying the clock via various displays as desired. This provides a way to have multiple
# displays such as on the screen as well as a small LCD.
class Display(ABC, threading.Thread):

    # Width and length is desired display size or desired window size depending on the type of display.
    def __init__(self, width, height, toggle_pause_function, back_function, next_function, pins=None):
        super().__init__()
        self.width = width
        self.height = height
        self.current_time = None
        self.pomodoro_time_state = None
        self.pins = pins
        self._modes = ['clock', 'pomodoro']
        self._curr_mode = None
        self.toggle_pause_function = toggle_pause_function
        self.back_function = back_function
        self.next_function = next_function
        self.current_time = None
        self.pomodoro_time_state = None
        self.current_data_queue = queue.Queue()
        self.current_data = CurrentData()


    # Change modes
    @abstractmethod
    def change_mode(self):

        # If current mode is None, then set to the first mode - initialisation.
        # If not none, circulate through the modes.
        if self._curr_mode is None:
            self._curr_mode = self._modes.pop(0)
        else:
            self._modes.append(self._curr_mode)
            self._curr_mode = self._modes.pop(0)

    def run(self):
        while True:
            while not self.current_data_queue.empty():
                self.current_data = self.current_data_queue.get_nowait()

            if self.current_data.current_time is not None:
                self.update_display()

            time.sleep(0.5)

    @abstractmethod
    def update_display(self):
        pass


# Class for LCD - in this case the DisplayHatMini
class LcdDisplay(Display):
    def __init__(self, toggle_pause_function, back_function, next_function):
        self.buffer = Image.new("RGB", (DisplayHATMini.WIDTH, DisplayHATMini.HEIGHT,), "BLACK")

        self.fonts = {'main': ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 75),
                      'sub':ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 25)}

        self.display = DisplayHATMini(self.buffer, backlight_pwm=True)
        self.display.set_led(0.05, 0.05, 0.05)

        pins = [self.display.BUTTON_A, self.display.BUTTON_B, self.display.BUTTON_X, self.display.BUTTON_Y]

        super().__init__(self.display.WIDTH, self.display.HEIGHT, toggle_pause_function,
                         back_function, next_function, pins)

        # Set the current mode
        self.change_mode()

        # Mapping to mode to buttons and functions.
        self.function_dict = {'clock': {self.display.BUTTON_A: self.change_mode(),
                                        self.display.BUTTON_B: self.toggle_pause_function,
                                        self.display.BUTTON_X: self.back_function,
                                        self.display.BUTTON_Y: self.next_function},
                              'pomodoro': {self.display.BUTTON_A: self.change_mode(),
                                           self.display.BUTTON_B: self.toggle_pause_function,
                                           self.display.BUTTON_X: self.back_function,
                                           self.display.BUTTON_Y: self.next_function}}

    # Rotate through the modes.
    def change_mode(self):
        super().change_mode()

    # Draw the icons on the screen according to the mode
    def draw_icons(self, buffer):
        if self._curr_mode == 'clock':
            buffer.paste(Image.open("icons/eject.png"), (0, 60), 0)
            buffer.paste(Image.open("icons/pause.png"), (280, 40), 0)
            buffer.paste(Image.open("icons/back-button.png"), (0, 200), 0)
            buffer.paste(Image.open("icons/next-button.png"), (280, 200), 0)

    # Update the display to show the latest state.
    def update_display(self):
        print(f"{self.current_data.current_time}, {self.current_data.remaining_timer_s}")
        date = self.current_data.current_time.strftime("%d-%m-%Y")
        time = self.current_data.current_time.strftime("%H:%M:S")
        pomodoro_str = (f"{int(self.current_data.remaining_timer_s/60):0>2}:"
                        f"{abs(self.current_data.remaining_timer_s)%60:0>2}")

        with Image.open("buffer11.jpg") as img:
            self.buffer.paste(img, (int((DisplayHATMini.WIDTH - DisplayHATMini.HEIGHT)/2), 0))
            draw = ImageDraw.Draw(self.buffer)
            self.draw_icons(self.buffer)
            draw.text((5, 0), f"{date}", font=self.fonts['sub'], fill=(255, 0, 0))
            draw.text((200, 0), f"{time}", font=self.fonts['sub'], fill=(255, 0, 0))
            draw.text((100, 100), f"{pomodoro_str}", font=self.fonts['main'], fill=(255, 0, 0))
            self.display.display()


if __name__ == '__main__':
    def toggle_pause_fnc():
        print("toggle pause function test")

    def back_fnc():
        print("back function test")

    def next_fnc():
        print("next function test")

    print("here before run")
    lcd_display = LcdDisplay(toggle_pause_fnc, back_fnc, next_fnc)
    lcd_display.setDaemon(True)
    lcd_display.start()
    print("here after run")
    current_data = CurrentData()

    current_data.remaining_timer_s = 60
    while True:
        current_data.current_time = datetime.datetime.now()
        lcd_display.current_data_queue.put_nowait(current_data)

        # print(f"Queue {lcd_display.current_data_queue.get_nowait()}")
        current_data.remaining_timer_s -= 1
        time.sleep(.1)
