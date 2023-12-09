import datetime
import threading

import time
import test
import timers.timer_seq as timer_seq


# Main class for the clock
class Clock(threading.Thread):
    def __init__(self, timer_speed=1):
        super().__init__()
        self.timer_speed=1
        self.timer_seq_mgr = timer_seq.TimerSequenceManager(speed=timer_speed)
        self.current_time = datetime.datetime.now()
        self.current_timer_seq = self.timer_seq_mgr.timer_seq

    def run(self):
        while(True):
            self.current_time = datetime.datetime.now()
            print(self.current_time)
            self.current_timer_seq.decrement_current_timer()
            time.sleep(1)

if __name__ == '__main__':
    clock = Clock(5);
    clock.run()

        