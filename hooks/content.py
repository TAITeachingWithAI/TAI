"""MkDocs build hook: replicate the old Jekyll auto-listing behaviour.

Two tokens can be placed anywhere in a page's Markdown:

  <!--pdfs-->      -> a styled list of the PDFs that live directly in the
                      same folder as the page (subfolders excluded).
  <!--sections-->  -> a "grid cards" block linking to the immediate
                      child sections (subfolders that contain an index.md).

This keeps section/index pages to a couple of lines: drop in a token and
newly added PDFs or lesson folders appear automatically on the next build.
"""

import posixpath
import re

import yaml


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


def on_page_markdown(markdown, *, page, config, files, **kwargs):
    if "<!--pdfs-->" not in markdown and "<!--sections-->" not in markdown:
        return markdown
    folder = posixpath.dirname(page.file.src_uri)
    markdown = markdown.replace("<!--sections-->", _sections_block(folder, files))
    markdown = markdown.replace("<!--pdfs-->", _pdf_block(folder, files))
    return markdown
