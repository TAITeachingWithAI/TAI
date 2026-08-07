---
title: Robotics
order: 5
---

# Robotics

Teaching material for the robotics lesson of Part 2: AI & Science — **"A
rover learning on an exoplanet"**. Students program a micro:bit rover with an
AI co-pilot: first calibrating basic movement, then building a Q-learning
grid simulation, and finally deploying it on a Cutebot.

## Lesson material

- [:material-file-pdf-box: Rover lesson: student version](RL_Rover_Handout_student.pdf)
- [:material-file-pdf-box: Rover lesson: teacher version](RL_Rover_Handout_teacher.pdf)

!!! info "Which version do I need?"
    The **student version** is the worksheet you hand out. The **teacher version**
    is the same lesson including the worked answers, for your own preparation.

!!! warning "Backup and solution files are a last resort"
    Give a group the backup/solution files below only if they are genuinely
    stuck after trying with the AI co-pilot first — struggling productively
    with the AI is the point of the lesson.

## Assignment 1 — Calibration

Backup solutions for the three calibration tasks (drive forward, turn 90°,
walk a square). Copy-paste only as a last resort.

- [:material-language-python: 01_forward.py](assignment-1-calibration/01_forward.py)
- [:material-language-python: 02_turn90.py](assignment-1-calibration/02_turn90.py)
- [:material-language-python: 03_square.py](assignment-1-calibration/03_square.py)

## Assignment 2 — RL grid

!!! note "What students receive"
    **`Code_RL_grid_TO_ANNOTATE.docx`** is the file to print and hand to
    students: the RL grid code with blank space for them to annotate each
    block. Everything else in this section is a backup or teacher resource.

- [:material-file-word-box: **Code_RL_grid_TO_ANNOTATE.docx** — print and hand to students](assignment-2-rl-grid/Code_RL_grid_TO_ANNOTATE.docx)
- [:material-file-word-box: Code_RL_grid_SOLUTION.docx](assignment-2-rl-grid/Code_RL_grid_SOLUTION.docx) — the same code, with the explanation filled in (for you).
- [:material-chip: RL_leds_3x3.hex](assignment-2-rl-grid/RL_leds_3x3.hex) — ready-to-flash version, in case a group's python.microbit.org save fails.
- [:material-language-python: RL_grid_BACKUP_SOLUTION.py](assignment-2-rl-grid/RL_grid_BACKUP_SOLUTION.py) — the plain source, as a copy-paste backup.

### Q-values notebook

A notebook with pictures and a simulation of how Q values evolve throughout
learning — useful to walk through with the whole class.

Click **Open in Colab** to run it in your browser without installing
anything, or download the `.ipynb` file to run it locally.

| Run it | Download |
| --- | --- |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/TAITeachingWithAI/TAI/blob/main/docs/for-teachers/part-2-ai-science/robotics/assignment-2-rl-grid/RL_Rover_Qvalues_Simulation.ipynb) | [:material-notebook: .ipynb](assignment-2-rl-grid/RL_Rover_Qvalues_Simulation.ipynb) |

## Assignment 3 — Cutebot

- [:material-language-python: Cutebot.py](assignment-3-cutebot/Cutebot.py) — required library; add this to the micro:bit project **before** the RL code.
- [:material-chip: RL_cutebot.hex](assignment-3-cutebot/RL_cutebot.hex) — ready-to-flash version of the full RL + Cutebot code, in case a group's save fails.
- [:material-language-python: RL_cutebot_BACKUP_SOLUTION.py](assignment-3-cutebot/RL_cutebot_BACKUP_SOLUTION.py) — the plain source, as a copy-paste backup.
