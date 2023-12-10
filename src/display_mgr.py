from abc import ABC
import clock
import test


class Display(ABC):

    # Width and length is desired display size or desired window size depending on the type of display.
    def __init__(self, width, length, pins = None):
        self.width = width
        self.length = length
        self.pins = pins
        self._display_mode
    def

# Class to manage the common parts of the different displays.
class DisplayManager:

    def __init__(self, speed):
        self.speed = speed
        self.clock = clock(speed=self.speed)
        self.clock.start()
        self._modes = ['clock', 'pomodoro']
        self._curr_mode = self._modes.pop(0)
        self.top_left_button_function = None
        self.bottom_left_button_function = None
        self.top_right_button_function = None
        self.bottom_right_function = None

    # Change modes
    def change_mode(self):
        self._modes.append(self._curr_mode)
        self._curr_mode = self._modes.pop(0)

        # Set up button functions by setting them to function calls.
        if self._curr_mode == 'clock':
            self.top_left_button_function = self.back
            self.top_right_button_function = self.pause
            self.bottom_left_button_function = self.rewind
            self.top_right_button_function = self.fastforward
        elif self._curr_mode == 'pomodoro':
            self.top_left_button_function = self.back
            self.top_right_button_function = self.pause
            self.bottom_left_button_function = self.rewind
            self.top_right_button_function = self.fastforward
        else:
            raise ValueError

    def pause(self):
        pass

    def back(self):
        pass

    def rewind(self):
        pass

    def fastforward(self):
        pass

    def top_left_button_press(self):
        print("top left button press")

    def bottom_left_button_press(self):
        print("bottom left button press")

    def top_right_button_press(self):
        print("top right button press")

    def bottom_right_button_press(self):
        print("bottom right button press")


