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


def _read_title(abs_path: str) -> str | None:
    """Best-effort page title: YAML `title:` meta, else first H1."""
    try:
        with open(abs_path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return None
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            try:
                meta = yaml.safe_load(text[3:end]) or {}
            except yaml.YAMLError:
                meta = {}
            if isinstance(meta, dict) and meta.get("title"):
                return str(meta["title"])
            text = text[end + 4:]
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


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
    lines = ['<div class="grid cards" markdown>', ""]
    for parent in sorted(children):
        f = children[parent]
        title = _read_title(f.abs_src_path) or _prettify(posixpath.basename(parent))
        href = posixpath.basename(parent) + "/index.md"
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
