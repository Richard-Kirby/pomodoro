#!/usr/bin/env python3
from abc import abstractmethod, ABC, abstractproperty


class Timer(ABC):
    def __init__(self, name, description, length_sec: int):

        # Make sure name isn't blank.
        if len(name)>0:
            self.name = name
        else:
            raise ValueError(f"Name can't be blank name={name}")

        # Make sure timer is more than 0 sec.
        if length_sec >0:
            self.length_sec = length_sec
        else:
            raise ValueError(f"Timer length must be greater than 0 seconds length ={length_sec}")

        # Desciption can be anything, including blank.
        self.description = description
        self.time_remaining = self.length_sec

        # start off with paused state.
        self._state = "paused"
        self.type = None
        self.colour = '000000'
        self.overrun_time = 0

    # Start of unpause.
    def start(self):
        self._state = 'running'

    # change state to paused. Might already be paused.
    def pause(self):
        self._state = 'paused'

    def restart(self):
        self._state = 'running'
        self.time_remaining = self.length_sec

    def complete(self):
        self._state = 'complete'
        self.time_remaining = 0
        self.overrun_time = 0

    def decrement_time(self):
        if self._state == 'running':
            self.time_remaining -= 1  # Subtract one second from the remaining.

            # Mark timer as complete if counts down to zero.
            if self.time_remaining == 0:
                self.complete()

        elif self._state == 'complete':
            self.overrun_time -= 1
        else:
            print(f"Not decrementing as state is {self._state}")



    def print_state(self):
        # logger.debug(f"timername: {self.name} state: {self._state} remaining: {self.time_remaining}")
        print(f"timer name: {self.name} state: {self._state} remaining: {self.time_remaining} "
              f"overrun: {self.overrun_time}")

    def return_type(self):
        return self.type

    def return_colour(self):
        return self.colour


class WorkTimer(Timer):
    def __init__(self, name, description, length_sec: int):
        super().__init__(name, description, length_sec)
        self.type = 'Work'
        self.colour = 'FF0000'


class BreakTimer(Timer):
    def __init__(self, name, description, length_sec: int):
        super().__init__(name, description, length_sec)
        self.type = 'Break'
        self.colour = '00FF00'


if __name__ == '__main__':
    work1 = WorkTimer("work1", 'work 1 timers', 25*60)
    work1.print_state()

    # cont equivalent of 30 minutes. Should not decrement as timer is paused.
    for i in range(30*60):
        work1.decrement_time()
        work1.print_state()

    if work1.time_remaining == 25 *60:
        print("test passed")
    else:
        print(f"failed test, should be 25*60, but is {work1.time_remaining}")

    # Change state to running and try again.
    work1.start()

    # Cont equivalent of 30 minutes. Should not decrement as timer is paused.
    for i in range(30*60):
        work1.decrement_time()
        work1.print_state()

    if work1.overrun_time == -5*60:
        print(f"Passed Test {work1.overrun_time}")
    else:
        print(f"failed test, should be 5*60, but is {work1.overrun_time}")


    break1 = BreakTimer('break1', 'break timer', 5*60)
    break1.print_state()

    # Change state to running and try again.
    break1.start()

    # Cont equivalent of 3 minutes.
    for i in range(3 * 60):
        break1.decrement_time()
        break1.print_state()

    #restart the timer.
    break1.restart()
    if break1.time_remaining != 5 *60:
        print("test failed")
    else:
        print("test passed")

    for i in range(6 * 60):
        break1.decrement_time()
        break1.print_state()

    if break1.overrun_time == -1 * 60:
        print(f"Passed Test {break1.overrun_time}")
    else:
        print(f"failed test, should be -1*60, but is {break1.overrun_time}")

    result_str = f"{work1.return_colour()}, {break1.return_colour()}, {work1.return_type()}, {break1.return_type()}"

    if result_str == 'FF0000, 00FF00, Work, Break':
        print("test passed")
    else:
        print("test failed")

    try:
        faulty_work = Timer("", "", 300)
    except:
        print("Exception Test Passed")

    try:
        faulty_work = Timer("except", "", 0)
    except:
        print("Exception Test Passed")





