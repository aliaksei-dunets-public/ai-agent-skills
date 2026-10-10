#!/usr/bin/env python3
"""Install optimizer into a repository path used by a supported platform.

Installation is staged: the new copy is built and verified next to the target,
then swapped in. A failed copy or swap leaves the previous installation intact.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
import uuid
from pathlib import Path

TARGETS = {
    "codex": Path(".agents/skills/optimizer"),
    "google-antigravity": Path(".agent/skills/optimizer"),
    "github-copilot-vscode": Path(".github/skills/optimizer"),
    "claude-vscode": Path(".claude/skills/optimizer"),
}
EXCLUDES = {"__pycache__", ".git", "runs"}
# Grading keys and fixtures must never be readable by an agent under evaluation.
DEV_EXCLUDES = {"tests"}


def _skip(name: str) -> bool:
    return name in EXCLUDES or name.endswith((".pyc", ".zip"))


def ignore_for(source: Path, exclude_dev: bool):
    source = source.resolve()

    def ignored(path: str, names: list[str]) -> set[str]:
        skip = {name for name in names if _skip(name)}
        if exclude_dev and Path(path).resolve() == source:
            skip |= {name for name in names if name in DEV_EXCLUDES}
        return skip

    return ignored


def iter_files(root: Path, exclude_dev: bool = False) -> list[Path]:
    """Return installable files below root in a stable order."""
    root = root.resolve()
    files = []
    for current, dirs, names in os.walk(root):
        here = Path(current)
        dirs[:] = sorted(
            d for d in dirs
            if not _skip(d) and not (exclude_dev and here == root and d in DEV_EXCLUDES)
        )
        files.extend(here / n for n in sorted(names) if not _skip(n))
    return files


def tree_hash(root: Path, exclude_dev: bool = False) -> str:
    """Content hash of the installable tree; identical for a source and its copy."""
    root = root.resolve()
    digest = hashlib.sha256()
    for path in iter_files(root, exclude_dev):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def _remove(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)


def install(source: Path, repo: Path, platform: str, mode: str, force: bool, dry_run: bool,
            exclude_dev: bool = False) -> Path:
    target = (repo / TARGETS[platform]).resolve()
    source = source.resolve()
    if target == source:
        return target
    if source in target.parents:
        raise ValueError("target cannot be inside the optimizer source directory")
    if mode == "symlink" and exclude_dev:
        raise ValueError("symlink mode cannot exclude development files")
    if (target.exists() or target.is_symlink()) and not force:
        raise FileExistsError(f"target exists: {target}; use --force to replace it")
    if dry_run:
        return target

    target.parent.mkdir(parents=True, exist_ok=True)
    token = uuid.uuid4().hex[:8]
    staging = target.parent / f".{target.name}.staging-{token}"
    backup = target.parent / f".{target.name}.backup-{token}"
    try:
        if mode == "symlink":
            staging.symlink_to(source, target_is_directory=True)
        else:
            shutil.copytree(source, staging, ignore=ignore_for(source, exclude_dev))
            if not (staging / "SKILL.md").is_file():
                raise OSError("staged copy has no SKILL.md")
            if tree_hash(staging) != tree_hash(source, exclude_dev):
                raise OSError("staged copy does not match the source")
    except BaseException:
        _remove(staging)
        raise

    had_previous = target.exists() or target.is_symlink()
    if had_previous:
        os.rename(target, backup)
    try:
        os.rename(staging, target)
    except BaseException:
        if had_previous:
            os.rename(backup, target)
        _remove(staging)
        raise
    if had_previous:
        _remove(backup)
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--platform", choices=[*TARGETS, "all"], required=True)
    parser.add_argument("--mode", choices=["copy", "symlink"], default="copy")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--exclude-dev", action="store_true",
                        help="omit tests/ (required for installations used by evals)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    source = Path(__file__).resolve().parents[1]
    repo = args.repo.resolve()
    platforms = list(TARGETS) if args.platform == "all" else [args.platform]
    try:
        for platform in platforms:
            target = install(source, repo, platform, args.mode, args.force, args.dry_run, args.exclude_dev)
            verb = "would install" if args.dry_run else "installed"
            print(f"{platform}: {verb} -> {target}")
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
