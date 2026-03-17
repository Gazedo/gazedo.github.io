#!/usr/bin/env python3
"""
Import Hugo Academic posts from ../gazedo.gitlab.io into this Zola/Serene site.

- Converts YAML front matter → TOML front matter
- Flattens nested post directories: post/<project>/<sub>/index.md
  → content/posts/<project>-<sub>/index.md
- Co-locates images alongside their post
- Updates image references in content body
"""

import re
import shutil
import sys
from pathlib import Path

import yaml

SRC  = Path(__file__).parent.parent.parent / "gazedo.gitlab.io" / "content" / "post"
DEST = Path(__file__).parent.parent / "content" / "posts"

# Hugo date format → Zola (YYYY-MM-DD only)
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2}).*")

def to_toml_string(value: str) -> str:
    escaped = value.replace('\\', '\\\\').replace('"', '\\"')
    return f'"{escaped}"'

def slugify(name: str) -> str:
    """Convert a path component to a kebab-case slug."""
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")

def convert_front_matter(hugo: dict, project_slug: str) -> str:
    """Return a Zola TOML front matter block (without the +++ delimiters)."""
    lines = []

    title = hugo.get("title", "Untitled")
    lines.append(f"title = {to_toml_string(title)}")

    description = hugo.get("summary", "")
    if description:
        lines.append(f"description = {to_toml_string(description)}")

    raw_date = str(hugo.get("date", "1970-01-01"))
    date_match = DATE_RE.match(raw_date)
    date = date_match.group(1) if date_match else "1970-01-01"
    lines.append(f"date = {date}")

    raw_updated = str(hugo.get("lastmod", ""))
    updated_match = DATE_RE.match(raw_updated)
    if updated_match and updated_match.group(1) != date:
        lines.append(f"updated = {updated_match.group(1)}")

    if hugo.get("draft", False):
        lines.append("draft = true")

    # Taxonomies block
    tags = [str(t) for t in hugo.get("tags", [])]
    categories = [str(c) for c in hugo.get("categories", [])]
    # Add the project name as a category so posts are groupable
    if project_slug not in categories:
        categories.insert(0, project_slug)

    lines.append("")
    lines.append("[taxonomies]")
    tag_list = ", ".join(to_toml_string(t) for t in tags)
    lines.append(f"tags = [{tag_list}]")
    cat_list = ", ".join(to_toml_string(c) for c in categories)
    lines.append(f"categories = [{cat_list}]")

    # Extra block
    lines.append("")
    lines.append("[extra]")
    lines.append('lang = "en"')
    lines.append("toc = true")
    lines.append("copy = true")
    lines.append("comment = false")
    if hugo.get("featured", False):
        lines.append("featured = true")

    return "\n".join(lines)


def strip_hugo_front_matter(text: str):
    """
    Strip YAML front matter (--- ... ---) and return (parsed_dict, body).
    Handles both --- and +++ delimiters defensively.
    """
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                parsed = yaml.safe_load(parts[1]) or {}
            except yaml.YAMLError as e:
                print(f"  WARN: YAML parse error: {e}", file=sys.stderr)
                parsed = {}
            return parsed, parts[2].lstrip("\n")
    return {}, text


def update_image_refs(body: str, images: list[str]) -> str:
    """
    Convert Hugo shortcodes to Zola equivalents:
      {{< figure src="x" alt="y" ... >}}  →  {{ figure(src="x", alt="y") }}
      {{< video  src="x" ... >}}           →  <video controls src="x"></video>
    """
    # --- figure shortcode ---
    def replace_figure(m: re.Match) -> str:
        attrs_raw = m.group(1)
        src   = re.search(r'src=["\']([^"\']+)["\']',   attrs_raw)
        alt   = re.search(r'alt=["\']([^"\']+)["\']',   attrs_raw)
        caption = re.search(r'caption=["\']([^"\']+)["\']', attrs_raw)
        parts = []
        if src:
            parts.append(f'src="{src.group(1)}"')
        if alt:
            parts.append(f'alt="{alt.group(1)}"')
        if caption:
            parts.append(f'caption="{caption.group(1)}"')
        return "{{{{ figure({}) }}}}".format(", ".join(parts))

    body = re.sub(r'\{\{<\s*figure\s+(.*?)\s*>\}\}', replace_figure, body, flags=re.DOTALL)

    # --- video shortcode → plain HTML5 video ---
    def replace_video(m: re.Match) -> str:
        attrs_raw = m.group(1)
        src = re.search(r'src=["\']([^"\']+)["\']', attrs_raw)
        src_val = src.group(1) if src else ""
        return f'<video controls src="{src_val}"></video>'

    body = re.sub(r'\{\{<\s*video\s+(.*?)\s*>\}\}', replace_video, body, flags=re.DOTALL)

    return body


def import_post(src_index: Path, dest_dir: Path, project_slug: str, post_slug: str):
    dest_dir.mkdir(parents=True, exist_ok=True)

    raw = src_index.read_text(encoding="utf-8")
    hugo_fm, body = strip_hugo_front_matter(raw)

    toml_fm = convert_front_matter(hugo_fm, project_slug)

    # Collect sibling assets (images, etc.) — skip .drawio and other non-web files
    web_exts = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".mp4", ".mov"}
    assets = [
        f for f in src_index.parent.iterdir()
        if f.is_file() and f.suffix.lower() in web_exts
    ]

    body = update_image_refs(body, [a.name for a in assets])

    dest_index = dest_dir / "index.md"
    dest_index.write_text(f"+++\n{toml_fm}\n+++\n{body}", encoding="utf-8")
    print(f"  wrote {dest_index.relative_to(dest_dir.parent.parent)}")

    for asset in assets:
        dest_asset = dest_dir / asset.name
        shutil.copy2(asset, dest_asset)
        print(f"    copied {asset.name}")


def main():
    if not SRC.exists():
        print(f"ERROR: source not found: {SRC}", file=sys.stderr)
        sys.exit(1)

    DEST.mkdir(parents=True, exist_ok=True)

    # Walk: post/<project>/[<sub>/]index.md
    for project_dir in sorted(SRC.iterdir()):
        if not project_dir.is_dir() or project_dir.name.startswith("_"):
            continue

        project_slug = slugify(project_dir.name)
        print(f"\n[{project_dir.name}]")

        # Check if posts are nested (sub-series) or flat (single index.md)
        direct_index = project_dir / "index.md"

        if direct_index.exists():
            # Flat post — e.g. brushed_motor_encoder/index.md
            dest_dir = DEST / project_slug
            import_post(direct_index, dest_dir, project_slug, project_slug)
        else:
            # Series post — e.g. autolevel/brainstorm/index.md
            for sub_dir in sorted(project_dir.iterdir()):
                if not sub_dir.is_dir() or sub_dir.name.startswith("_"):
                    continue
                sub_index = sub_dir / "index.md"
                if not sub_index.exists():
                    continue
                sub_slug = slugify(sub_dir.name)
                combined_slug = f"{project_slug}-{sub_slug}"
                dest_dir = DEST / combined_slug
                import_post(sub_index, dest_dir, project_slug, combined_slug)

    print("\nDone.")


if __name__ == "__main__":
    main()
