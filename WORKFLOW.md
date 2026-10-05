# Working on the TAI course materials

This repository holds the **Teaching With AI website** and the **editable LaTeX
sources** for the lesson worksheets. From now on we edit the sources **locally**
and push to GitHub (Prism is retired — this repo is the single source of truth).

## How the repo is organised

- **`materials/`** — the sources **you edit**. One folder per lesson, each with
  its `.tex` file(s) and its own `Figures/`:
  - `materials/part-1-ai-arts-and-humanities/<lesson>/`
  - `materials/part-2-ai-science/<lesson>/`
- **`website/`** — the published site: the pages **and** the generated PDFs.
  Do **not** hand-edit the PDFs here — `publish.py` overwrites them.
- **`publish.py` + `publish.yml`** — the tool that builds a lesson's PDFs from
  its source and copies them into `website/`.

One source produces **both** the student and the teacher PDF, via a toggle near
the top of each `.tex`:

```latex
\newif\ifteacher
\teacherfalse   % student version (no answers)
% \teachertrue  % teacher version (with answers)
```

You never flip this by hand — `publish.py` builds both versions for you.

## One-time setup

You need four things.

1. **Git + access to the GitHub organisation `TAITeachingWithAI`.**
   - Install Git: <https://git-scm.com>. (Ask Mirte to add you to the org with
     write access if you don't have it.)
   - Clone the repo and enter it:
     ```bash
     git clone https://github.com/TAITeachingWithAI/TAI.git
     cd TAI
     ```
   - On your first `git push`, Git will ask you to sign in to GitHub — follow the
     prompt (Git Credential Manager remembers it afterwards).

2. **A LaTeX distribution** (this gives you the `pdflatex` command):
   - **Windows:** MiKTeX — <https://miktex.org> (installs missing packages
     automatically the first time you build).
   - **macOS:** MacTeX — <https://tug.org/mactex>.
   - **Linux:** TeX Live — e.g. `sudo apt install texlive-full`.
   - Check it works: `pdflatex --version`.
   - The worksheets use common packages (`booktabs`, `fontawesome5`, `tcolorbox`,
     `tikz`, `cleveref`, `subcaption`, `hyperref`, …). MiKTeX/MacTeX/TeX Live-full
     already have them or fetch them on demand.

3. **Python 3** with one package:
   - Install Python 3 if you don't have it: <https://python.org>
     (check `python --version`, or `python3 --version` on macOS/Linux).
   - Install the single dependency:
     ```bash
     pip install pyyaml
     ```

4. **A LaTeX editor** (your choice): VS Code + the *LaTeX Workshop* extension,
   or TeXstudio, or TeXworks.

> Optional — to preview the whole website locally (not needed just to edit a
> worksheet): `pip install mkdocs-material`, then `python -m mkdocs serve` and
> open the URL it prints.

## Everyday workflow

1. **Get the latest** before you start:
   ```bash
   git pull
   ```
2. **Edit** a lesson's `.tex` under `materials/…`. Each lesson folder is
   self-contained, so you can also compile it directly in your editor to preview.
3. **Publish** it to the website (builds the student + teacher PDFs with the TAI
   logo and copies them into `website/`):
   ```bash
   python publish.py <lesson>
   ```
   - List every lesson name:   `python publish.py --list`
   - A whole part:             `python publish.py part-1-ai-arts-and-humanities`
   - Everything:               `python publish.py`
4. **Commit and push**:
   ```bash
   git add -A
   git commit -m "Update the <lesson> worksheet"
   git push
   ```
   Pushing to `main` redeploys the site automatically; a minute or two later it's
   live at <https://taiteachingwithai.github.io/TAI/>. You don't need to do
   anything else for the deploy.

## Rules of thumb

- Edit in **`materials/`**, never the PDFs in `website/` (they are regenerated).
- `git pull` before you start **and** before you push, so your work and the
  other person's don't clash.
- **New lesson?** Create `materials/<part>/<lesson>/` with the `.tex` + a
  `Figures/` folder, then add a short block to `publish.yml` (copy an existing
  one — it maps the `.tex` to its output PDF name and the student/teacher
  section). Then `python publish.py <lesson>`.
- A few Part 1 cards (prompt guide, style guide, exhibition cards,
  diffusion assignment images) were made in another tool and have **no `.tex`** —
  they live only in `website/` and are not built by `publish.py`.

## If you use an AI assistant (e.g. Claude Code)

Point it at this file and `materials/README.md`. In short:

- Sources are in `materials/<part>/<lesson>/` (`.tex` + `Figures/`, self-contained).
  The site is in `website/`; the generated PDFs there must never be hand-edited.
- Build/publish with `python publish.py <lesson>` — it compiles the student
  (`\teacherfalse`) and teacher (`\teachertrue`) versions as defined in
  `publish.yml`, routes each to the student/teacher section, then you
  `git add` / `commit` / `push`.
- Pushing to `main` triggers the GitHub Actions deploy; the Pages source must stay
  set to **GitHub Actions** (not "deploy from a branch").
