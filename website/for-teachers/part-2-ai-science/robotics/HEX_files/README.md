# What's in this folder (for teachers, no coding knowledge needed)

## The files

- `Cutebot.py` — a small piece of code that tells the micro:bit how to talk to the Cutebot robot (move the wheels, read the sensors, etc.). Think of it as a "driver" or "instruction manual" for the hardware.
- `RL_cutebot_3cell.py` / `RL_cutebot_4cell.py` — the actual reinforcement-learning programs for the 3-cell and 2x2-cell (4-cell) grids.
- `RL_cutebot_3cell.hex` / `RL_cutebot_4cell.hex` — ready-to-flash versions of the two programs above. These are what students in **Level 1** drag-and-drop onto the micro:bit — no coding needed, no extra files to add.

## Why does `RL_cutebot_3cell.py` (and the 4-cell one) start with all the Cutebot code?

If you open `RL_cutebot_3cell.py` or `RL_cutebot_4cell.py`, you'll notice the first part of the file (roughly the first 70 lines) is an exact copy of what's inside `Cutebot.py`, and only after that does the actual learning code begin (the part explained step by step in the handout).

This is **not a mistake** — it's a technical workaround:

- The tool we use to turn a Python program into a `.hex` file (the format you drag onto the micro:bit) can only pack **one single file** at a time.
- Normally, when coding on `python.microbit.org`, you could have two separate files — `main.py` (your program) and `Cutebot.py` (the driver) — and the program simply "imports" the driver when it starts.
- But since our tool can only turn one file into a `.hex`, we glued the two together ahead of time: we pasted the contents of `Cutebot.py` directly at the top of the learning program, so the resulting `.hex` file works all by itself, with nothing missing.

**In short:** the `.hex` files already contain everything they need inside them. A student who flashes `RL_cutebot_3cell.hex` or `RL_cutebot_4cell.hex` onto the micro:bit does **not** need to separately add `Cutebot.py` anywhere — it's already built in.

## So when is `Cutebot.py` actually needed as a separate file?

Only in **Levels 2 and 3**, where students (with the help of an AI) write their own program from scratch on `python.microbit.org`, instead of just flashing a ready-made `.hex`.

In that case, their own code needs to say "use the Cutebot driver" (this line appears in the AI prompt they use: *"using MicroPython and the Cutebot library (Cutebot.py)"*). For that line to work, `Cutebot.py` must be uploaded as its **own separate file** next to their program on the micro:bit's file system (in `python.microbit.org`, this just means having two files open/saved: their own script and `Cutebot.py`).

That's why `Cutebot.py` is kept here as a standalone file too — it's not used for Level 1 (it's already baked into the `.hex` files), but it's needed for Levels 2 and 3, where students build and flash their own code.
