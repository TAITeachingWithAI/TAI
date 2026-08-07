from microbit import *
from Cutebot import *
import random

ct = CUTEBOT()

# ---------------------------------
# CALIBRATE THESE
# ---------------------------------

MOVE_TIME = 200      # ms for 6 cm
TURN_TIME = 350      # ms for 90°

SPEED = 30

# ---------------------------------
# RL PARAMETERS
# ---------------------------------

ALPHA = 0.5
GAMMA = 0.9
EPSILON = 0.3

GOAL = 8

# ---------------------------------
# STATE
# ---------------------------------

Q = []

for i in range(9):
    Q.append([0,0,0,0])

# headings

NORTH = 0
EAST  = 1
SOUTH = 2
WEST  = 3

heading = EAST

# ---------------------------------
# MOTOR HELPERS
# ---------------------------------

def stop():
    ct.set_motors_speed(0,0)

def forward():
    ct.set_motors_speed(SPEED,SPEED)
    sleep(MOVE_TIME)
    stop()

def turn_left():
    ct.set_motors_speed(-SPEED,SPEED)
    sleep(TURN_TIME)
    stop()

def turn_right():
    ct.set_motors_speed(SPEED,-SPEED)
    sleep(TURN_TIME)
    stop()

def rotate_to(target):

    global heading

    diff = (target - heading) % 4

    if diff == 1:
        turn_right()

    elif diff == 2:
        turn_right()
        sleep(100)
        turn_right()

    elif diff == 3:
        turn_left()

    heading = target

# ---------------------------------
# GRID
# ---------------------------------

def row(state):
    return state // 3

def col(state):
    return state % 3

def next_state(state, action):

    r = row(state)
    c = col(state)

    if action == NORTH:
        r -= 1

    elif action == EAST:
        c += 1

    elif action == SOUTH:
        r += 1

    elif action == WEST:
        c -= 1

    if r < 0 or r > 2:
        return state, -5

    if c < 0 or c > 2:
        return state, -5

    ns = r*3 + c

    if ns == GOAL:
        return ns, 10

    return ns, -1

# ---------------------------------
# ACTION CHOICE
# ---------------------------------

def choose_action(state):

    if random.random() < EPSILON:
        return random.randint(0,3)

    best = 0

    for a in range(1,4):
        if Q[state][a] > Q[state][best]:
            best = a

    return best

# ---------------------------------
# EPISODE
# ---------------------------------

def run_episode():

    global heading

    heading = EAST

    state = 0

    while state != GOAL:

        action = choose_action(state)

        ns, reward = next_state(state, action)

        if reward > 0:
            display.show(Image.HEART)
        
        rotate_to(action)

        if ns != state:
            forward()

        best_next = max(Q[ns])

        Q[state][action] = (
            Q[state][action]
            + ALPHA * (
                reward
                + GAMMA * best_next
                - Q[state][action]
            )
        )

        state = ns

        display.show(str(state))

        sleep(2000)

# ---------------------------------
# MAIN
# ---------------------------------

display.scroll("A")

while True:

    if button_a.was_pressed():

        run_episode()

        display.show(Image.HAPPY)