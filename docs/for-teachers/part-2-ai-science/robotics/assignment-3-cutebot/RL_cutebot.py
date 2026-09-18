from microbit import *
import cutebot  # adding the library
# cannot use this --> from Cutebot import *
import random

# cannot use this --> ct = CUTEBOT()

# ---------------------------------
# WHY THIS VERSION EXISTS
# ---------------------------------
# Back to the ORIGINAL open-loop calibration (SPEED=24, TURN_TIME=295,
# MOVE_TIME=500) as the base, with two small, targeted additions instead
# of a full closed-loop redesign:
#
#   - forward(): instead of a single blind timed move, the robot steers
#     with the two line sensors (bang-bang correction) for the WHOLE
#     MOVE_TIME window, so it tracks the physical tape from cell center
#     to cell center rather than just hoping it drove straight.
#
#   - turn_left()/turn_right(): still do the calibrated open-loop turn
#     first (this is usually close). Then, ONCE, check the sensor on the
#     side just turned toward (left sensor after turning left, right
#     sensor after turning right) - if it isn't on the line yet, nudge a
#     little further the same way for a fixed CORRECTION_TIME. That's it,
#     no loop, no repeated attempts: most turns just slightly undershoot,
#     so one small top-up fixes the common case.
#
# If the robot still isn't lined up after that (a bigger miss, or landed
# off the tape entirely), it's left as-is - there's no further automatic
# recovery. PAUSE_TIME at the end of every action gives you a window to
# reposition it by hand before the next action starts.

# ---------------------------------
# CALIBRATE THESE
# ---------------------------------

SPEED = 24         # original calibrated driving speed
MOVE_TIME = 600    # original calibrated forward time (one grid cell)
TURN_TIME = 350    # original calibrated turn time (90 degrees)
REST_TIME = 200    # brief settle pause right after each individual motor
                   # command stops

CORRECTION_TIME = 60   # ms - the single fixed top-up nudge after a turn,
                       # used only if the relevant sensor isn't on the
                       # line yet. Tune by eye: too short and it won't
                       # fix real undershoots, too long and it'll overturn.

STEER = 6          # bang-bang steering offset used while following the
                   # line during forward(). NOTE: SPEED=24 is close to
                   # this robot's ~22 motor stall floor, so keep STEER
                   # small - if a wheel visibly stalls instead of curving
                   # during a correction, LOWER STEER rather than raising it.
POLL_MS = 20       # how often the line sensors are checked during forward()

START_CREEP_MS = 80   # tiny forward nudge before the very first turn of the
                       # episode, so the robot isn't sitting exactly on cell
                       # 0's intersection (where the E/S tape arms overlap
                       # the sensors and can fool the post-turn check)

PAUSE_TIME = 4000  # pause at the end of each action so you can check the
                   # robot against the displayed state and reposition it
                   # by hand if needed, before the next action starts

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
    cutebot.set_motors_speed(0,0)

def forward():
    # follows the black line for the whole MOVE_TIME window instead of
    # just driving straight blind
    t0 = running_time()

    while running_time() - t0 < MOVE_TIME:
        l = cutebot.has_left_track()
        r = cutebot.has_right_track()

        if l and not r:
            # drifted right of the tape -> curve left to recenter
            cutebot.set_left_rgb_led(255, 0, 0)
            cutebot.set_right_rgb_led(0, 0, 0)
            cutebot.set_motors_speed(SPEED - STEER, SPEED)

        elif r and not l:
            # drifted left of the tape -> curve right to recenter
            cutebot.set_left_rgb_led(0, 0, 0)
            cutebot.set_right_rgb_led(255, 0, 0)
            cutebot.set_motors_speed(SPEED, SPEED - STEER)

        else:
            # centered (both black) or between segments (both white) -> straight
            cutebot.set_left_rgb_led(0, 255, 0)
            cutebot.set_right_rgb_led(0, 255, 0)
            cutebot.set_motors_speed(SPEED, SPEED)

        sleep(POLL_MS)

    stop()
    cutebot.set_left_rgb_led(0, 0, 0)
    cutebot.set_right_rgb_led(0, 0, 0)
    sleep(REST_TIME)

def turn_left():
    cutebot.set_motors_speed(-SPEED, SPEED)
    sleep(TURN_TIME)
    stop()
    sleep(REST_TIME)

    # most turns underturn a bit - if the side we just turned toward
    # isn't on the line yet, nudge a little further the same way, once
    if not cutebot.has_left_track():
        cutebot.set_left_rgb_led(255, 0, 0)
        cutebot.set_motors_speed(-SPEED, SPEED)
        sleep(CORRECTION_TIME)
        stop()
        sleep(REST_TIME)
        cutebot.set_left_rgb_led(0, 0, 0)

def turn_right():
    cutebot.set_motors_speed(SPEED, -SPEED)
    sleep(TURN_TIME)
    stop()
    sleep(REST_TIME)

    if not cutebot.has_right_track():
        cutebot.set_right_rgb_led(255, 0, 0)
        cutebot.set_motors_speed(SPEED, -SPEED)
        sleep(CORRECTION_TIME)
        stop()
        sleep(REST_TIME)
        cutebot.set_right_rgb_led(0, 0, 0)

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

    # tiny creep off the starting intersection before the first turn -
    # otherwise the first turn's post-turn sensor check can be fooled by
    # sitting right on cell 0's tape intersection
    cutebot.set_motors_speed(SPEED, SPEED)
    sleep(START_CREEP_MS)
    stop()
    sleep(REST_TIME)

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

        sleep(PAUSE_TIME)

# ---------------------------------
# MAIN
# ---------------------------------

display.scroll("A")

while True:

    if button_a.was_pressed():

        run_episode()

        display.show(Image.HAPPY)
