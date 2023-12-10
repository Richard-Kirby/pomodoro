# Pomodoro Clock Requirements

## Initialisation
1. On initialisation, the Clock shall read the config file and configure accordingly.
2. The Clock shall provide some simple instructions on startup.
2. The Clock shall start in Normal Mode, with no Pomodoros active.

## Clock Display

### Displays
1. The Clock shall support multiple displays as interfaces, accepting commands from each to control the Clock. 

### Key Display Items 
1. Current time shall always be shown on the clock.
2. Current date shall always be shown on the clock. 
3. Weather shall be optionally shown on the clock.# Meh? 

### Display Modes
The Clock shall have the following modes:
1. Normal Mode - No pomodoro is active. Time is the main display, active Pomodoro times are displayed smaller. 
2. Pomodoro Mode - a pomodoro session is active, current time is displayed smaller, but still visible. 

#### Switching Display Modes
1. The Clock shall provide a mechanism to switch between Pomodoro mode and Normal Mode as desired.
2. The Clock shall keep any active Pomodoro timer in the same state (running or paused) when the mode is switched.

## Pomodoros
1. The Clock shall provide standard Pomodoro sequences as options to the user. 
2. The Clock shall provide a way for users to add custom Pomodoro sequences as desired. 
3. The Clock shall provide a way for users to select different Pomodoro sequences.
4. The Clock shall provide a way for users to pause/unpause the current Pomodoro timer. 
5. The Clock shall provide a way for users to rewind to the start of the current Pomodoro timer. 
6. The Clock shall provide a way for users to fastforward the current Pomodoro timer to the start of the next 
Pomodoro timer.
7. The Clock shall indicate the current type of Pomodoro (e.g. working or break)
8. The Clock shall indicate when a Pomodoro timer is completed. 
9. The Clock shall continue calculating the time for the current Pomodoro after it has expired until it is acknowledged.
10. The Clock shall show elapsed time on a Pomodoro via an image or series of images. 
11. Each Pomodoro timer will start in a Paused state.

## Demo Mode
Demo mode provides for a configurable speed-up in the time for any timers that are in use. This will be part of the 
config file, so it isn't accidently entered into. 

## Other Timers
1. The Clock shall provide standard non-Pomodoro timers. E.g. 1, 2, 5, 10, 20 minutes. # Not sure about this. 

## Configuration
1. The Clock shall allow for Demo mode to be entered via the configuration file. 
2. The clock shall provide a mechanism to enter custom Pomodoro timers via the config file.

## Sound
1. Sound will be muted on startup. 
2. Sound can be turned on/off via button press when in Normal Mode. 
3. 
 





