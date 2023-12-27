#!/usr/bin/python3

import datetime
import threading

import time
import test
import display
import timers.timer_seq as timer_seq


# Main class for the clock
class Clock(threading.Thread):
    def __init__(self, timer_speed=1):
        super().__init__()
        self.timer_speed = timer_speed
        self.timer_seq_mgr = timer_seq.TimerSequenceManager(speed=self.timer_speed)
        self.current_time = datetime.datetime.now()
        self.current_timer_seq = self.timer_seq_mgr.timer_seq

        # Set up and get the LCD display running.
        self.lcd_display = display.LcdDisplay(self.timer_seq_mgr.timer_seq.toggle_pause_current_timer,
                                              self.timer_seq_mgr.timer_seq.restart_current_timer,
                                              self.timer_seq_mgr.timer_seq.next_timer)
        
        # self.lcd_display.setDaemon(True)
        self.current_data = display.CurrentData()
        self.current_data.current_timer_data = display.CurrentTimerData(
            self.current_timer_seq.current_timer.name,
            self.current_timer_seq.current_timer.description,
            self.current_timer_seq.current_timer.length_sec,
            self.current_timer_seq.current_timer.return_colour())
        self.lcd_display.start()

    # Decrements the current timer and returns the data
    def decrement_current_timer(self):
        current_timer_data = display.CurrentTimerData(self.current_timer_seq.current_timer.name,
                                                      self.current_timer_seq.current_timer.description,
                                                      self.current_timer_seq.current_timer.length_sec,
                                                      self.current_timer_seq.current_timer.return_colour())

        self.current_timer_seq.decrement_current_timer()

        if self.current_timer_seq.current_timer.time_remaining == 0:
            current_timer_data.remaining_timer_s = self.current_timer_seq.current_timer.overrun_time
        else:
            current_timer_data.remaining_timer_s = self.current_timer_seq.current_timer.time_remaining

        return current_timer_data

    # Main function that runs as part of the thread. Ticks time down and gets current time for display as needed.
    def run(self):
        while True:
            self.current_data.current_datetime = datetime.datetime.now()
            self.current_data.current_timer_data = self.decrement_current_timer()
            self.lcd_display.current_data_queue.put_nowait(self.current_data)

            # print(f"Queue {lcd_display.current_data_queue.get_nowait()}")
            # Once counted down to zero, send the overrun time.
            # print(self.current_timer_seq.current_timer.return_state_str())
            time.sleep(1)


if __name__ == '__main__':
    clock = Clock(1)
    clock.current_timer_seq.current_timer.start()
    clock.setDaemon(True)
    clock.start()
