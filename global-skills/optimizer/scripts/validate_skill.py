#!/usr/bin/env python3
"""Static integrity and safety validator for the optimizer skill."""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # keep the package free of __pycache__
sys.path.insert(0, str(Path(__file__).resolve().parent))
from install_platform import TARGETS  # noqa: E402

PLATFORM_CONFIGS = {
    "codex": "evals/platforms/codex.json",
    "google-antigravity": "evals/platforms/google-antigravity.json",
    "github-copilot-vscode": "evals/platforms/github-copilot-vscode.json",
    "claude-vscode": "evals/platforms/claude-vscode.json",
}
PLATFORM_REFERENCES = {
    "references/platforms/common.md",
    "references/platforms/codex.md",
    "references/platforms/google-antigravity.md",
    "references/platforms/github-copilot-vscode.md",
    "references/platforms/claude-vscode.md",
}
REQUIRED = {
    "SKILL.md",
    "GUIDE.md",
    "CHANGELOG.md",
    "VERSION",
    "references/index.md",
    "references/audit/instructions-context.md",
    "references/audit/orchestration-tools.md",
    "references/audit/security-trust.md",
    "references/audit/evaluation-metrics.md",
    "references/audit/output-contract.md",
    "references/patterns/context-state.md",
    "references/patterns/orchestration.md",
    "references/patterns/runtime-evaluation.md",
    "references/patterns/compact-response.md",
    "references/providers/openai/common.md",
    "references/providers/openai/gpt-5.4.md",
    "references/providers/openai/gpt-5.5.md",
    "references/providers/openai/gpt-5.6.md",
    *PLATFORM_REFERENCES,
    *PLATFORM_CONFIGS.values(),
    "evals/README.md",
    "schemas/eval-result.schema.json",
    "scripts/install_platform.py",
    "scripts/run_platform_eval.py",
    "scripts/grade_result.py",
    "scripts/summarize_runs.py",
    "tests/README.md",
    "tests/cases/report-language-auto-russian.md",
    "tests/expected/report-language-auto-russian.json",
    "tests/cases/report-language-explicit-override.md",
    "tests/expected/report-language-explicit-override.json",
}
# Run results are local evidence, not package content.
SKIPPED_DIRS = ("tests/runs/",)
# Fixtures describe hypothetical artifacts whose paths do not exist here.
REFERENCE_CHECK_EXEMPT = ("tests/cases/",)
INTERNAL_REF = re.compile(r"^[A-Za-z0-9_-][A-Za-z0-9_.-]*(?:/[A-Za-z0-9_.-]+)+\.(?:md|json|py|ya?ml)$")
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".py", ".txt", ".json", ""}
MAX_SKILL_LINES = 350
MAX_SKILL_BYTES = 18_000
DANGEROUS_DEFAULTS = {
    "danger-full-access",
    "dangerously-skip-permissions",
    "bypasspermissions",
    "allow-all",
    "--yes-to-all",
}


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    block = text[4:end]
    result: dict[str, str] = {}
    current = None
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            current = m.group(1)
            result[current] = m.group(2).strip()
        elif current and line.startswith("  "):
            result[current] = (result[current] + " " + line.strip()).strip()
    return result


def code_fences_balanced(text: str) -> bool:
    return len(re.findall(r"^```", text, flags=re.MULTILINE)) % 2 == 0


def referenced_paths(text: str) -> set[str]:
    """Backticked relative file paths, such as `audit/security-trust.md`."""
    refs = set()
    for value in re.findall(r"`([^`\s]+)`", text):
        value = value.rstrip(".,;:")
        if INTERNAL_REF.match(value):
            refs.add(value)
    return refs


def reference_exists(root: Path, source: Path, ref: str) -> bool:
    """Resolve from the package root, the referencing file, or the routing index."""
    bases = (root, source.parent, root / "references")
    return any((base / ref).is_file() for base in bases)


def validate_expected(root: Path, errors: list[str]) -> None:
    for path in sorted((root / "tests/expected").glob("*.json")):
        rel = path.relative_to(root).as_posix()
        try:
            spec = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid expected spec {rel}: {exc}")
            continue
        rubric, checks = spec.get("rubric"), spec.get("checks")
        if not isinstance(rubric, dict) or not isinstance(checks, dict):
            errors.append(f"expected spec {rel} needs rubric and checks objects")
            continue
        if not checks:
            errors.append(f"expected spec {rel} has no deterministic checks")
        patterns = [p for c in checks.get("required_concepts", []) for p in c.get("any", [])]
        patterns += [f.get("pattern", "") for f in checks.get("forbidden_patterns", [])]
        for pattern in patterns:
            try:
                re.compile(pattern)
            except re.error as exc:
                errors.append(f"invalid regex in {rel}: {pattern!r}: {exc}")
        case = root / "tests/cases" / f"{path.stem}.md"
        if case.exists() and "mode" in checks:
            match = re.search(r"^mode:\s*(\S+)", case.read_text(encoding="utf-8"), re.IGNORECASE | re.MULTILINE)
            mode = match.group(1) if match else "standard"
            if mode != checks["mode"]:
                errors.append(f"expected spec {rel} mode {checks['mode']!r} differs from case mode {mode!r}")


def validate_platform_config(root: Path, rel: str, errors: list[str]) -> dict | None:
    path = root / rel
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid platform config {rel}: {exc}")
        return None
    required = {"platform", "surface", "executable", "install_path", "prompt_prefix", "command_template", "output_format"}
    missing = required - set(data)
    if missing:
        errors.append(f"platform config {rel} missing keys: {sorted(missing)}")
    command = data.get("command_template")
    if not isinstance(command, list) or not command or not all(isinstance(v, str) for v in command):
        errors.append(f"platform config {rel} command_template must be a non-empty string array")
        command = []
    joined = " ".join(command).lower()
    for unsafe in DANGEROUS_DEFAULTS:
        if unsafe in joined:
            errors.append(f"unsafe default flag in {rel}: {unsafe}")
    if command and command[0] != data.get("executable"):
        errors.append(f"platform config {rel} executable does not match command_template[0]")
    install_path = str(data.get("install_path", ""))
    if install_path.startswith("/") or ".." in Path(install_path).parts:
        errors.append(f"platform config {rel} install_path must be repository-relative")
    expected_target = TARGETS.get(str(data.get("platform")))
    if expected_target is None or Path(install_path) != expected_target:
        errors.append(f"platform config {rel} install_path differs from the installer target")
    if "{prompt}" not in command:
        errors.append(f"platform config {rel} does not pass the prompt placeholder")
    safety = data.get("safety")
    if not isinstance(safety, dict) or not isinstance(safety.get("verified"), bool) or not safety.get("write_protection"):
        errors.append(f"platform config {rel} needs safety.write_protection and boolean safety.verified")
    patterns = (data.get("activation_signal") or {}).get("tool_patterns")
    if not isinstance(patterns, list):
        errors.append(f"platform config {rel} needs activation_signal.tool_patterns (may be empty)")
    else:
        for pattern in patterns:
            try:
                re.compile(pattern)
            except re.error as exc:
                errors.append(f"invalid activation pattern in {rel}: {exc}")
    return data


def validate(root: Path) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    files = [p for p in root.rglob("*")
             if p.is_file() and not p.relative_to(root).as_posix().startswith(SKIPPED_DIRS)]
    all_files = {p.relative_to(root).as_posix() for p in files}

    for rel in sorted(REQUIRED - all_files):
        errors.append(f"missing required file: {rel}")

    skill = root / "SKILL.md"
    if skill.exists():
        text = skill.read_text(encoding="utf-8")
        fm = frontmatter(text)
        if fm.get("name") != "optimizer":
            errors.append("SKILL.md frontmatter name must be optimizer")
        if not fm.get("description"):
            errors.append("SKILL.md frontmatter description is missing")
        lines = len(text.splitlines())
        size = len(text.encode("utf-8"))
        if lines > MAX_SKILL_LINES:
            errors.append(f"SKILL.md too long: {lines} lines > {MAX_SKILL_LINES}")
        if size > MAX_SKILL_BYTES:
            errors.append(f"SKILL.md too large: {size} bytes > {MAX_SKILL_BYTES}")

    case_names = {p.stem for p in (root / "tests/cases").glob("*.md")}
    expected_names = {p.stem for p in (root / "tests/expected").glob("*.json")}
    if case_names != expected_names:
        errors.append(f"fixture mismatch: cases={sorted(case_names)} expected={sorted(expected_names)}")
    if len(case_names) < 12:
        warnings.append(f"only {len(case_names)} behavioral fixtures")
    validate_expected(root, errors)

    for path in files:
        rel = path.relative_to(root).as_posix()
        if "__pycache__" in path.parts or path.suffix.lower() == ".pyc":
            errors.append(f"generated Python artifact included: {rel}")
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            errors.append(f"unexpected binary or unsupported file: {rel}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"non-UTF-8 file: {rel}")
            continue
        if "\ufeff" in text:
            warnings.append(f"BOM found: {rel}")
        if path.suffix == ".md" and not code_fences_balanced(text):
            errors.append(f"unbalanced code fences: {rel}")
        if path.suffix == ".md" and not rel.startswith(REFERENCE_CHECK_EXEMPT):
            for ref in sorted(referenced_paths(text)):
                if not reference_exists(root, path, ref):
                    errors.append(f"broken internal reference in {rel}: {ref}")
        if rel.startswith(("references/providers/", "references/platforms/")):
            if "checked_at:" not in text:
                errors.append(f"missing checked_at metadata: {rel}")
            if "verification_required_for:" not in text:
                errors.append(f"missing freshness policy: {rel}")
        if path.suffix == ".py":
            try:
                ast.parse(text, filename=rel)
            except SyntaxError as exc:
                errors.append(f"Python syntax error in {rel}: {exc}")
        if path.suffix == ".json":
            try:
                json.loads(text)
            except json.JSONDecodeError as exc:
                errors.append(f"invalid JSON in {rel}: {exc}")

    configs = []
    for rel in PLATFORM_CONFIGS.values():
        if (root / rel).exists():
            data = validate_platform_config(root, rel, errors)
            if data:
                configs.append(data)
    install_paths = [c.get("install_path") for c in configs]
    if len(install_paths) != len(set(install_paths)):
        errors.append("platform install paths must be unique")

    version = (root / "VERSION").read_text(encoding="utf-8").strip() if (root / "VERSION").exists() else ""
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        errors.append(f"invalid VERSION value: {version!r}")

    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "metrics": {
            "version": version,
            "files": len(all_files),
            "skill_lines": len(skill.read_text(encoding="utf-8").splitlines()) if skill.exists() else 0,
            "skill_bytes": len(skill.read_bytes()) if skill.exists() else 0,
            "behavioral_fixtures": len(case_names),
            "platform_profiles": len(configs),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate(args.root.resolve())
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("PASS" if result["ok"] else "FAIL")
        for item in result["errors"]:
            print(f"ERROR: {item}")
        for item in result["warnings"]:
            print(f"WARN: {item}")
        print(json.dumps(result["metrics"], indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
