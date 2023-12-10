# Design

On startup, the clock will read the config file and configure itself accordingly. This includes any custom Pomodoros 
that the user has entered. It will start in Normal Mode with no active Pomodoro sequence. 

The initialisation sequence will provide some simple instructions for getting started. 

# Displays 
The system allows multiple displays that operate on the same clock, so each affects timers, etc. Each display can have 
its own mode, but otherwise have the same state. 

# Clock Face

In Normal Mode, the current time and date will be prominently displayed. If there are no active Pomodoro sequence, it 
shall indicate how to start a sequence. 

# Button Presses
A button will initiate selecting a Pomodoro sequence to start. 
X and Y buttons can then select the Pomodoro sequence. 
A will confirm the sequence.
B will back out of the sequence and into Normal Mode if in Pomodoro Display Mode. 

Once started, the Y button will pause or unpause the current timer. Pressing the A button will rewind to the start of
the current timer and pressing the X button will fastforward through the current timer to the next timer, which will 
not be started until un-paused by pressing the Y button. 


# Configuration
The config file allows for demo mode to be turned on/off, for custom Pomodoros, sound on/off, 


