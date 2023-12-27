import timers.timer as timer
from timers.test import Test
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('raspidoroLogger')


# Class to manage the available timer sequences. This is just a shell at the moment.
# ToDo: add more sequences and the necessary functions to manage them.
class TimerSequenceManager:
    def __init__(self, speed=1):
        self.speed = speed
        self.timer_seq = TimerSequence(self.speed)


# Class to manage the current sequence.
class TimerSequence:
    def __init__(self, speed=1):
        self.timer_factory = timer.TimerFactory()
        self.timer_seq = []
        self.current_timer = None
        self.create_sequence()

        # Allows for faster than real time for testing/demo purposes.
        self.speed = speed

    # Create the timer sequence.
    def create_sequence(self):
        # Initial timer list ToDo: make more flexible by adding more timer sequences.
        timer_list = [
            ['Work', 'Work 1', 'Work', 25 * 60],
            ['Break', 'Break 1', 'Short Break - Stretch', 5 * 60],
            ['Work', 'Work 2', 'Standing Work', 25 * 60],
            ['Break', 'Break 2', 'Short Break - Water', 5 * 60],
            ['Work', 'Work 3', 'Work', 25 * 60],
            ['Break', 'Break 3', 'Long Break - Exercise', 15 * 60]
        ]

        for item in timer_list:
            self.timer_seq.append(self.timer_factory.get_timer(*item))

        # for item in self.timer_seq:
        #    print(item.return_state_str())

        self.current_timer = self.timer_seq.pop(0)

    # Decrement the current timer according to set speed, which may be different from real time.
    def decrement_current_timer(self):
        # Decrement the current timer in relation to the current speed, which may be different from real time.
        for count in range(self.speed):
            self.current_timer.decrement_time()

    # Toggle the pause on the current timer.
    def toggle_pause_current_timer(self):
        self.current_timer.toggle_pause()

    #Restart the current timer.
    def restart_current_timer(self):
        self.current_timer.restart()

    # Restarting sequence just creates the sequence again.
    def restart_sequence(self):
        self.create_sequence()

    # Go to the next timer.
    def next_timer(self):  #
        # Restart the current timer -just resetting it.
        logger.info(f"Current timer {self.current_timer.return_state_str()}")
        self.current_timer.restart()

        # Append the current timer to the end of the timer sequence.
        self.timer_seq.append(self.current_timer)
        self.current_timer = self.timer_seq.pop(0)
        self.current_timer.start()
        logger.info(f"Current timer {self.current_timer.return_state_str()}")


if __name__ == '__main__':
    tests = []

    timer_seq_mgr = TimerSequenceManager()
    timer_seq = timer_seq_mgr.timer_seq
    timer_seq.current_timer.start()
    state = None

    for i in range(30 * 60):
        timer_seq.decrement_current_timer()
        state = timer_seq.current_timer.return_state_str()
        print(state)

    if state == 'timer name: Work 1 state: complete remaining: 0 overrun: -300':
        tests.append(Test(__file__, "Work 1 test", "passed"))
    else:
        tests.append(Test(__file__, "Work 1 test", "failed"))

    # Try faster timers
    timer_seq_mgr = TimerSequenceManager(speed=15)
    timer_seq = timer_seq_mgr.timer_seq
    timer_seq.current_timer.start()
    state = None

    for i in range(30 * 4):
        timer_seq.decrement_current_timer()
        state = timer_seq.current_timer.return_state_str()
        print(state)

    if state == 'timer name: Work 1 state: complete remaining: 0 overrun: -300':
        tests.append(Test(__file__, "Work 1 test", "passed"))
    else:
        tests.append(Test(__file__, "Work 1 test", "failed"))

    # Go to the next timer.
    timer_seq.next_timer()

    # print(timer_seq.current_timer.return_state_str())

    if timer_seq.current_timer.return_state_str() == 'timer name: Break 1 state: paused remaining: 300 overrun: 0':
        tests.append(Test(__file__, "Next Timer", "passed"))
    else:
        tests.append(Test(__file__, "Next Timer", "failed"))

    for timer in timer_seq.timer_seq:
        print(timer.return_state_str())

    for test in tests:
        print(test.return_result())
