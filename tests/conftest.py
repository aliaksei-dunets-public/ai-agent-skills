"""Fixtures shared by all skill tests."""

from pathlib import Path

import pytest


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """Project root with an empty .tmp/ (the path has a space on purpose)."""
    root = tmp_path / "my project"
    (root / ".tmp").mkdir(parents=True)
    return root


@pytest.fixture
def root(tmp_path: Path) -> Path:
    """Empty project root for project-init tests."""
    path = tmp_path / "my project"
    path.mkdir()
    return path
