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
        self.timer_speed = 1
        self.timer_seq_mgr = timer_seq.TimerSequenceManager(speed=timer_speed)
        self.current_time = datetime.datetime.now()
        self.current_timer_seq = self.timer_seq_mgr.timer_seq
        self.current_timer = self.current_timer_seq.current_timer
        self.hat_display = display.LcdDisplay(self.current_timer.toggle_pause,
                                              self.current_timer.back,
                                              self.current_timer.complete)

    # Main function that runs as part of the thread. Ticks time down and gets current time for display as needed.
    def run(self):
        while True:
            self.current_time = datetime.datetime.now()
            print(self.current_time)
            self.current_timer_seq.decrement_current_timer()
            print(f'{self.current_timer.return_state_str()}')
            time.sleep(1)


if __name__ == '__main__':
    clock = Clock(15)
    clock.current_timer.start()
    clock.run()
