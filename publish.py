#!/usr/bin/env python3
"""Publish course materials from ``materials/`` to the ``website/``.

Usage::

    python publish.py                   publish everything
    python publish.py physics           publish one lesson
    python publish.py art-styles biology  several lessons
    python publish.py part-1-ai-arts-and-humanities   a whole part
    python publish.py --list            show all parts and lessons

Each lesson in ``publish.yml`` lists its builds. A build compiles ``tex`` with
the student (``\\teacherfalse``) or teacher (``\\teachertrue``) toggle into
``out``, and publishes it to the student or teacher section (``dest``). A part
with ``copy_materials: true`` also copies every non-LaTeX material file into its
for-teachers lesson folder.

Files under ``materials/`` are the masters you edit; files written under
``website/`` are generated, so do not edit those by hand.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
CFG = yaml.safe_load((ROOT / "publish.yml").read_text(encoding="utf-8"))
PARTS = CFG["parts"]

TOGGLE = {"student": r"\teacherfalse", "teacher": r"\teachertrue"}
SECTION = {"student": "for-students", "teacher": "for-teachers"}
SKIP_EXT = {".tex"}
LATEX_ARTIFACTS = {
    ".aux", ".log", ".out", ".toc", ".synctex.gz", ".fls",
    ".fdb_latexmk", ".nav", ".snm", ".vrb", ".bbl", ".blg",
}


def find_pdflatex() -> str:
    exe = shutil.which("pdflatex")
    if exe:
        return exe
    local = os.environ.get("LOCALAPPDATA", "")
    if local:
        for p in Path(local).glob("Programs/MiKTeX/miktex/bin/*/pdflatex.exe"):
            return str(p)
    raise SystemExit("pdflatex not found (install a TeX distribution or add it to PATH)")


PDFLATEX = find_pdflatex()


def build_one(part: str, lesson: str, build: dict, default_dest: str) -> None:
    src = ROOT / "materials" / part / lesson
    tex, out = build["tex"], build["out"]
    toggle = TOGGLE[build["toggle"]]
    dest = build.get("dest", default_dest)
    dest_dir = ROOT / "website" / SECTION[dest] / part / lesson
    dest_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        for item in src.iterdir():
            if item.is_dir():
                shutil.copytree(item, td / item.name)
            else:
                shutil.copy2(item, td / item.name)
        texpath = td / tex
        text = texpath.read_text(encoding="utf-8", errors="ignore")
        text = re.sub(r"\\teacher(?:true|false)", lambda _m: toggle, text)
        texpath.write_text(text, encoding="utf-8")
        for _ in range(2):
            subprocess.run([PDFLATEX, "-interaction=nonstopmode", "-halt-on-error", tex],
                           cwd=td, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        built = td / (Path(tex).stem + ".pdf")
        if not built.exists():
            raise SystemExit(f"  FAILED to build {part}/{lesson}/{tex} ({build['toggle']})")
        shutil.copy2(built, dest_dir / out)
        print(f"  built  {part}/{lesson}: {out}  ->  {SECTION[dest]}")


def copy_materials(part: str, lesson: str) -> None:
    src = ROOT / "materials" / part / lesson
    dest_dir = ROOT / "website" / "for-teachers" / part / lesson
    for dirpath, dirnames, filenames in os.walk(src):
        dp = Path(dirpath)
        if "Figures" in dp.relative_to(src).parts:
            continue
        if "Figures" in dirnames:
            dirnames.remove("Figures")
        for fn in filenames:
            low = fn.lower()
            ext = Path(fn).suffix.lower()
            if (ext in SKIP_EXT or ext in LATEX_ARTIFACTS or ext == ".pdf"
                    or low.endswith(".synctex.gz")):
                continue  # .tex, build artifacts and compiled PDFs are not materials
            rel = (dp / fn).relative_to(src)
            target = dest_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dp / fn, target)
            print(f"  copied {part}/{lesson}: {rel.as_posix()}")


def publish_lesson(part: str, lesson: str) -> None:
    pc = PARTS[part]
    print(f"[{part}/{lesson}]")
    for b in pc["lessons"][lesson]:
        build_one(part, lesson, b, pc.get("default_dest", "teacher"))
    if pc.get("copy_materials"):
        copy_materials(part, lesson)


def main() -> None:
    args = sys.argv[1:]
    if args and args[0] in ("--list", "-l", "-h", "--help"):
        for part, pc in PARTS.items():
            print(f"{part}:")
            for lesson in pc["lessons"]:
                print(f"    {lesson}")
        print("\nUsage: python publish.py [lesson|part ...]   (no arguments = everything)")
        return

    targets: list[tuple[str, str]] = []
    if not args:
        for part, pc in PARTS.items():
            targets += [(part, lesson) for lesson in pc["lessons"]]
    else:
        lesson_to_part = {}
        for part, pc in PARTS.items():
            for lesson in pc["lessons"]:
                lesson_to_part.setdefault(lesson, part)
        for a in args:
            if a in PARTS:
                targets += [(a, lesson) for lesson in PARTS[a]["lessons"]]
            elif a in lesson_to_part:
                targets.append((lesson_to_part[a], a))
            else:
                raise SystemExit(f"unknown part or lesson: {a}  (try --list)")

    for part, lesson in targets:
        publish_lesson(part, lesson)
    print("done.")


if __name__ == "__main__":
    main()
