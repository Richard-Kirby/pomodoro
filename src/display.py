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


# Class used to transmit timer data to the diplays.
class CurrentTimerData:
    def __init__(self, name, description, length_sec, colour):
        self.name = name
        self.description = description
        self.length_sec = length_sec
        self.remaining_timer_s = None
        self.timer_colour = colour


# Class to transmit timer and current timer to displays.
class CurrentData:
    def __init__(self):
        self.current_datetime = None
        self.current_timer_data = None


# Class to manage the background images, which are rotated.
class ImageManager:
    def __init__(self):
        self.image_array = None
        self.image_list = {'moon': [
            'buffer0.jpg',
            'buffer1.jpg',
            'buffer2.jpg',
            'buffer3.jpg',
            'buffer4.jpg',
            'buffer5.jpg',
            'buffer6.jpg',
            'buffer7.jpg',
            'buffer8.jpg',
            'buffer9.jpg',
            'buffer10.jpg',
            'buffer11.jpg',
            'buffer12.jpg',
            'buffer13.jpg',
            'buffer14.jpg',
            'buffer15.jpg',
            'buffer16.jpg',
            'buffer17.jpg',
            'buffer18.jpg',
            'buffer19.jpg',
            'buffer20.jpg',
            'buffer21.jpg',
            'buffer22.jpg',
            'buffer23.jpg'
        ]}

    # Set the image series to use
    def set_image_series(self, series_name):
        self.image_array = self.image_list[series_name]

    # Return the current image and wrap it to the end.
    def get_current_image(self):
        curr_image = self.image_array.pop(0)
        self.image_array.append(curr_image)
        return curr_image


# Abstract base class for displaying the clock via various displays as desired. This provides a way to have multiple
# displays such as on the screen as well as a small LCD.
class Display(ABC, threading.Thread):

    # Width and length is desired display size or desired window size depending on the type of display.
    def __init__(self, width, height, toggle_pause_function, restart_function, next_function, pins=None):
        super().__init__()
        self.width = width
        self.height = height
        self.pomodoro_time_state = None
        self.pins = pins
        self._modes = ['clock', 'pomodoro']
        self._curr_mode = None
        self.toggle_pause_function = toggle_pause_function
        self.restart_function = restart_function
        self.next_function = next_function
        self.pomodoro_time_state = None
        self.current_data_queue = queue.Queue()
        self.current_data = CurrentData()
        self.current_image = None

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

            if self.current_data.current_datetime is not None:
                self.update_display()

            time.sleep(0.5)

    @abstractmethod
    def update_display(self):
        pass


# Class for LCD - in this case the DisplayHatMini
class LcdDisplay(Display):
    def __init__(self, toggle_pause_function, restart_function, next_function):
        self.buffer = Image.new("RGB", (DisplayHATMini.WIDTH, DisplayHATMini.HEIGHT,), "BLACK")

        self.fonts = {'main': ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 75),
                      'sub': ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 25)}

        self.display = DisplayHATMini(self.buffer, backlight_pwm=True)
        self.display.set_led(0.0, 0.0, 0.0)

        pins = [self.display.BUTTON_A, self.display.BUTTON_B, self.display.BUTTON_X, self.display.BUTTON_Y]

        super().__init__(self.display.WIDTH, self.display.HEIGHT, toggle_pause_function,
                         restart_function, next_function, pins)

        # Set the current mode
        self.change_mode()

        # Mapping to mode to buttons and functions.
        self.function_dict = {'clock': {self.display.BUTTON_A: self.change_mode(),
                                        self.display.BUTTON_X: self.toggle_pause_function,
                                        self.display.BUTTON_B: self.restart_function,
                                        self.display.BUTTON_Y: self.next_function},
                              'pomodoro': {self.display.BUTTON_A: self.change_mode(),
                                           self.display.BUTTON_X: self.toggle_pause_function,
                                           self.display.BUTTON_B: self.restart_function,
                                           self.display.BUTTON_Y: self.next_function}}

        self.image_manager = ImageManager()
        self.image_manager.set_image_series('moon')

        # Set the last button press to current time.
        self.last_button_press = datetime.datetime.now()

        # Register function to deal with button presses
        self.display.on_button_pressed(self.button_press)

    # Rotate through the modes.
    def change_mode(self):
        super().change_mode()

    # Function to deal with the button presses by calling the appropriate function.
    def button_press(self, pin):
        # print(f"sec button {(datetime.datetime.now() - self.last_button_press).total_seconds()}")
        if (datetime.datetime.now() - self.last_button_press).total_seconds() > 2:
            # Call the function that matches the button
            self.function_dict[self._curr_mode][pin]()
            self.last_button_press = datetime.datetime.now()

    # Draw the icons on the screen according to the mode
    def draw_icons(self, buffer):
        if self._curr_mode == 'clock':
            buffer.paste(Image.open("icons/eject.png"), (0, 60), 0)
            buffer.paste(Image.open("icons/pause.png"), (280, 40), 0)
            buffer.paste(Image.open("icons/back-button.png"), (0, 200), 0)
            buffer.paste(Image.open("icons/next-button.png"), (280, 200), 0)

    # Update the display to show the latest state.
    def update_display(self):
        print(f"{self.current_data.current_datetime}, {self.current_data.current_timer_data.remaining_timer_s}")
        disp_date = self.current_data.current_datetime.strftime("%d-%m-%Y")
        disp_time = self.current_data.current_datetime.strftime("%H:%M:%S")

        # Determining the sign to display (minus means the current timer is exceeded)
        if self.current_data.current_timer_data.remaining_timer_s < 0:
            sign = '-'
            self.display.set_led(0.0, 0.0, 0.0)
            time.sleep(0.1)
            self.display.set_led(0.5, 0.0, 0.0)
            time.sleep(0.1)
            self.display.set_led(0.0, 0.0, 0.0)
        else:
            sign = ''

        # Pomodoro timer string to be displayed.
        pomodoro_time_str = (f"{sign}{abs(int(self.current_data.current_timer_data.remaining_timer_s / 60)):0>2}:"
                             f"{abs(self.current_data.current_timer_data.remaining_timer_s) % 60:0>2}")

        # Background image
        # Start of time
        if self.current_image is None:
            self.current_image = self.image_manager.get_current_image()

        # Go to the next image every minute
        elif self.current_data.current_timer_data.remaining_timer_s % 60 == 0:
            self.current_image = self.image_manager.get_current_image()

        else:  # no change
            self.current_image = self.current_image

        with Image.open(self.current_image) as img:
            self.buffer.paste(img, (int((DisplayHATMini.WIDTH - DisplayHATMini.HEIGHT) / 2), 0))
            draw = ImageDraw.Draw(self.buffer)
            self.draw_icons(self.buffer)

            draw.text((5, 0), f"{disp_date}", font=self.fonts['sub'], fill=(255, 0, 0))
            draw.text((200, 0), f"{disp_time}", font=self.fonts['sub'], fill=(255, 0, 0))

            pomodoro_str_size = self.fonts['main'].getsize(pomodoro_time_str)
            draw.text(((self.display.WIDTH - pomodoro_str_size[0])/2, 60), f"{pomodoro_time_str}", font=self.fonts['main'],
                      fill=self.current_data.current_timer_data.timer_colour)

            # ToDo: need to deal with different modes for font sizes.
            timer_name_size = self.fonts['sub'].getsize(self.current_data.current_timer_data.name)
            draw.text(((self.display.WIDTH - timer_name_size[0])/2, 140),
                      f"{self.current_data.current_timer_data.name}", font=self.fonts['sub'],
                      fill=self.current_data.current_timer_data.timer_colour)

            # ToDo: need to deal with different modes for font sizes.
            timer_description_size = self.fonts['sub'].getsize(self.current_data.current_timer_data.description)
            draw.text(((self.display.WIDTH - timer_description_size[0])/2, 170),
                      f"{self.current_data.current_timer_data.description}", font=self.fonts['sub'],
                      fill=self.current_data.current_timer_data.timer_colour)

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
    current_timer_data = CurrentTimerData("work", "work timer", "1500", '#FF00FF')
    current_data.current_timer_data = current_timer_data

    current_data.current_timer_data.remaining_timer_s = 600
    while True:
        current_data.current_datetime = datetime.datetime.now()
        lcd_display.current_data_queue.put_nowait(current_data)

        # print(f"Queue {lcd_display.current_data_queue.get_nowait()}")
        current_data.current_timer_data.remaining_timer_s -= 1
        time.sleep(.1)
