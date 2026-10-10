"""Deterministic regression tests for optimizer scripts (no LLM required).

Run from the package root:  python -m unittest discover -s tests/unit
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.dont_write_bytecode = True  # the validator rejects __pycache__ in the package
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import grade_result  # noqa: E402
import install_platform  # noqa: E402
import run_platform_eval  # noqa: E402
import summarize_runs  # noqa: E402
import validate_skill  # noqa: E402

GOOD_ZERO = {
    "schema_version": "2.0",
    "metadata": {"mode": "quick", "report_language": "en"},
    "no_material_issue": True,
    "findings": [],
    "validation": ["Static review of the supplied prompt description."],
}
FINDING = {
    "id": "OPT-001",
    "severity": "medium",
    "confidence": "high",
    "evidence_type": "static",
    "problem": "Проблема: навык загружает все справочники перед каждой задачей.",
    "evidence": [{"location": "SKILL.md", "summary": "Безусловная загрузка каталога справочников."}],
    "recommendation": "Добавить маршрутизацию и загружать только нужные справочники.",
}


def claude_stream(result_obj: dict, read_skill: bool = True) -> str:
    events = [{"type": "system", "subtype": "init", "model": "test-model"}]
    if read_skill:
        events.append({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": "Read",
             "input": {"file_path": "C:\\sandbox\\.claude\\skills\\optimizer\\SKILL.md"}}]}})
    events.append({"type": "result", "result": json.dumps(result_obj),
                   "usage": {"input_tokens": 100, "output_tokens": 50}, "total_cost_usd": 0.01, "num_turns": 2})
    return "\n".join(json.dumps(e) for e in events)


class Workspace(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="optimizer-test-"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)


class ValidatorReferences(Workspace):
    def copy_package(self) -> Path:
        dest = self.tmp / "optimizer"
        shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns("runs", "__pycache__"))
        return dest

    def test_relative_reference_in_routing_index_is_resolved(self):
        self.assertTrue(validate_skill.validate(self.copy_package())["ok"])

    def test_missing_relative_reference_is_reported(self):
        pkg = self.copy_package()
        index = pkg / "references/index.md"
        index.write_text(index.read_text(encoding="utf-8") + "\n| Extra | `audit/missing-file.md` |\n",
                         encoding="utf-8")
        errors = validate_skill.validate(pkg)["errors"]
        self.assertIn("broken internal reference in references/index.md: audit/missing-file.md", errors)

    def test_missing_reference_from_skill_routing_list(self):
        pkg = self.copy_package()
        (pkg / "references/audit/security-trust.md").unlink()
        errors = validate_skill.validate(pkg)["errors"]
        self.assertTrue(any("SKILL.md: audit/security-trust.md" in e for e in errors), errors)

    def test_fixture_paths_are_exempt(self):
        self.assertEqual(validate_skill.referenced_paths("`.github/copilot-instructions.md`"), set())


class Installer(Workspace):
    def test_failed_copy_keeps_previous_installation(self):
        target = self.tmp / ".claude/skills/optimizer"
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text("previous", encoding="utf-8")
        with mock.patch.object(install_platform.shutil, "copytree", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                install_platform.install(ROOT, self.tmp, "claude-vscode", "copy", force=True, dry_run=False)
        self.assertEqual((target / "SKILL.md").read_text(encoding="utf-8"), "previous")
        self.assertEqual(sorted(p.name for p in target.parent.iterdir()), ["optimizer"])

    def test_force_replaces_and_matches_source_hash(self):
        target = self.tmp / ".agents/skills/optimizer"
        target.mkdir(parents=True)
        (target / "stale.txt").write_text("old", encoding="utf-8")
        install_platform.install(ROOT, self.tmp, "codex", "copy", force=True, dry_run=False)
        self.assertFalse((target / "stale.txt").exists())
        self.assertEqual(install_platform.tree_hash(target), install_platform.tree_hash(ROOT))

    def test_eval_install_excludes_grading_keys(self):
        target = install_platform.install(ROOT, self.tmp, "codex", "copy", force=False, dry_run=False,
                                          exclude_dev=True)
        self.assertFalse((target / "tests").exists())
        keys = run_platform_eval.expected_hashes(ROOT)
        self.assertEqual(run_platform_eval.leaked_files(self.tmp, keys), [])
        shutil.copytree(ROOT / "tests/expected", self.tmp / "copied")
        self.assertTrue(run_platform_eval.leaked_files(self.tmp, keys))


class PromptIsolation(unittest.TestCase):
    def test_prompt_never_contains_expected_content(self):
        config = json.loads((ROOT / "evals/platforms/codex.json").read_text(encoding="utf-8"))
        for case in sorted((ROOT / "tests/cases").glob("*.md")):
            prompt = run_platform_eval.prompt_for(config, case.read_text(encoding="utf-8"))
            spec = grade_result.load_spec(case.stem)
            for item in spec["rubric"]["required"] + spec["rubric"]["forbidden"]:
                self.assertNotIn(item, prompt, case.stem)
            self.assertNotIn("required_concepts", prompt)


class Grading(unittest.TestCase):
    def setUp(self):
        self.spec = grade_result.load_spec("zero-findings")

    def test_empty_response_never_passes(self):
        graded = grade_result.grade("", self.spec)
        self.assertFalse(graded["schema_valid"])
        self.assertEqual(graded["semantic_status"], "not_graded")

    def test_prose_response_is_schema_invalid(self):
        self.assertFalse(grade_result.grade("Looks fine to me.", self.spec)["schema_valid"])

    def test_wrong_shape_is_schema_invalid(self):
        graded = grade_result.grade(json.dumps({"findings": "none"}), self.spec)
        self.assertFalse(graded["schema_valid"])
        self.assertTrue(graded["schema_errors"])

    def test_valid_zero_findings_passes(self):
        graded = grade_result.grade("```json\n" + json.dumps(GOOD_ZERO) + "\n```", self.spec)
        self.assertTrue(graded["schema_valid"], graded["schema_errors"])
        self.assertEqual(graded["semantic_status"], "pass")
        self.assertEqual(graded["rubric_review"], "pending")

    def test_invented_finding_fails_zero_findings_case(self):
        invented = dict(GOOD_ZERO, no_material_issue=False,
                        findings=[dict(FINDING, severity="high", problem="Invented risk.")])
        self.assertEqual(grade_result.grade(json.dumps(invented), self.spec)["semantic_status"], "fail")

    def test_report_language_russian(self):
        spec = grade_result.load_spec("report-language-auto-russian")
        ok = dict(GOOD_ZERO, metadata={"mode": "standard", "report_language": "ru"},
                  no_material_issue=False, findings=[FINDING],
                  validation=["Статическая проверка `SKILL.md` без измерений."])
        self.assertEqual(grade_result.grade(json.dumps(ok), spec)["semantic_status"], "pass")
        english = dict(ok, metadata={"mode": "standard", "report_language": "en"},
                       findings=[dict(FINDING, problem="Loads every reference.", recommendation="Route references.",
                                      evidence=[{"location": "SKILL.md", "summary": "Unconditional load."}])])
        self.assertEqual(grade_result.grade(json.dumps(english), spec)["semantic_status"], "fail")

    def test_activation_ignores_agent_prose(self):
        config = {"activation_signal": {"tool_patterns": [r"skills[\\/]+optimizer[\\/]+SKILL\.md"]}}
        prose_only = grade_result.extract_response(
            "stream-json", claude_stream(GOOD_ZERO, read_skill=False).replace(
                '"result": "', '"result": "I read .claude/skills/optimizer/SKILL.md ', 1))
        self.assertEqual(grade_result.activation_status(config, prose_only["events"]), "unverified")
        real = grade_result.extract_response("stream-json", claude_stream(GOOD_ZERO))
        self.assertEqual(grade_result.activation_status(config, real["events"]), "verified")


class Runner(Workspace):
    def setUp(self):
        super().setUp()
        self.config = json.loads((ROOT / "evals/platforms/claude-vscode.json").read_text(encoding="utf-8"))
        self.context = {"run_id": "test", "skill_version": (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
                        "skill_hash": install_platform.tree_hash(ROOT, exclude_dev=True)}
        self.case = ROOT / "tests/cases/zero-findings.md"
        self.out = self.tmp / "runs"

    def run_case(self, fake_run, config=None, allow=False):
        def dispatch(args, **kwargs):
            if "--version" in args:
                return subprocess.CompletedProcess(args, 0, "9.9.9\n", "")
            return fake_run(args, **kwargs)

        with mock.patch.object(run_platform_eval.shutil, "which", return_value="claude"), \
                mock.patch.object(run_platform_eval.subprocess, "run", side_effect=dispatch) as patched:
            record = run_platform_eval.run_one(config or self.config, self.case, None, self.out, 5, False,
                                               {"max_turns": "1", "budget_usd": "0.1", "credit_limit": "1"},
                                               self.context, allow, False)
        return record, patched

    def test_verified_run_passes_and_records_metrics(self):
        record, _ = self.run_case(lambda args, **kw: subprocess.CompletedProcess(args, 0, claude_stream(GOOD_ZERO), ""))
        self.assertEqual(record["verdict"], "PASS", record)
        self.assertTrue(record["install_verified"])
        self.assertEqual(record["cli_version"], "9.9.9")
        self.assertEqual(record["usage"], {"input_tokens": 100, "output_tokens": 50})
        self.assertTrue((self.out / "claude-vscode--zero-findings.json").exists())

    def test_zero_exit_with_empty_response_fails(self):
        record, _ = self.run_case(lambda args, **kw: subprocess.CompletedProcess(args, 0, "", ""))
        self.assertTrue(record["execution_success"])
        self.assertFalse(record["schema_valid"])
        self.assertEqual(record["verdict"], "FAIL")

    def test_missing_activation_is_unverified(self):
        record, _ = self.run_case(
            lambda args, **kw: subprocess.CompletedProcess(args, 0, claude_stream(GOOD_ZERO, read_skill=False), ""))
        self.assertEqual(record["verdict"], "UNVERIFIED")

    def test_timeout_with_bytes_output_is_recorded(self):
        def timeout(args, **kw):
            raise subprocess.TimeoutExpired(args, 5, output=b"partial \xff", stderr=b"slow")

        record, _ = self.run_case(timeout)
        self.assertEqual(record["exit_code"], 124)
        self.assertTrue(record["timed_out"])
        self.assertTrue(record["stdout"].startswith("partial"))
        self.assertIn("timeout after 5s", record["stderr"])
        self.assertEqual(record["verdict"], "FAIL")
        self.assertTrue((self.out / "claude-vscode--zero-findings.json").exists())

    def test_sandbox_mutation_is_a_safety_violation(self):
        def writer(args, cwd, **kw):
            (Path(cwd) / "notes.txt").write_text("written by agent", encoding="utf-8")
            return subprocess.CompletedProcess(args, 0, claude_stream(GOOD_ZERO), "")

        record, _ = self.run_case(writer)
        self.assertEqual(record["safety"], "violation")
        self.assertIn("created notes.txt", record["workspace_mutations"])
        self.assertEqual(record["verdict"], "FAIL")

    def test_unverified_write_protection_is_blocked_without_opt_in(self):
        config = dict(self.config, safety={"write_protection": "none", "verified": False})
        record, patched = self.run_case(lambda args, **kw: self.fail("must not execute"), config=config)
        self.assertEqual(record["verdict"], "BLOCKED")
        patched.assert_not_called()

    def test_previous_results_are_not_overwritten(self):
        ok = lambda args, **kw: subprocess.CompletedProcess(args, 0, claude_stream(GOOD_ZERO), "")  # noqa: E731
        self.run_case(ok)
        with self.assertRaises(FileExistsError):
            self.run_case(ok)

    def test_as_text_decodes_bytes(self):
        self.assertEqual(run_platform_eval.as_text(b"a\xffb"), "a\ufffdb")
        self.assertEqual(run_platform_eval.as_text(None), "")


class Summaries(unittest.TestCase):
    def record(self, verdict, tokens, cost, duration=1000):
        usage = {"input_tokens": tokens, "output_tokens": 0} if tokens is not None else "unknown"
        return {"platform": "codex", "case": f"c{duration}", "verdict": verdict, "duration_ms": duration,
                "usage": usage, "cost_usd": cost if cost is not None else "unknown"}

    def test_failed_attempts_are_charged_to_successes(self):
        summary = summarize_runs.summarize([self.record("PASS", 100, 0.1, 1000), self.record("FAIL", 300, 0.3, 2000)])
        self.assertEqual(summary["success_rate"], 0.5)
        self.assertEqual(summary["tokens_per_successful_task"], 400)

    def test_unknown_usage_is_not_estimated(self):
        summary = summarize_runs.summarize([self.record("PASS", 100, 0.1), self.record("PASS", None, None, 2000)])
        self.assertEqual(summary["tokens_per_successful_task"], "unknown")
        self.assertEqual(summary["cost_per_successful_task_usd"], "unknown")


if __name__ == "__main__":
    unittest.main()
