from abc import ABC, abstractmethod
from __future__ import annotations

from displayhatmini import DisplayHATMini
import test


class Display(ABC):

    # Width and length is desired display size or desired window size depending on the type of display.
    def __init__(self, width, height, toggle_pause_function, back_function, next_function, pins = None):
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

    def update_data(curr_date_time, pomodoro_time_state):
            self.current_time = curr_date_time
            self.pomodoro_time_state = pomodoro_time_state

    @abstractmethod
    def update_display(self):
        pass


# Class for LCD - in this case the DisplayHatMini
class LcdDisplay(Display):
    def __init__(self, toggle_pause_function, back_function, next_function):

        displayhatmini = DisplayHATMini()

        pins = [displayhatmini.BUTTON_A, displayhatmini.BUTTON_B,displayhatmini.BUTTON_X,displayhatmini.BUTTON_Y]

        super.__init__(displayhatmini.WIDTH, displayhatmini.HEIGHT, toggle_pause_function, back_function,
                       next_function, pins)

        # Set the current mode
        self.change_mode()

        # Mapping to mode to buttons and functions.
        self.function_dict = {'clock':{displayhatmini.BUTTON_A:self.change_mode(),
                                       displayhatmini.BUTTON_B:self.toggle_pause_function,
                                       displayhatmini.BUTTON_X: self.back_function,
                                       displayhatmini.BUTTON_Y: self.next_function},
                              'pomodoro':{displayhatmini.BUTTON_A:self.change_mode(),
                                          displayhatmini.BUTTON_B:self.toggle_pause_function,
                                          displayhatmini.BUTTON_X: self.back_function,
                                          displayhatmini.BUTTON_Y: self.next_function}}

    # Rotate through the modes.
    def change_mode(self):
        super().change_mode()

    # Update the display to show the latest state.
    def update_display(self):
        pass




