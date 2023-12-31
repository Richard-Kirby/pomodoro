from __future__ import annotations

import time
import datetime
from abc import ABC, abstractmethod
import threading
import queue
from PIL import Image, ImageDraw, ImageFont
from displayhatmini import DisplayHATMini


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
            'image0.jpg',
            'image1.jpg',
            'image2.jpg',
            'image3.jpg',
            'image4.jpg',
            'image5.jpg',
            'image6.jpg',
            'image7.jpg',
            'image8.jpg',
            'image9.jpg',
            'image10.jpg',
            'image11.jpg',
            'image12.jpg',
            'image13.jpg',
            'image14.jpg',
            'image15.jpg',
            'image16.jpg',
            'image17.jpg',
            'image18.jpg',
            'image19.jpg',
            'image20.jpg',
            'image21.jpg',
            'image22.jpg',
            'image23.jpg'
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

        print(f"Current mode {self._curr_mode}")

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

        self.fonts = {'main': ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 75),
                      'sub': ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 25)}

        self.display = DisplayHATMini(self.buffer, backlight_pwm=True)
        self.display.set_led(0.0, 0.0, 0.0)

        pins = [self.display.BUTTON_A, self.display.BUTTON_B, self.display.BUTTON_X, self.display.BUTTON_Y]

        super().__init__(self.display.WIDTH, self.display.HEIGHT, toggle_pause_function,
                         restart_function, next_function, pins)

        # Set the current mode
        self.change_mode()

        # Mapping to mode to buttons and functions.
        self.function_dict = {'clock': {self.display.BUTTON_A: self.change_mode,
                                        self.display.BUTTON_X: self.toggle_pause_function,
                                        self.display.BUTTON_B: self.restart_function,
                                        self.display.BUTTON_Y: self.next_function},
                              'pomodoro': {self.display.BUTTON_A: self.change_mode,
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
    # ToDo Icons should be different based on mode.
    def draw_icons(self, buffer):
        print(f"icons current mode {self._curr_mode}")
        if self._curr_mode == 'clock':
            buffer.paste(Image.open("icons/eject.png"), (0, 60), 0)
            buffer.paste(Image.open("icons/pause.png"), (280, 40), 0)
            buffer.paste(Image.open("icons/back-button.png"), (0, 200), 0)
            buffer.paste(Image.open("icons/next-button.png"), (280, 200), 0)
        elif self._curr_mode == 'pomodoro':
            buffer.paste(Image.open("icons/eject.png"), (0, 60), 0)
            buffer.paste(Image.open("icons/pause.png"), (280, 40), 0)
            buffer.paste(Image.open("icons/back-button.png"), (0, 200), 0)
            buffer.paste(Image.open("icons/next-button.png"), (280, 200), 0)
        else:
            raise TypeError

    # Write the text at the desired location, with the font colour and the bac_fill_colour.
    @staticmethod
    def write_text(draw, text, location, font, font_colour, border=0, back_fill_colour=None):

        left, top, right, bottom = draw.textbbox(location, text, font=font)

        # If a back_fill_colour is defined, then draw a text box around it with the requested background colour.
        if back_fill_colour is not None:
            draw.rectangle((left - border, top - border, right + border, bottom + border), fill=back_fill_colour)
        else:
            pass

        draw.text(location, text, font=font, fill=font_colour)

    # Update the display to show the latest state.
    # TODO: add different modes
    def update_display(self):
        # print(f"{self.current_data.current_datetime}, {self.current_data.current_timer_data.remaining_timer_s}")
        # self.buffer = Image.new("RGB", (DisplayHATMini.WIDTH, DisplayHATMini.HEIGHT,), "BLACK")

        self.buffer.paste(0, (0, 0, DisplayHATMini.WIDTH - 1, DisplayHATMini.HEIGHT - 1))

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
            # self.draw_icons(self.buffer)

        else:  # no change
            self.current_image = self.current_image

        with Image.open(self.current_image) as img:
            # print(f"image size {img.size} display size {self.display.WIDTH} {self.display.HEIGHT}")
            # self.buffer.paste(img, (int((DisplayHATMini.WIDTH - DisplayHATMini.HEIGHT) / 2), 0))
            # print(f"x = {int((self.display.WIDTH - img.size[0])/2)} y = {int((self.display.HEIGHT - img.size[1])/2)}")
            self.buffer.paste(img, (int((self.display.WIDTH - img.size[0]) / 2),
                                    int((self.display.HEIGHT - img.size[1]) / 2)))

            # self.draw_icons(self.buffer)

            draw = ImageDraw.Draw(self.buffer)
            # self.draw_icons(self.buffer)

            draw.text((5, 0), f"{disp_date}", font=self.fonts['sub'])
            draw.text((200, 0), f"{disp_time}", font=self.fonts['sub'])

            pomodoro_str_size = self.fonts['main'].getsize(pomodoro_time_str)

            # Large display item
            self.write_text(draw, pomodoro_time_str,
                            (int((self.display.WIDTH - pomodoro_str_size[0]) / 2), 60), self.fonts['main'],
                            self.current_data.current_timer_data.timer_colour, border=2,
                            back_fill_colour='black')

            # ToDo: need to deal with different modes for font sizes.
            timer_name_size = self.fonts['sub'].getsize(self.current_data.current_timer_data.name)

            self.write_text(draw, self.current_data.current_timer_data.name,
                            ((self.display.WIDTH - timer_name_size[0]) / 2, 140),
                            self.fonts['sub'], self.current_data.current_timer_data.timer_colour,
                            border=2, back_fill_colour='black')

            timer_description_size = self.fonts['sub'].getsize(self.current_data.current_timer_data.description)

            self.write_text(draw, self.current_data.current_timer_data.description,
                            ((self.display.WIDTH - timer_description_size[0]) / 2, 170),
                            self.fonts['sub'], self.current_data.current_timer_data.timer_colour,
                            border=2, back_fill_colour='black')

            # ToDo: need to deal with different modes for font sizes.

            self.display.display()


if __name__ == '__main__':
    def toggle_pause_fnc():
        print("toggle pause function test")


    def back_fnc():
        print("back function test")


    def next_fnc():
        print("next function test")


    # print("here before run")
    lcd_display = LcdDisplay(toggle_pause_fnc, back_fnc, next_fnc)
    lcd_display.setDaemon(True)
    lcd_display.start()
    # print("here after run")
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
