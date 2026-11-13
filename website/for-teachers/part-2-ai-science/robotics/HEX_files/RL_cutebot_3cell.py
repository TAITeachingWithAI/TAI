from microbit import *
from time import sleep_us
from machine import time_pulse_us

CUTEBOT_ADDR = 0x10
left = 0x04
right = 0x08


class CUTEBOT(object):
    def __init__(self):
        i2c.init()
        self.__pin_e = pin12
        self.__pin_t = pin8
        self.__pinL = pin13
        self.__pinR = pin14
        self.__pinL.set_pull(self.__pinL.PULL_UP)
        self.__pinR.set_pull(self.__pinR.PULL_UP)

    def set_motors_speed(self, left_wheel_speed: int, right_wheel_speed: int):
        if left_wheel_speed > 100 or left_wheel_speed < -100:
            raise ValueError('speed error,-100~100')
        if right_wheel_speed > 100 or right_wheel_speed < -100:
            raise ValueError('speed error,-100~100')
        left_direction = 0x02 if left_wheel_speed > 0 else 0x01
        right_direction = 0x02 if right_wheel_speed > 0 else 0x01
        left_wheel_speed = left_wheel_speed if left_wheel_speed > 0 else left_wheel_speed * -1
        right_wheel_speed = right_wheel_speed if right_wheel_speed > 0 else right_wheel_speed * -1
        i2c.write(CUTEBOT_ADDR, bytearray(
            [0x01, left_direction, left_wheel_speed, 0]))
        i2c.write(CUTEBOT_ADDR, bytearray(
            [0x02, right_direction, right_wheel_speed, 0]))

    def set_car_light(self, light: int, R: int, G: int, B: int):
        if R > 255 or G > 255 or B > 255:
            raise ValueError('RGB is error')
        i2c.write(CUTEBOT_ADDR, bytearray([light, R, G, B]))

    def get_distance(self, unit: int = 0):
        self.__pin_e.read_digital()
        self.__pin_t.write_digital(1)
        sleep_us(10)
        self.__pin_t.write_digital(0)
        ts = time_pulse_us(self.__pin_e, 1, 25000)
        distance = round(ts * 34 / 2 / 1000)
        if unit == 0:
            return distance
        elif unit == 1:
            return round(distance / 30.48, 2)

    def get_tracking(self):
        left = self.__pinL.read_digital()
        right = self.__pinR.read_digital()
        if left == 1 and right == 1:
            return 00
        elif left == 0 and right == 1:
            return 10
        elif left == 1 and right == 0:
            return 1
        elif left == 0 and right == 0:
            return 11
        else:
            print("Unknown ERROR")

    def set_servo(self, servo, angle):
        if servo > 2 or servo < 1:
            raise ValueError('select servo error,1,2')
        if angle > 180 or angle < 0:
            raise ValueError('angle error,0~180')
        i2c.write(CUTEBOT_ADDR, bytearray([servo + 4, angle, 0, 0]))


import random

ct = CUTEBOT()

# --- calibration, from Assignment: Calibrate your rover ---
SPEED = 24
MOVE_TIME = 600      # ms per grid cell (~13.3 cm cells)
TURN_TIME = 300      # ms per 90-degree turn

# --- grid definition: a straight line of 3 cells, numbered 0, 1, 2 ---
GOAL = 2

NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3
ACTIONS = [NORTH, EAST, SOUTH, WEST]
heading = EAST


# basic movements
def forward():
    ct.set_motors_speed(SPEED, SPEED)
    sleep(MOVE_TIME)
    ct.set_motors_speed(0, 0)


def turn_left():
    ct.set_motors_speed(-SPEED, SPEED)
    sleep(TURN_TIME)
    ct.set_motors_speed(0, 0)


def turn_right():
    ct.set_motors_speed(SPEED, -SPEED)
    sleep(TURN_TIME)
    ct.set_motors_speed(0, 0)


def rotate_to(target):
    global heading
    diff = (target - heading) % 4
    if diff == 1:
        turn_right()
    elif diff == 2:
        turn_right()
        sleep(200)
        turn_right()
    elif diff == 3:
        turn_left()
    heading = target


# the memory table: one row per cell, one column per action -- all slots start at 0
table = [[0, 0, 0, 0] for _ in range(3)]


# which cell does "action" lead to from "state"? (also carries the reward)
def next_state(state, action):
    if action == EAST:
        if state + 1 > GOAL:
            return state, -10      # hit the edge, stays in place
        ns = state + 1
    elif action == WEST:
        if state - 1 < 0:
            return state, -10      # hit the edge, stays in place
        ns = state - 1
    else:
        return state, -10          # NORTH/SOUTH: no such move in this corridor
    return (ns, 10) if ns == GOAL else (ns, -1)


# choose an action using the table (ties broken randomly)
def choose_action(state):
    best_value = max(table[state])
    candidates = [a for a in ACTIONS if table[state][a] == best_value]
    return random.choice(candidates)


# one interaction: choose an action, move, get the reward, update the table
def interaction(state):
    action = choose_action(state)
    ns, reward = next_state(state, action)
    rotate_to(action)
    if ns != state:
        forward()
    table[state][action] = reward     # overwrite, no learning rate
    if reward == 10:
        display.show(Image.HEART)
    return ns, reward


# loop over a full episode
def run_episode():
    global heading
    heading = EAST
    state = 0
    total_reward = 0
    while state != GOAL:
        state, reward = interaction(state)
        total_reward += reward
        display.show(str(state))
        sleep(1500)
    display.show(Image.HAPPY)
    sleep(300)
    display.scroll(str(total_reward))


display.scroll("A")
while True:
    if button_a.was_pressed():
        run_episode()
