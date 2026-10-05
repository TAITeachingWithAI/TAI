# Backup solution -- Task 1: drive forward one grid cell.
# Only use this if your team is completely stuck after trying with the AI!
from microbit import *
from Cutebot import *

ct = CUTEBOT()

SPEED = 30        # tweak this
MOVE_TIME = 200   # ms -- tweak until the rover crosses exactly one grid cell

ct.set_motors_speed(SPEED, SPEED)
sleep(MOVE_TIME)
ct.set_motors_speed(0, 0)
