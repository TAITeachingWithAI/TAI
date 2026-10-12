# Working on the TAI site

The project is split across **two repositories**:

- **`TAITeachingWithAI/TAI`** (this one, **public**) — the website: the pages,
  `mkdocs.yml`, `hooks/`, the GitHub Actions deploy, and the **generated** PDFs /
  notebooks under `website/`. This is what deploys to
  <https://taiteachingwithai.github.io/TAI/>.
- **`TAITeachingWithAI/TAI_materials`** (**private**) — the editable LaTeX
  **sources** (`.tex` + `Figures/`) and the `publish.py` / `publish.yml` tool.

You **edit worksheet sources in the private repo**; `publish.py` there builds the
PDFs and writes them into this repo's `website/`. So:

- Don't hand-edit the PDFs in `website/` — they are regenerated and would be
  overwritten.
- The Markdown **pages** in `website/` *are* edited here directly.
- The small Part 1 cards made in another tool (prompt guide, style guide,
  exhibition cards, diffusion assignment images) have no `.tex` and live only
  here.

## Setup

Clone **both** repos **side by side** (so `publish.py` in the materials repo can
find this one):

```
Projects\TAI             <- git clone https://github.com/TAITeachingWithAI/TAI.git
Projects\TAI_materials   <- git clone https://github.com/TAITeachingWithAI/TAI_materials.git
```

You also need Git (with access to the org — including the **private** repo), a
LaTeX distribution (MiKTeX / MacTeX / TeX Live) for `pdflatex`, Python 3 with
`pip install pyyaml`, and a LaTeX editor. Full details are in the
**`README.md` of the `TAI_materials` repo**.

> To preview this site locally: `pip install mkdocs-material`, then
> `python -m mkdocs serve` in this repo and open the URL it prints.

## Everyday workflow

1. `git pull` in **both** repos.
2. Edit a `.tex` in **`TAI_materials`** under `materials/<part>/<lesson>/`.
3. From the `TAI_materials` repo, build + copy the PDFs into this repo:
   ```bash
   python publish.py <lesson>      # also: --list, a <part>, or nothing = all
   ```
4. Commit and push **both** repos:
   - in `TAI_materials` — the source change;
   - in `TAI` (this repo) — the rebuilt PDFs.
   Pushing **this** repo to `main` redeploys the live site automatically (a minute
   or two later).

## Notes

- Editing only a **page** (Markdown) here? Just edit, commit and push this repo —
  no `publish.py` needed.
- The GitHub **Pages source must stay set to "GitHub Actions"** (Settings → Pages),
  not "Deploy from a branch", or a stray Jekyll build will overwrite the site.

## If you use an AI assistant (e.g. Claude Code)

- Two repos, cloned side by side: this **public `TAI`** = the site (`website/`,
  `mkdocs.yml`, deploy); **private `TAI_materials`** = the `.tex` sources +
  `publish.py`.
- To change a worksheet: edit its `.tex` in `TAI_materials`, run
  `python publish.py <lesson>` (it builds student=`\teacherfalse` /
  teacher=`\teachertrue` per `publish.yml` and writes the PDFs into this repo),
  then commit & push **both** repos.
- Never hand-edit generated PDFs under `website/`. Pushing `TAI`'s `main`
  triggers the Pages deploy.
