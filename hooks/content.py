"""MkDocs build hook: replicate the old Jekyll auto-listing behaviour.

Two tokens can be placed anywhere in a page's Markdown:

  <!--pdfs-->      -> a styled list of the PDFs that live directly in the
                      same folder as the page (subfolders excluded).
  <!--sections-->  -> a "grid cards" block linking to the immediate
                      child sections (subfolders that contain an index.md).
  <!--student-pdfs--> -> on a teacher lesson page: direct links to the PDFs of
                      the matching student page. Teacher lesson pages always
                      get this ("## Student material") even without the token,
                      so teachers find all material in one place.

This keeps section/index pages to a couple of lines: drop in a token and
newly added PDFs or lesson folders appear automatically on the next build.

Lesson pages (for-students/<part>/<lesson>/index.md and the same under
for-teachers) also get a "lesson at a glance" block with the duration, subject,
lesson outline and learning goals. The data comes from data/lesson_summaries.yml,
which TAI_materials/publish.py generates from the lessons' .tex sources. The
block is inserted before the first "## " heading, or where the page puts
<!--summary-->.
"""

import os
import posixpath
import re

import yaml

_SUMMARIES = None


def _summaries(config) -> dict:
    global _SUMMARIES
    if _SUMMARIES is None:
        path = os.path.join(os.path.dirname(config["config_file_path"]), "data", "lesson_summaries.yml")
        try:
            with open(path, encoding="utf-8") as fh:
                _SUMMARIES = yaml.safe_load(fh) or {}
        except OSError:
            _SUMMARIES = {}
    return _SUMMARIES


def _md_list(items, indent: str, numbered: bool) -> list[str]:
    lines = []
    for n, item in enumerate(items, 1):
        text, subs = (item.get("text", ""), item.get("sub", [])) if isinstance(item, dict) else (item, [])
        lines.append(f"{indent}{f'{n}.' if numbered else '-'} {text}")
        for sub in subs:
            lines.append(f"{indent}    - {sub}")
    return lines


def _summary_block(s: dict, teacher: bool) -> str:
    facts = []
    if s.get("duration"):
        facts.append(f":material-clock-outline: **Duration:** {s['duration']}")
    if s.get("subject"):
        facts.append(f":material-school-outline: **Subject:** {s['subject']}")
    title = "Lesson at a glance" if teacher else "This lesson at a glance"
    lines = [f'!!! abstract "{title}"', ""]
    if facts:
        lines.append("    " + "  \n    ".join(facts))
        lines.append("")

    def outline_part(open_: bool):
        out = [f'    ???{"+" if open_ else ""} note "Lesson outline"', ""]
        o = s.get("outline")
        if isinstance(o, list):
            out += _md_list(o, "        ", numbered=True)
        elif o:
            out.append(f"        {o}")
        if s.get("outline_note"):
            out += ["", f"        {s['outline_note']}"]
        return out + [""]

    goals = [f'    ???+ success "{"Learning goals" if teacher else "What you will learn"}"', ""]
    goals += _md_list(s.get("goals") or [], "        ", numbered=False) + [""]

    if teacher:
        lines += outline_part(True) + goals
        setup = s.get("setup")
        if setup:
            lines += ['    ??? info "What you need"', ""]
            lines += (_md_list(setup, "        ", numbered=False) if isinstance(setup, list)
                      else [f"        {setup}"]) + [""]
    else:
        lines += goals + outline_part(False)
    return "\n".join(lines).rstrip() + "\n"


def _insert_summary(markdown: str, page, config) -> str:
    parts = page.file.src_uri.split("/")
    if len(parts) != 4 or parts[0] not in ("for-students", "for-teachers") or parts[3] != "index.md":
        return markdown
    s = _summaries(config).get(f"{parts[1]}/{parts[2]}")
    if not s:
        return markdown.replace("<!--summary-->", "")
    block = _summary_block(s, teacher=parts[0] == "for-teachers")
    if "<!--summary-->" in markdown:
        return markdown.replace("<!--summary-->", block)
    # Default position: right after the H1 and its intro paragraph(s), before the
    # first heading, list, table, admonition, token or HTML block.
    h1 = re.search(r"^# .*$", markdown, re.M)
    pos = h1.end() if h1 else 0
    while True:
        m = re.match(r"\n*([^\n].*?)(?=\n\s*\n|\Z)", markdown[pos:], re.S)
        if not m:
            break
        first = m.group(1).lstrip()
        if re.match(r"(#|[-*+] |\d+\. |\||<|!!!|\?\?\?|\[!\[|\[:)", first):
            break
        pos += m.end()
    return markdown[:pos].rstrip() + "\n\n" + block + "\n" + markdown[pos:].lstrip("\n")


def _prettify(filename: str) -> str:
    """`Art_styles_image_generation.pdf` -> `Art styles image generation`."""
    stem = filename.rsplit(".", 1)[0]
    stem = stem.replace("_", " ").replace("-", " ")
    stem = re.sub(r"\s+", " ", stem).strip()
    return stem[:1].upper() + stem[1:] if stem else filename


def _read_page_meta(abs_path: str) -> tuple[str | None, float]:
    """Best-effort ``(title, order)`` for a page.

    The title comes from the YAML ``title:`` meta, else the first H1. The order
    comes from an optional ``order:`` meta; pages without one keep their
    previous alphabetical placement.
    """
    try:
        with open(abs_path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return None, float("inf")
    title = None
    order = float("inf")
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            try:
                meta = yaml.safe_load(text[3:end]) or {}
            except yaml.YAMLError:
                meta = {}
            if isinstance(meta, dict):
                if meta.get("title"):
                    title = str(meta["title"])
                try:
                    order = float(meta["order"])
                except (KeyError, TypeError, ValueError):
                    pass
            text = text[end + 4:]
    if title is None:
        match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        title = match.group(1).strip() if match else None
    return title, order


def _pdf_block(folder: str, files) -> str:
    items = []
    for f in files:
        uri = f.src_uri
        if uri.lower().endswith(".pdf") and posixpath.dirname(uri) == folder:
            name = posixpath.basename(uri)
            items.append((name, _prettify(name)))
    if not items:
        return "_No documents in this section yet._"
    items.sort(key=lambda pair: pair[1].lower())
    return "\n".join(
        f"- [:material-file-pdf-box: {label}]({name})" for name, label in items
    )


def _student_folder(folder: str) -> str | None:
    """for-teachers/<part>/<lesson> -> for-students/<part>/<lesson> (lesson pages only)."""
    parts = folder.split("/")
    if len(parts) == 3 and parts[0] == "for-teachers":
        return "/".join(["for-students"] + parts[1:])
    return None


def _student_pdfs(folder: str, files) -> list[tuple[str, str]]:
    """(relative link, label) for the PDFs in the matching student folder."""
    sfolder = _student_folder(folder)
    if not sfolder:
        return []
    items = []
    for f in files:
        uri = f.src_uri
        if uri.lower().endswith(".pdf") and posixpath.dirname(uri) == sfolder:
            name = posixpath.basename(uri)
            items.append((posixpath.relpath(uri, folder).replace(" ", "%20"), _prettify(name)))
    return sorted(items, key=lambda pair: pair[1].lower())


def _student_pdf_block(folder: str, files) -> str:
    items = _student_pdfs(folder, files)
    if not items:
        return "_No student documents for this lesson._"
    return "\n".join(f"- [:material-file-pdf-box: {label}]({link})" for link, label in items)


def _ensure_student_material(markdown: str, page, files) -> str:
    """Teacher lesson pages always show the student material too (as direct links)."""
    if "<!--student-pdfs-->" in markdown:
        return markdown
    folder = posixpath.dirname(page.file.src_uri)
    if not _student_pdfs(folder, files):
        return markdown
    section = "## Student material\n\n<!--student-pdfs-->\n"
    m = re.search(r"^## ", markdown, re.M)
    if m:
        return markdown[:m.start()] + section + "\n" + markdown[m.start():]
    return markdown.rstrip() + "\n\n" + section


def _sections_block(folder: str, files) -> str:
    children = {}
    for f in files:
        uri = f.src_uri
        if not uri.endswith("index.md"):
            continue
        parent = posixpath.dirname(uri)
        if parent and parent != folder and posixpath.dirname(parent) == folder:
            children[parent] = f
    if not children:
        return ""
    entries = []
    for parent, f in children.items():
        name = posixpath.basename(parent)
        title, order = _read_page_meta(f.abs_src_path)
        entries.append((order, name.lower(), title or _prettify(name), name + "/index.md"))
    entries.sort()
    lines = ['<div class="grid cards" markdown>', ""]
    for _, _, title, href in entries:
        lines.append(f"-   :material-folder-open:{{ .lg .middle }} **[{title}]({href})**")
        lines.append("")
    lines.append("</div>")
    return "\n".join(lines)


def _fill_durations(markdown: str, config) -> str:
    """<!--duration:<part>/<lesson>--> -> the lesson's short duration (from the summaries)."""
    data = _summaries(config)
    return re.sub(r"<!--duration:([^>]+?)-->",
                  lambda m: (data.get(m.group(1).strip()) or {}).get("duration") or "", markdown)


def on_page_markdown(markdown, *, page, config, files, **kwargs):
    markdown = _fill_durations(markdown, config)
    markdown = _ensure_student_material(markdown, page, files)
    markdown = _insert_summary(markdown, page, config)
    folder = posixpath.dirname(page.file.src_uri)
    if "<!--student-pdfs-->" in markdown:
        markdown = markdown.replace("<!--student-pdfs-->", _student_pdf_block(folder, files))
    if "<!--pdfs-->" not in markdown and "<!--sections-->" not in markdown:
        return markdown
    markdown = markdown.replace("<!--sections-->", _sections_block(folder, files))
    markdown = markdown.replace("<!--pdfs-->", _pdf_block(folder, files))
    return markdown
