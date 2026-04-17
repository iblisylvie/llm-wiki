"""Build navigation trees from wiki and raw directories."""

from pathlib import Path

from build_site.parser import read_wiki_page, read_raw_file


def _insert_node(parent: dict, name: str, node_type: str):
    for child in parent["children"]:
        if child["name"] == name and child["type"] == node_type:
            return child
    node = {"name": name, "type": node_type, "children": []}
    parent["children"].append(node)
    return node


def build_wiki_tree(wiki_dir: str) -> dict:
    tree = {"name": "Wiki", "type": "folder", "children": []}
    files = sorted(Path(wiki_dir).rglob("*.md"))
    for f in files:
        rel = f.relative_to(wiki_dir)
        parts = rel.parts
        node = tree
        for part in parts[:-1]:
            node = _insert_node(node, part, "folder")
        node["children"].append({
            "name": parts[-1],
            "type": "file",
            "path": str(rel),
            "source": str(f),
        })
    return tree


def build_raw_trees(raw_dir: str) -> list:
    trees = []
    dirs = sorted([d for d in Path(raw_dir).iterdir() if d.is_dir()])
    for d in dirs:
        tree = {"name": d.name, "type": "folder", "children": []}
        files = sorted(d.rglob("*"))
        for f in files:
            if f.is_dir():
                continue
            if f.name == ".gitkeep":
                continue
            rel = f.relative_to(raw_dir)
            parts = rel.parts
            node = tree
            # Skip the first part (directory name) to avoid duplicating the top-level folder
            for part in parts[1:-1]:
                node = _insert_node(node, part, "folder")
            node["children"].append({
                "name": parts[-1],
                "type": "file",
                "path": str(rel),
                "source": str(f),
            })
        trees.append(tree)
    return trees


def flatten_tree(nodes: list, pages: dict, prefix: str, wiki_dir: str, raw_dir: str):
    for node in nodes:
        if node["type"] == "file":
            key = prefix + "/" + node["path"] if prefix else node["path"]
            if prefix == "wiki":
                pages[key] = read_wiki_page(node["source"], node["path"])
            else:
                pages[key] = read_raw_file(node["source"], node["path"])
        elif node["type"] == "folder":
            flatten_tree(node["children"], pages, prefix, wiki_dir, raw_dir)


def build_nav_html(nodes: list, level: int = 0, parent_path: str = "") -> str:
    items = []
    for node in nodes:
        if node["type"] == "folder":
            child_parent_path = node.get("path", parent_path)
            children_html = build_nav_html(node["children"], level + 1, child_parent_path)
            items.append(f"""
                <div class="nav-folder">
                    <div class="nav-folder-title" data-toggle="collapse" style="padding-left:{16 + level * 12}px">
                        {node['name']}
                    </div>
                    <div class="nav-folder-children">
                        {children_html}
                    </div>
                </div>
            """)
        else:
            key = parent_path + "/" + node["path"] if parent_path else node["path"]
            display = node["name"]
            items.append(f"""
                <a class="nav-link" href="#/{key}" data-key="{key}" style="padding-left:{16 + level * 12}px">
                    {display}
                </a>
            """)
    return "".join(items)
