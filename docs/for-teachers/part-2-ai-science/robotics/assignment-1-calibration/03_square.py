# Backup solution -- Task 3: walk a square (4 cells).
# Only use this if your team is completely stuck after trying with the AI!
from microbit import *
from Cutebot import *

ct = CUTEBOT()

SPEED = 30
MOVE_TIME = 200   # from Task 1
TURN_TIME = 350   # from Task 2

def forward():
    ct.set_motors_speed(SPEED, SPEED)
    sleep(MOVE_TIME)
    ct.set_motors_speed(0, 0)

def turn_right():
    ct.set_motors_speed(SPEED, -SPEED)
    sleep(TURN_TIME)
    ct.set_motors_speed(0, 0)

for i in range(4):
    forward()
    turn_right()
