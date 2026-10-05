from microbit import *
import random

# ----------------------------
# PARAMETERS
# ----------------------------
alpha = 0.5
gamma = 0.9
epsilon = 0.3

# ----------------------------
# GRID (3x3)
# States:
# (0,0)=0   (1,0)=1   (2,0)=2
# (0,1)=3   (1,1)=4   (2,1)=5
# (0,2)=6   (1,2)=7   (2,2)=8  <- goal
# ----------------------------

goal_state = 8


# Q-table: 9 states x 4 actions
Q = [[0 for _ in range(4)] for _ in range(9)]

# ----------------------------
# HELPER FUNCTIONS
# ----------------------------


def state_to_xy(state):
    x = state % 3
    y = state // 3
    return x, y

def xy_to_state(x, y):
    return y * 3 + x


# ----------------------------
# DISPLAY FUNCTION
# ----------------------------
def show_state(state):
    display.clear()
    
    # draw reward (dim)
    display.set_pixel(2, 2, 4)
    
    # draw agent (bright)
    x, y = state_to_xy(state)
    display.set_pixel(x, y, 9)

# ----------------------------

# ----------------------------
# ACTION EXECUTION
# ----------------------------

def get_next_state(state, action):
    x, y = state_to_xy(state)

    new_x, new_y = x, y

    if action == 0:    # UP
        new_y -= 1
    elif action == 1:  # DOWN
        new_y += 1
    elif action == 2:  # LEFT
        new_x -= 1
    elif action == 3:  # RIGHT
        new_x += 1


    # Check boundaries (NO wrapping now)
    if new_x < 0 or new_x > 2 or new_y < 0 or new_y > 2:
        return state, -5  # invalid move (it stays where it was), penalty

    new_state = xy_to_state(new_x, new_y)

    # reward system
    if new_state == goal_state:
        return new_state, 10
    else:
        return new_state, -1


# ----------------------------
# ACTION SELECTION
# ----------------------------
def choose_action(state):
    if random.random() < epsilon:
        return random.randint(0, 3)
    else:
        return Q[state].index(max(Q[state]))


# ----------------------------
# TRAINING EPISODE
# ----------------------------
def train_episode():
    state = 0

    while state != goal_state:
        show_state(state)

        action = choose_action(state)

        new_state, reward = get_next_state(state, action)

        # Q-learning update
        Q[state][action] += alpha * (reward + gamma * max(Q[new_state]) - Q[state][action])

        state = new_state

        sleep(600)

    # show goal reached
    display.show(Image.YES)
    sleep(800)

    
# ----------------------------
# MAIN LOOP
# ----------------------------
running = True
while running:
    train_episode()
    if button_a.was_pressed():
        running = False  # stop the loop



    

