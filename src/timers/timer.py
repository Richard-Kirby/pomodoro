#!/usr/bin/env python3
from __future__ import annotations
from timers.test import Test

from abc import ABC


# Timer Factory creates timers as requested.
class TimerFactory:
    def __init__(self):
        pass

    @staticmethod
    def get_timer(timer_type, name, description, length_sec) -> Timer:
        if timer_type == 'Work':
            return WorkTimer(name, description, length_sec)
        elif timer_type == 'Break':
            return BreakTimer(name, description, length_sec)

        else:
            print("Unrecognised timer type")


# Abstract Timer class for dealing with an individual timer.
class Timer(ABC):
    def __init__(self, name, description, length_sec: int):

        # Make sure name isn't blank.
        if len(name) > 0:
            self.name = name
        else:
            raise ValueError(f"Name can't be blank name={name}")

        # Make sure timer is more than 0 sec.
        if length_sec > 0:
            self.length_sec = length_sec
        else:
            raise ValueError(f"Timer length must be greater than 0 seconds length ={length_sec}")

        # Description can be anything, including blank.
        self.description = description
        self.time_remaining = self.length_sec

        # start off with paused state.
        self._state = "paused"
        self.type = None
        self.colour = '000000'

        # keep track of the overrun of a given timer.
        self.overrun_time = 0

    # Start or unpause.
    def start(self):
        self._state = 'running'

    # Change state to be paused or un-paused. Might already be paused.
    def toggle_pause(self):
        if self._state == 'paused':
            self._state = 'running'
        elif self._state == 'running':
            self._state == 'paused'
        else:
            raise ValueError

    # Restart the timer - this cancels any time spent. Goes immediately to running, not paused.
    # Overrun time is also reset as the timer should be ready for another use.
    def restart(self):
        self._state = 'running'
        self.time_remaining = self.length_sec
        self.overrun_time = 0

    # Complete the timer, by setting state to complete and remaining time to 0.
    def complete(self):
        self._state = 'complete'
        self.time_remaining = 0
        # self.overrun_time = 0

    # Decrement the timer by 1s, note that this might be faster than real time for testing purposes.
    def decrement_time(self):
        if self._state == 'running':
            self.time_remaining -= 1  # Subtract one second from the remaining.

            # Mark timer as complete if counts down to zero.
            if self.time_remaining == 0:
                self.complete()
        # Keep counting even if complete - useful to know how much the timer has been overrun.
        elif self._state == 'complete':
            self.overrun_time -= 1
        else:
            pass  # Don't decrement if paused.
            # print(f"Not decrementing as state is {self._state}")

    # Print the current state of the timer
    def return_state_str(self):
        return f"timer name: {self.name} state: {self._state} remaining: {self.time_remaining} "\
               f"overrun: {self.overrun_time}"

    # Return the timer type
    def return_type(self):
        return self.type

    # Return the timer's colour.
    def return_colour(self):
        return self.colour


# Concrete Work Timer Class.
class WorkTimer(Timer):
    def __init__(self, name, description, length_sec: int):
        super().__init__(name, description, length_sec)
        self.type = 'Work'
        self.colour = 'FF0000'


# Concrete Break Timer Class.
class BreakTimer(Timer):
    def __init__(self, name, description, length_sec: int):
        super().__init__(name, description, length_sec)
        self.type = 'Break'
        self.colour = '00FF00'


# Tests
if __name__ == '__main__':

    tests = []

    work1 = WorkTimer("work1", 'work 1 timers', 25*60)

    # cont equivalent of 30 minutes. Should not decrement as timer is paused.
    for i in range(30*60):
        work1.decrement_time()

    if work1.time_remaining == 25 * 60:
        tests.append(Test("Paused", "passed"))
    else:
        tests.append(Test("Paused", "failed"))

    # Change state to running and try again.
    work1.start()

    # Cont equivalent of 30 minutes. Should not decrement as timer is paused.
    for i in range(30*60):
        work1.decrement_time()

    if work1.overrun_time == -5*60:
        tests.append(Test("Over-run timer", "passed"))
    else:
        tests.append(Test("Over-run timer", "failed",
                          "failed test, should be 5*60, but is {work1.overrun_time}"))

    break1 = BreakTimer('break1', 'break timer', 5*60)
    print(break1.return_state_str())

    # Change state to running and try again.
    break1.start()

    # Cont equivalent of 3 minutes.
    for i in range(3 * 60):
        break1.decrement_time()

    # restart the timer.
    break1.restart()
    if break1.time_remaining == 5 * 60:
        tests.append(Test("restart", "passed"))
    else:
        tests.append(Test("restart", "failed",
                          f"failed test, should be 5*60, but is {break1.time_remaining}"))

    for i in range(6 * 60):
        break1.decrement_time()

    if break1.overrun_time == -1 * 60:
        tests.append(Test("restart", "passed"))
    else:
        tests.append(Test("restart", "failed",
                          f"failed test, should be -1*60, but is {break1.overrun_time}"))

    result_str = f"{work1.return_colour()}, {break1.return_colour()}, {work1.return_type()}, {break1.return_type()}"

    if result_str == 'FF0000, 00FF00, Work, Break':
        tests.append(Test("colour", "passed"))
    else:
        tests.append(Test("colour", "failed"))

    try:
        faulty_work = Timer("", "", 300)
    except ValueError:
        tests.append(Test("exception", "passed"))
    else:
        tests.append(Test("exception", "failed", "should have excepted"))

    try:
        faulty_work = Timer("except", "", 0)
    except ValueError:
        tests.append(Test("exception", "passed"))
    else:
        tests.append(Test("exception", "failed", "should have excepted"))

    timer_factory = TimerFactory()

    timer1 = timer_factory.get_timer("Work", "Work from Factory", "work timer", 120)
    timer2 = timer_factory.get_timer("Break", "Break from Factory", "break timer", 120)
    print(timer1)
    print(timer2)

    timer1.start()
    for i in range(125):
        timer1.decrement_time()

    if timer1.return_state_str() == 'timer name: Work from Factory state: complete remaining: 0 overrun: -5':
        tests.append(Test("Factory Work", "passed"))
    else:
        tests.append(Test("Factory Work", "failed"))

    print(timer1.return_state_str())

    timer2.start()
    for i in range(100):
        timer2.decrement_time()

    print(timer2.return_state_str())
    if timer2.return_state_str() == 'timer name: Break from Factory state: running remaining: 20 overrun: 0':
        tests.append(Test("Factory Break", "passed"))
    else:
        tests.append(Test("Factory Break", "failed"))

    for i in range(len(tests)):
        print(tests[i].return_result())
