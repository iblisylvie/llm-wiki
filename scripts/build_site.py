#!/usr/bin/env python3
"""
Build a static knowledge base site with three-column layout.
"""

from pathlib import Path

from build_site.tree import build_wiki_tree, build_raw_trees, flatten_tree, build_nav_html
from build_site.renderer import render_site_html

ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = ROOT / "wiki"
RAW_DIR = ROOT / "raw"
SITE_DIR = ROOT / "site"


def main():
    SITE_DIR.mkdir(exist_ok=True)

    wiki_tree = build_wiki_tree(str(WIKI_DIR))
    raw_trees = build_raw_trees(str(RAW_DIR))

    pages = {}
    flatten_tree(wiki_tree["children"], pages, "wiki", str(WIKI_DIR), str(RAW_DIR))
    for raw_tree in raw_trees:
        flatten_tree(raw_tree["children"], pages, "", str(WIKI_DIR), str(RAW_DIR))

    # Build left nav: wiki first, then raw folders as collapsible top-level folders
    nav_items = []
    if wiki_tree["children"]:
        wiki_tree["path"] = "wiki"
        nav_items.append(build_nav_html([wiki_tree], 0, ""))
    for raw_tree in raw_trees:
        if raw_tree["children"]:
            # Render raw folder as a collapsible top-level node without extra prefix
            nav_items.append(build_nav_html([raw_tree], 0, ""))

    nav_html = "".join(nav_items)
    output_path = str(SITE_DIR / "index.html")
    render_site_html(nav_html, pages, output_path)

    print(f"Site generated at {output_path}")
    print(f"Total pages: {len(pages)}")


if __name__ == "__main__":
    main()
