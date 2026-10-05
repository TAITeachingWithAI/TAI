# Backup solution -- Task 2: turn 90 degrees on the spot.
# Only use this if your team is completely stuck after trying with the AI!
from microbit import *
from Cutebot import *

ct = CUTEBOT()

SPEED = 30        # tweak this
TURN_TIME = 350   # ms -- tweak until the rover turns exactly 90 degrees

ct.set_motors_speed(SPEED, -SPEED)   # turn right
sleep(TURN_TIME)
ct.set_motors_speed(0, 0)
