"""从技能目录加载 SKILL.md。

较新的 google-adk 提供 `google.adk.skills.load_skill_from_dir` 时由 agent 优先使用；
当前环境若未导出该函数，则用本模块实现（行为与官方加载 SKILL/references/scripts 一致）。"""
from __future__ import annotations

import pathlib
from typing import Any

import yaml
from google.adk.skills.models import Frontmatter, Resources, Script, Skill


def _is_text_file(path: pathlib.Path) -> bool:
    """通过扩展名和试读判断是否为文本文件。"""
    text_exts = {".md", ".txt", ".html", ".htm", ".json", ".yaml", ".yml", ".css", ".js"}
    if path.suffix.lower() in text_exts:
        return True
    try:
        path.read_text(encoding="utf-8")
        return True
    except (UnicodeDecodeError, IOError):
        return False


def load_skill_from_dir(skill_dir: pathlib.Path, base_dir: pathlib.Path | None = None) -> Skill:
    """读取 SKILL.md 的 YAML frontmatter 与正文，并加载 references / assets / scripts。

    Args:
        skill_dir: 技能子目录路径。
        base_dir: 解析 external_references 相对路径时的基准目录；
                  默认以 skill_dir 为基准。
    """
    skill_dir = skill_dir.resolve()
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        raise FileNotFoundError(f"缺少 SKILL.md: {skill_md}")

    text = skill_md.read_text(encoding="utf-8")
    if not text.lstrip().startswith("---"):
        raise ValueError(f"SKILL.md 必须以 YAML frontmatter 开头: {skill_md}")

    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"无效的 frontmatter 结构: {skill_md}")

    fm_raw: Any = yaml.safe_load(parts[1]) or {}
    if not isinstance(fm_raw, dict):
        raise ValueError(f"SKILL.md frontmatter 须为 YAML 映射: {skill_md}")

    body = parts[2].lstrip("\n")
    frontmatter = Frontmatter.model_validate(fm_raw)

    references: dict[str, str] = {}
    ref_root = skill_dir / "references"
    if ref_root.is_dir():
        for p in ref_root.rglob("*"):
            if p.is_file() and _is_text_file(p):
                rel = p.relative_to(ref_root).as_posix()
                references[rel] = p.read_text(encoding="utf-8")

    # 加载外部 references（frontmatter 中的 external_references 字段）
    _base = base_dir if base_dir else skill_dir
    for ext in fm_raw.get("external_references", []):
        ext_path = pathlib.Path(ext)
        if not ext_path.is_absolute():
            ext_path = _base / ext_path
        ext_path = ext_path.resolve()
        if not ext_path.exists():
            continue
        if ext_path.is_dir():
            for p in ext_path.rglob("*"):
                if p.is_file() and _is_text_file(p):
                    rel = p.relative_to(ext_path).as_posix()
                    key = f"{ext_path.name}/{rel}"
                    references[key] = p.read_text(encoding="utf-8")
        elif ext_path.is_file() and _is_text_file(ext_path):
            references[ext_path.name] = ext_path.read_text(encoding="utf-8")

    assets: dict[str, str] = {}
    assets_root = skill_dir / "assets"
    if assets_root.is_dir():
        for p in assets_root.rglob("*"):
            if p.is_file():
                rel = p.relative_to(assets_root).as_posix()
                assets[rel] = p.read_text(encoding="utf-8")

    scripts: dict[str, Script] = {}
    scripts_root = skill_dir / "scripts"
    if scripts_root.is_dir():
        for p in scripts_root.rglob("*.py"):
            if p.is_file():
                rel = p.relative_to(scripts_root).as_posix()
                scripts[rel] = Script(src=p.read_text(encoding="utf-8"))

    return Skill(
        frontmatter=frontmatter,
        instructions=body,
        resources=Resources(references=references, assets=assets, scripts=scripts),
    )
