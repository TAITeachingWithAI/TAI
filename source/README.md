# LaTeX sources

The LaTeX sources for the lesson worksheets. These are the files that produce the
PDFs published under `docs/`. They live outside `docs/`, so MkDocs does not
publish them; the repository keeps the source and the built PDF together.

## Layout

```
source/part-2-ai-science/
    mathematics/  Math.tex     + Figures/
    physics/      physics.tex  + Figures/
```

Each lesson folder is self-contained: the `.tex` and every figure it needs are
inside it, so it compiles on its own.

## Student vs teacher version

Both files use one source for both versions, controlled by a toggle near the top:

```latex
\newif\ifteacher
\teacherfalse   % student version (no answers)
% \teachertrue  % teacher version (with answers)
```

Set `\teacherfalse` for the student PDF, `\teachertrue` for the teacher PDF.

## Building

With MiKTeX (already installed on this machine) or any TeX distribution:

```bash
cd source/part-2-ai-science/mathematics
pdflatex Math.tex        # run twice so cross-references resolve
```

Then copy the resulting PDF into the matching folder under
`docs/for-teachers/part-2-ai-science/...`, naming it `*_forstudents.pdf` or
`*_teachertrue.pdf`, and commit both the source change and the new PDF.

Build artifacts (`.aux`, `.log`, `.pdf`, ...) are ignored by `source/.gitignore`.
