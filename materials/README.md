# Course materials (working copies)

This is where we **work on** the course materials. The `website/` folder is what
gets published to the site; `materials/` holds the editable masters that produce
it. Edit here, then publish to the website when a lesson is ready.

```
materials/part-2-ai-science/<lesson>/
    <Lesson>.tex + Figures/      the worksheet source (built into the PDFs)
    *.ipynb, *.pptx, *.py, ...   notebooks, slides, code, images (copied as-is)
```

## The two layers

- **`materials/`** — the masters. Edit freely; a lesson can sit here half-finished
  without affecting the live site.
- **`website/`** — the published site. The lesson PDFs and the copied files there
  are **generated** by `publish.py`, so do not edit those by hand (your changes
  would be overwritten on the next publish). The Markdown pages in `website/` are
  the site's pages and *are* edited there directly.

## Student vs teacher version

Each worksheet uses one `.tex` for both versions, via a toggle near the top:

```latex
\newif\ifteacher
\teacherfalse   % student version (no answers)
% \teachertrue  % teacher version (with answers)
```

You don't set this by hand when publishing — `publish.py` builds both versions.

## Publishing to the website

From the repo root, with MiKTeX (or any TeX distribution) installed:

```bash
python publish.py                 # publish every lesson
python publish.py physics         # publish just one lesson (others stay as they are)
python publish.py physics biology # or several
```

This builds each lesson's student and teacher PDF and copies its other materials
into `website/for-teachers/part-2-ai-science/<lesson>/`. Then review `git diff`,
commit, and push — the site deploys automatically.

The exact published PDF names are set per lesson in `publish.yml`. Build
artifacts (`.aux`, `.log`, ...) are ignored by `.gitignore`.

## Not managed here (yet)

Some published files are not built from `materials/` and live only in `website/`:
the exoplanet data PDFs (`exoplanet-files/`), the math print-out plots
(`linear_fit_*.pdf`), and anything in Part 1. These are placed in `website/`
directly for now.
