#!/usr/bin/env python3
"""
migrate-raw.py — 迁移 raw/ 目录并同步更新 wiki 中的路径引用。

用法示例:
    python scripts/migrate-raw.py --dry-run \
        "会议记录" "02-市场情报/行业动态/会议记录"

    python scripts/migrate-raw.py \
        "竞品资料" "05-竞品分析/对比分析/竞品资料"
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "raw"
WIKI_DIR = REPO_ROOT / "wiki"
CLAUDE_MD = REPO_ROOT / "CLAUDE.md"


def run_git_mv(src: Path, dst: Path, dry_run: bool) -> bool:
    """使用 git mv 移动目录/文件。"""
    if not src.exists():
        print(f"[ERROR] 源路径不存在: {src}")
        return False

    if dry_run:
        print(f"[DRY-RUN] git mv {src.relative_to(REPO_ROOT)} {dst.relative_to(REPO_ROOT)}")
        return True

    try:
        subprocess.run(
            ["git", "mv", str(src), str(dst)],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"[MOVED] {src.relative_to(REPO_ROOT)} -> {dst.relative_to(REPO_ROOT)}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] git mv 失败: {e.stderr}")
        return False


def find_md_files() -> list[Path]:
    """查找需要扫描的 markdown 文件。"""
    files = list(WIKI_DIR.rglob("*.md"))
    if CLAUDE_MD.exists():
        files.append(CLAUDE_MD)
    return files


def replace_in_content(
    content: str,
    old_rel: str,
    new_rel: str,
) -> tuple[str, int]:
    """
    替换 content 中的路径引用。

    替换规则（按优先级）：
    1. Markdown 链接/图片中的 ../../raw/old -> ../../raw/new
    2. 正文文本中的 raw/old -> raw/new
    3. YAML frontmatter sources 列表中的条目（行首缩进后接旧路径）
    """
    changed = 0

    # 规则 1: ../../raw/old_path -> ../../raw/new_path
    # 匹配 ../../raw/旧路径/文件名 或 ../../raw/旧路径/
    old_link = f"../../raw/{old_rel}"
    new_link = f"../../raw/{new_rel}"
    if old_link in content:
        count = content.count(old_link)
        content = content.replace(old_link, new_link)
        changed += count

    # 规则 2: raw/old_path -> raw/new_path
    # 用于正文中 `raw/会议记录/...` 这样的描述
    old_desc = f"raw/{old_rel}"
    new_desc = f"raw/{new_rel}"
    if old_desc in content:
        count = content.count(old_desc)
        content = content.replace(old_desc, new_desc)
        changed += count

    # 规则 3: YAML frontmatter sources 中的条目
    # 匹配形如：- "old_rel/..." 或 - old_rel/...
    # 使用正则，只匹配 sources 块内的行
    pattern = re.compile(
        rf"^(\s*-\s*['\"]?){re.escape(old_rel)}",
        re.MULTILINE,
    )

    def _repl_sources(m: re.Match) -> str:
        return f"{m.group(1)}{new_rel}"

    content, count = pattern.subn(_repl_sources, content)
    changed += count

    return content, changed


def process_wiki_files(old_rel: str, new_rel: str, dry_run: bool) -> dict[str, int]:
    """扫描并更新所有 wiki markdown 文件。"""
    stats = {"files_scanned": 0, "files_changed": 0, "replacements": 0}

    for md_file in find_md_files():
        stats["files_scanned"] += 1
        original = md_file.read_text(encoding="utf-8")
        updated, changed = replace_in_content(original, old_rel, new_rel)

        if changed:
            stats["files_changed"] += 1
            stats["replacements"] += changed
            if dry_run:
                print(f"[DRY-RUN] 将修改 {md_file.relative_to(REPO_ROOT)} ({changed} 处)")
            else:
                md_file.write_text(updated, encoding="utf-8")
                print(f"[UPDATED] {md_file.relative_to(REPO_ROOT)} ({changed} 处)")

    return stats


def main() -> int:
    parser = argparse.ArgumentParser(
        description="迁移 raw/ 子目录并同步更新 wiki 中的路径引用。"
    )
    parser.add_argument("old_path", help="raw/ 下的旧相对路径")
    parser.add_argument("new_path", help="raw/ 下的新相对路径")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只打印将要执行的操作，不真正修改文件",
    )
    args = parser.parse_args()

    old_rel = args.old_path.strip("/")
    new_rel = args.new_path.strip("/")

    src = RAW_DIR / old_rel
    dst_parent = RAW_DIR / new_rel

    if not src.exists():
        print(f"[ERROR] 源路径不存在: {src}")
        return 1

    # 目标路径的最后一个分量是移动后的名称
    dst = dst_parent
    # 但如果 new_rel 以旧路径的 basename 结尾，且父目录已存在，则直接作为最终路径
    # 实际上 shutil.move 的行为就是：dst_parent 是最终路径（含名称）
    # 为了让用户能写 "02-市场情报/行业动态/会议记录" 这种包含最终目录名的路径：
    if dst.exists() and dst.is_dir():
        # 如果目标已存在且是目录，则源会移入该目录下（git mv 行为）
        # 此时最终路径会变成 dst / src.name，通常不是用户想要的
        # 这里给出警告
        print(f"[WARN] 目标目录已存在: {dst}")
        print(f"[WARN] git mv 将把源移入该目录下，最终路径为: {dst / src.name}")

    print("=" * 60)
    print(f"迁移: raw/{old_rel} -> raw/{new_rel}")
    if args.dry_run:
        print("模式: DRY-RUN (不会真正修改)")
    print("=" * 60)

    # 1. 移动目录
    ok = run_git_mv(src, dst, args.dry_run)
    if not ok:
        return 1

    # 2. 更新 wiki 文件
    stats = process_wiki_files(old_rel, new_rel, args.dry_run)

    print("=" * 60)
    print(f"扫描文件: {stats['files_scanned']}")
    print(f"修改文件: {stats['files_changed']}")
    print(f"总替换数: {stats['replacements']}")
    print("=" * 60)

    if args.dry_run:
        print("DRY-RUN 完成。如需执行，请去掉 --dry-run 重新运行。")
    else:
        print("迁移完成。建议执行 `git status` 和 `git diff --stat` 检查变更。")

    return 0


if __name__ == "__main__":
    sys.exit(main())
