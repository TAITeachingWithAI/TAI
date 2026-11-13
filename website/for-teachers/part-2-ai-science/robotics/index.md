---
title: Robotics
order: 5
---

# Robotics

Teaching material for the robotics lesson of Part 2: AI & Science, **"A rover
that learns the fastest path"**. Students first act out reinforcement learning
themselves (one student is the robot, the others are the environment), and then
make a real Cutebot robot with a micro:bit learn the fastest path across a
small printed grid. In the second assignment they choose one of three levels,
from running ready-made code to programming everything themselves with the help
of an AI.

## Lesson material

- [:material-file-pdf-box: Robotics lesson: student version](Robotics_student.pdf)
- [:material-file-pdf-box: Robotics lesson: teacher version](Robotics_teacher.pdf)

!!! info "Which version do I need?"
    The **student version** is the worksheet you hand out. The **teacher version**
    is the same lesson including the worked answers, for your own preparation.

## Levels and timing

| Level | What students do | Duration of the whole lesson |
| --- | --- | --- |
| 1 | The AI already wrote the code: students read it, find its functions, and flash it. | about 2 h 25 min |
| 2 | Students prompt an AI to write the code in one go, then test and explain it. | about 3 h |
| 3 | Students program all the steps themselves, with the help of an AI. | about 3 h 25 min |

## Prepare before the lesson

Per group of 2 to 4 students: a micro:bit V2 with USB cable, an ELECFREAKS
Cutebot with battery pack, and a laptop with access to
[python.microbit.org](https://python.microbit.org){ target="_blank" } and an AI
chatbot.

**Print:**

- [:material-printer: Robotics: 3-cell grid (A3 print)](Robotics_3cell_grid_A3_print.pdf): the 3-cell grid the robot drives on (A3, cells of 13.3 cm), one per Cutebot.
- From the student version: the environment and robot printables for assignment 1 (one set per pair of students) and the printed code for level 1 (one per student). They are in the appendix of the handout.

## Files for the micro:bit

The code for the Cutebot comes as ready-made files. The `.hex` files are ready to
flash: students drag them onto the micro:bit, no coding needed. The
[explanation for teachers](HEX_files/README.md) describes what each file is and
when students need it.

!!! tip "Download everything at once"
    The worksheet tells students to look for these files in a folder called
    `HEX_files`. The easiest way is to download the whole folder as one ZIP file,
    unzip it, and share the `HEX_files` folder with your students as it is:

    [:material-folder-zip: Robotics: HEX_files folder (ZIP)](Robotics_HEX_files.zip)

You can also download the files one by one:

- [:material-language-python: Cutebot.py](HEX_files/Cutebot.py): the Cutebot driver library. Only needed in levels 2 and 3, as a separate file next to the students' own program.
- [:material-chip: RL_cutebot_3cell.hex](HEX_files/RL_cutebot_3cell.hex) and [:material-language-python: RL_cutebot_3cell.py](HEX_files/RL_cutebot_3cell.py): the learning robot on the 3-cell grid (level 1, and the reference solution for levels 2 and 3).
- [:material-chip: RL_cutebot_4cell.hex](HEX_files/RL_cutebot_4cell.hex) and [:material-language-python: RL_cutebot_4cell.py](HEX_files/RL_cutebot_4cell.py): the advanced 2×2 grid challenge (level 3).

**Calibration** (only if a robot does not drive exactly one cell or turn exactly 90 degrees):

- [:material-chip: 01_forward.hex](HEX_files/Calibration/01_forward.hex) / [.py](HEX_files/Calibration/01_forward.py): drive one cell forward.
- [:material-chip: 02_turn90.hex](HEX_files/Calibration/02_turn90.hex) / [.py](HEX_files/Calibration/02_turn90.py): turn 90 degrees.
- [:material-chip: 03_square.hex](HEX_files/Calibration/03_square.hex) / [.py](HEX_files/Calibration/03_square.py): drive a square.

!!! warning "Ready-made code is a backup"
    In levels 2 and 3, give a group the ready-made files only if they are
    genuinely stuck after working with the AI: struggling productively with the
    AI is part of the lesson.
