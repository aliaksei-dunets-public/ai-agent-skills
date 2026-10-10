#!/usr/bin/env python3
"""Grade an optimizer response independently of the agent that produced it.

The grader runs after execution and is the only consumer of `tests/expected/`.
It separates three questions that a zero exit code does not answer:

- schema_valid: the response is one JSON object matching the canonical schema;
- semantic_status: deterministic case checks pass (`pass`, `fail`, or
  `not_graded` when the schema is invalid);
- rubric_review: natural-language rubric items still need a human or external
  judge; they are reported as `pending`, never as passed.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas/eval-result.schema.json"

_TYPES = {
    "object": dict,
    "array": list,
    "string": str,
    "boolean": bool,
    "null": type(None),
}


# --- minimal JSON Schema (draft 2020-12 subset used by this package) ---------

def _type_ok(value, expected: str) -> bool:
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return isinstance(value, _TYPES[expected])


def _resolve(ref: str, root: dict) -> dict:
    if not ref.startswith("#/"):
        raise ValueError(f"unsupported $ref: {ref}")
    node = root
    for part in ref[2:].split("/"):
        node = node[part]
    return node


def validate_schema(value, schema: dict, root: dict | None = None, path: str = "$") -> list[str]:
    """Return schema violations; an empty list means valid."""
    root = root if root is not None else schema
    if "$ref" in schema:
        return validate_schema(value, _resolve(schema["$ref"], root), root, path)
    errors: list[str] = []
    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_type_ok(value, t) for t in types):
            return [f"{path}: expected {'|'.join(types)}"]
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected constant {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} not in {schema['enum']}")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: string shorter than {schema['minLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{path}: does not match {schema['pattern']}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: fewer than {schema['minItems']} items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path}: more than {schema['maxItems']} items")
        if "items" in schema:
            for i, item in enumerate(value):
                errors += validate_schema(item, schema["items"], root, f"{path}[{i}]")
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing required {key!r}")
        props = schema.get("properties", {})
        extra = schema.get("additionalProperties", True)
        for key, item in value.items():
            if key in props:
                errors += validate_schema(item, props[key], root, f"{path}.{key}")
            elif extra is False:
                errors.append(f"{path}: unexpected property {key!r}")
            elif isinstance(extra, dict):
                errors += validate_schema(item, extra, root, f"{path}.{key}")
    return errors


# --- response extraction ----------------------------------------------------

def _json_lines(stdout: str) -> list[dict]:
    events = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            events.append(event)
    return events


def _add_usage(total: dict, usage: dict) -> None:
    for key, value in usage.items():
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            total[key] = total.get(key, 0) + value


def extract_response(output_format: str, stdout: str) -> dict:
    """Normalize platform output into final text, events, and usage.

    Unknown values stay `None`; nothing is estimated.
    """
    result = {"text": stdout, "events": [], "usage": None, "cost_usd": None,
              "num_turns": None, "model": None}
    if output_format == "json":
        try:
            data = json.loads(stdout)
        except json.JSONDecodeError:
            return result
        if isinstance(data, dict):
            result.update(text=str(data.get("result", "")), usage=data.get("usage"),
                          cost_usd=data.get("total_cost_usd"), num_turns=data.get("num_turns"))
        return result
    if output_format == "stream-json":
        events = _json_lines(stdout)
        result.update(events=events, text="")
        for event in events:
            if event.get("type") == "system" and event.get("model"):
                result["model"] = event["model"]
            if event.get("type") == "result":
                result.update(text=str(event.get("result", "")), usage=event.get("usage"),
                              cost_usd=event.get("total_cost_usd"), num_turns=event.get("num_turns"))
        return result
    if output_format == "jsonl":
        events = _json_lines(stdout)
        usage: dict = {}
        texts = []
        turns = 0
        for event in events:
            item = event.get("item") if isinstance(event.get("item"), dict) else {}
            if item.get("type") == "agent_message" and isinstance(item.get("text"), str):
                texts.append(item["text"])
            if event.get("type") == "turn.completed":
                turns += 1
                if isinstance(event.get("usage"), dict):
                    _add_usage(usage, event["usage"])
        result.update(events=events, text=texts[-1] if texts else "",
                      usage=usage or None, num_turns=turns or None)
        return result
    return result


def tool_evidence(events: list[dict]) -> list[str]:
    """Serialized tool calls only; agent prose cannot fake an activation signal."""
    found = []
    for event in events:
        message = event.get("message")
        if isinstance(message, dict) and isinstance(message.get("content"), list):
            for part in message["content"]:
                if isinstance(part, dict) and part.get("type") == "tool_use":
                    found.append(json.dumps({"name": part.get("name"), "input": part.get("input")}))
        item = event.get("item")
        if isinstance(item, dict) and item.get("type") not in {None, "agent_message", "reasoning"}:
            found.append(json.dumps(item))
    return found


def activation_status(config: dict, events: list[dict]) -> str:
    signal = config.get("activation_signal") or {}
    patterns = signal.get("tool_patterns") or []
    if not patterns:
        return "unverified"
    calls = tool_evidence(events)
    for pattern in patterns:
        if any(re.search(pattern, call, flags=re.IGNORECASE) for call in calls):
            return "verified"
    return "unverified"


def parse_result_json(text: str) -> tuple[dict | None, str | None]:
    text = (text or "").strip()
    if not text:
        return None, "empty response"
    candidates = [text]
    candidates += re.findall(r"```(?:json)?\s*\n(.*?)```", text, flags=re.DOTALL)[::-1]
    start, end = text.find("{"), text.rfind("}")
    if 0 <= start < end:
        candidates.append(text[start:end + 1])
    for candidate in candidates:
        try:
            data = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict):
            return data, None
        return None, "response JSON is not an object"
    return None, "no JSON object found in response"


# --- deterministic checks ---------------------------------------------------

def _prose(data: dict) -> str:
    parts = []
    for finding in data.get("findings", []):
        for key in ("category", "problem", "root_cause", "recommendation"):
            if isinstance(finding.get(key), str):
                parts.append(finding[key])
        for ev in finding.get("evidence", []) or []:
            if isinstance(ev, dict) and isinstance(ev.get("summary"), str):
                parts.append(ev["summary"])
    for key in ("recommendations", "questions", "validation"):
        parts += [v for v in data.get(key, []) or [] if isinstance(v, str)]
    return "\n".join(parts)


def _strip_technical(text: str) -> str:
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"\S*[/\\.]\S*", " ", text)  # paths, file names, URLs
    return text


def script_share(text: str, script: str) -> float:
    letters = [ch for ch in _strip_technical(text) if ch.isalpha()]
    if not letters:
        return 0.0
    if script == "cyrillic":
        hits = sum("Ѐ" <= ch <= "ӿ" for ch in letters)
    else:
        hits = sum(ch.isascii() or "À" <= ch <= "ɏ" for ch in letters)
    return hits / len(letters)


LANGUAGE_SCRIPTS = {"ru": "cyrillic", "uk": "cyrillic", "en": "latin", "es": "latin", "de": "latin"}
SPANISH_MARKERS = re.compile(r"\b(el|la|los|las|de|del|que|para|una?|se|por|con|no)\b", re.IGNORECASE)


def run_checks(data: dict, checks: dict) -> list[dict]:
    results = []

    def record(check_id: str, passed: bool, detail: str = "") -> None:
        results.append({"id": check_id, "passed": bool(passed), "detail": detail})

    findings = data.get("findings", [])
    prose = _prose(data)
    serialized = json.dumps(data, ensure_ascii=False)

    if "mode" in checks:
        actual = data.get("metadata", {}).get("mode")
        record("mode", actual == checks["mode"], f"expected {checks['mode']}, got {actual}")
    if "no_material_issue" in checks:
        expected = checks["no_material_issue"]
        actual = data.get("no_material_issue")
        consistent = (not actual) or not findings
        record("no_material_issue", actual == expected and consistent,
               f"expected {expected}, got {actual} with {len(findings)} findings")
    if "min_findings" in checks:
        record("min_findings", len(findings) >= checks["min_findings"],
               f"{len(findings)} < {checks['min_findings']}" if len(findings) < checks["min_findings"] else "")
    if "max_findings" in checks:
        limit = checks["max_findings"]
        extra = [f for f in findings[limit:] if f.get("severity") not in {"critical", "high"}]
        record("max_findings", not extra,
               f"{len(findings)} findings exceed {limit} with non-high extras" if extra else "")
    for concept in checks.get("required_concepts", []):
        hit = any(re.search(p, prose, flags=re.IGNORECASE) for p in concept["any"])
        record(f"concept:{concept['id']}", hit, "" if hit else "no matching finding text")
    for forbidden in checks.get("forbidden_patterns", []):
        match = re.search(forbidden["pattern"], serialized, flags=re.IGNORECASE)
        record(f"forbidden:{forbidden['id']}", match is None, match.group(0) if match else "")
    if checks.get("no_measured_metrics"):
        measured = [m.get("name") for m in data.get("metrics", []) or [] if m.get("measured")]
        record("no_measured_metrics", not measured,
               f"claims measured metrics without supplied measurements: {measured}" if measured else "")
    if "report_language" in checks:
        lang = checks["report_language"]
        tag = str(data.get("metadata", {}).get("report_language", ""))
        script = LANGUAGE_SCRIPTS.get(lang, "latin")
        share = script_share(prose, script)
        passed = tag.split("-")[0] == lang and share >= 0.8
        if passed and lang == "es":
            passed = len(SPANISH_MARKERS.findall(prose)) >= 3
        record("report_language", passed, f"metadata={tag!r}, {script} share={share:.2f}")
    return results


def grade(response_text: str, spec: dict, schema: dict | None = None) -> dict:
    schema = schema if schema is not None else json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    data, parse_error = parse_result_json(response_text)
    graded = {
        "schema_valid": False,
        "schema_errors": [],
        "checks": [],
        "semantic_status": "not_graded",
        "rubric_review": "pending" if spec.get("rubric") else "none",
    }
    if data is None:
        graded["schema_errors"] = [parse_error]
        return graded
    errors = validate_schema(data, schema)
    graded["schema_errors"] = errors
    graded["schema_valid"] = not errors
    if errors:
        return graded
    graded["checks"] = run_checks(data, spec.get("checks", {}))
    graded["semantic_status"] = "pass" if all(c["passed"] for c in graded["checks"]) else "fail"
    return graded


def load_spec(case: str, root: Path = ROOT) -> dict:
    return json.loads((root / "tests/expected" / f"{case}.json").read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Grade a saved optimizer response.")
    parser.add_argument("--case", required=True)
    parser.add_argument("--response", type=Path, required=True, help="raw agent stdout or response text")
    parser.add_argument("--format", default="text", choices=["text", "json", "stream-json", "jsonl"])
    args = parser.parse_args()
    extracted = extract_response(args.format, args.response.read_text(encoding="utf-8"))
    result = grade(extracted["text"], load_spec(args.case))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["semantic_status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
