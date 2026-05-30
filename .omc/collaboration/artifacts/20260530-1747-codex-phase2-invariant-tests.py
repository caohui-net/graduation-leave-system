#!/usr/bin/env python3
"""Phase 2 minimal invariant tests for the Claude-Codex collaboration workflow.

The tests mutate only a temporary copy of .omc/collaboration/. The production
collaboration journal is used only as the source fixture and for the result
artifact written by this script.
"""

from __future__ import annotations

import json
import multiprocessing as mp
import os
import shutil
import subprocess
import sys
import tempfile
import traceback
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[3]
SOURCE_COLLAB_DIR = REPO_ROOT / ".omc" / "collaboration"
SOURCE_SKILL_SCRIPTS = REPO_ROOT / ".claude" / "skills" / "claude-codex-collab" / "scripts"
RESULT_PATH = SOURCE_COLLAB_DIR / "artifacts" / "20260530-1747-codex-phase2-invariant-test-results.md"


@dataclass
class TestResult:
    name: str
    passed: bool
    details: list[str]


class Harness:
    def __init__(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="codex-phase2-invariants-"))
        self.project_root = self.temp_dir / "project"
        self.collab_dir = self.project_root / ".omc" / "collaboration"
        self.skill_scripts = (
            self.project_root / ".claude" / "skills" / "claude-codex-collab" / "scripts"
        )
        self.results: list[TestResult] = []

    def setup(self) -> None:
        self.project_root.mkdir(parents=True)
        shutil.copytree(SOURCE_COLLAB_DIR, self.collab_dir, ignore=shutil.ignore_patterns("journal.lock"))
        shutil.copytree(SOURCE_SKILL_SCRIPTS, self.skill_scripts)
        (self.collab_dir / "locks").mkdir(parents=True, exist_ok=True)

    def cleanup(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def event_script(self) -> Path:
        return self.skill_scripts / "collab_event.py"

    def task_script(self) -> Path:
        return self.skill_scripts / "collab_task.py"

    def gemini_script(self) -> Path:
        return self.collab_dir / "scripts" / "invoke-gemini-analysis.sh"

    def read_events(self) -> list[dict]:
        events = []
        with (self.collab_dir / "events.jsonl").open("r", encoding="utf-8") as handle:
            for line_no, raw in enumerate(handle, 1):
                raw = raw.strip()
                if not raw:
                    raise AssertionError(f"blank event line at {line_no}")
                events.append(json.loads(raw))
        return events

    def read_state(self) -> dict:
        return json.loads((self.collab_dir / "state.json").read_text(encoding="utf-8"))

    def run_cmd(
        self,
        cmd: list[str],
        *,
        env: dict[str, str] | None = None,
        check: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            cmd,
            cwd=self.project_root,
            env=env,
            text=True,
            capture_output=True,
        )
        if check and result.returncode != 0:
            raise AssertionError(
                f"command failed ({result.returncode}): {' '.join(cmd)}\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )
        return result

    def record(self, name: str, fn) -> None:
        details: list[str] = []
        try:
            fn(details)
        except Exception as exc:  # noqa: BLE001 - test harness reports failures.
            details.append(f"{type(exc).__name__}: {exc}")
            details.append(traceback.format_exc(limit=6))
            self.results.append(TestResult(name, False, details))
        else:
            self.results.append(TestResult(name, True, details))

    def assert_no_duplicate_ids(self, events: list[dict]) -> None:
        ids = [event["id"] for event in events]
        duplicates = sorted({event_id for event_id in ids if ids.count(event_id) > 1})
        if duplicates:
            raise AssertionError(f"duplicate event ids: {duplicates}")

    def test_sequential_event_append(self, details: list[str]) -> None:
        task_id = "TASK-PHASE2-SEQUENTIAL"
        before = self.read_events()
        start_max = max(event["id"] for event in before)

        for index in range(3):
            result = self.run_cmd(
                [
                    sys.executable,
                    str(self.event_script()),
                    "artifact_created",
                    "codex",
                    task_id,
                    f"Phase 2 sequential append probe {index + 1}",
                    "[]",
                ],
                check=True,
            )
            details.append(result.stdout.strip())

        events = self.read_events()
        state = self.read_state()
        new_ids = [event["id"] for event in events[-3:]]
        expected = [start_max + 1, start_max + 2, start_max + 3]
        if new_ids != expected:
            raise AssertionError(f"expected appended ids {expected}, got {new_ids}")

        self.assert_no_duplicate_ids(events)
        max_event_id = max(event["id"] for event in events)
        if state["last_event_id"] != max_event_id:
            raise AssertionError(
                f"state.last_event_id={state['last_event_id']} max_event_id={max_event_id}"
            )

        details.append(f"appended ids contiguous: {new_ids}")
        details.append(f"state.last_event_id matches max event id: {max_event_id}")

    def test_atomic_claim_simulation(self, details: list[str]) -> None:
        task_id = "TASK-PHASE2-ATOMIC-CLAIM"
        barrier = mp.Barrier(3)
        queue: mp.Queue = mp.Queue()
        workers = [
            mp.Process(target=claim_worker, args=(self.project_root, task_id, "codex-a", barrier, queue)),
            mp.Process(target=claim_worker, args=(self.project_root, task_id, "codex-b", barrier, queue)),
        ]

        for worker in workers:
            worker.start()

        barrier.wait(timeout=10)

        outcomes = [queue.get(timeout=15) for _ in workers]
        for worker in workers:
            worker.join(timeout=5)
            if worker.exitcode not in (0, None):
                details.append(f"worker process exitcode: {worker.exitcode}")

        successes = [outcome for outcome in outcomes if outcome["returncode"] == 0]
        failures = [outcome for outcome in outcomes if outcome["returncode"] != 0]
        for outcome in sorted(outcomes, key=lambda item: item["agent"]):
            details.append(
                f"{outcome['agent']} rc={outcome['returncode']} "
                f"stdout={outcome['stdout'].strip()} stderr={outcome['stderr'].strip()}"
            )

        if len(successes) != 1 or len(failures) != 1:
            raise AssertionError(f"expected 1 success and 1 failure, got {outcomes}")

        claim_events = [
            event
            for event in self.read_events()
            if event.get("task_id") == task_id and event.get("type") == "task_claimed"
        ]
        if len(claim_events) != 1:
            raise AssertionError(f"expected 1 task_claimed event, got {len(claim_events)}")

        self.assert_no_duplicate_ids(self.read_events())
        details.append(f"single winning claim event id: {claim_events[0]['id']}")

    def test_independent_analysis_status(self, details: list[str]) -> None:
        task_id = "TASK-PHASE2-INDEPENDENT-ANALYSIS"
        self.run_cmd(
            [
                sys.executable,
                str(self.event_script()),
                "independent_analysis_completed",
                "codex",
                task_id,
                "Phase 2 independent analysis status probe",
                "[]",
            ],
            check=True,
        )

        events = self.read_events()
        state = self.read_state()
        event = events[-1]
        if event["type"] != "independent_analysis_completed":
            raise AssertionError(f"last event type mismatch: {event['type']}")
        if event["status"] != "waiting_synthesis":
            raise AssertionError(f"event status should be waiting_synthesis, got {event['status']}")
        if state["status"] != "waiting_synthesis":
            raise AssertionError(f"state status should be waiting_synthesis, got {state['status']}")

        details.append(f"event id {event['id']} status: {event['status']}")
        details.append(f"state status: {state['status']}")

    def test_gemini_dry_run_artifact_creation(self, details: list[str]) -> None:
        task_id = "TASK-PHASE2-GEMINI-DRY-RUN"
        prompt = "Phase 2 Gemini dry run invariant"
        before_artifacts = set((self.collab_dir / "artifacts").glob("*gemini-*.md"))
        env = os.environ.copy()
        env["PATH"] = self.no_gemini_path()

        if shutil.which("gemini", path=env["PATH"]) is not None:
            raise AssertionError("test PATH unexpectedly resolves a gemini executable")

        result = self.run_cmd(
            [
                "/bin/bash",
                str(self.gemini_script()),
                "--task-id",
                task_id,
                "--prompt",
                prompt,
                "--dry-run",
            ],
            env=env,
            check=False,
        )
        details.append(f"dry-run returncode: {result.returncode}")
        details.append(f"stdout: {result.stdout.strip()}")
        details.append(f"stderr: {result.stderr.strip()}")

        if result.returncode != 0:
            raise AssertionError("Gemini dry-run returned non-zero")
        if "Gemini CLI not found" in result.stdout or "Gemini CLI not found" in result.stderr:
            raise AssertionError("dry-run reached Gemini CLI availability check")

        after_artifacts = set((self.collab_dir / "artifacts").glob("*gemini-*.md"))
        new_artifacts = sorted(after_artifacts - before_artifacts)
        if not new_artifacts:
            raise AssertionError("dry-run did not create a Gemini artifact")

        artifact = new_artifacts[-1]
        content = artifact.read_text(encoding="utf-8")
        if "Dry-run" not in content or prompt not in content:
            raise AssertionError(f"artifact content missing dry-run marker or prompt: {artifact}")

        events = self.read_events()
        matching = [
            event
            for event in events
            if event.get("task_id") == task_id
            and event.get("type") == "analysis_requested"
            and event.get("agent") == "gemini"
        ]
        if len(matching) != 1:
            raise AssertionError(f"expected one Gemini analysis_requested event, got {len(matching)}")
        if not matching[0].get("artifacts"):
            raise AssertionError("Gemini dry-run event did not include artifact path")

        details.append(f"artifact created: {artifact.relative_to(self.project_root)}")
        details.append(f"event logged: id {matching[0]['id']}")

    def no_gemini_path(self) -> str:
        bin_dir = self.temp_dir / "no-gemini-bin"
        bin_dir.mkdir(exist_ok=True)
        for name in ["cat", "cut", "date", "dirname", "pwd", "python3", "tr"]:
            source = shutil.which(name)
            if not source:
                raise AssertionError(f"required command not found for dry-run PATH: {name}")
            link = bin_dir / name
            if not link.exists():
                link.symlink_to(source)
        return str(bin_dir)

    def write_results(self) -> None:
        now = datetime.now(timezone.utc).isoformat()
        passed = all(result.passed for result in self.results)
        lines = [
            "# Phase 2 Minimal Invariant Test Results",
            "",
            f"**Task:** TASK-20260530-06",
            f"**Agent:** Codex",
            f"**Timestamp:** {now}",
            f"**Result:** {'PASS' if passed else 'FAIL'}",
            f"**Fixture:** temporary copy of `.omc/collaboration/` under `{self.temp_dir}`",
            "",
            "## Summary",
            "",
        ]
        for result in self.results:
            lines.append(f"- {'PASS' if result.passed else 'FAIL'}: {result.name}")

        lines.extend(["", "## Details", ""])
        for result in self.results:
            lines.append(f"### {result.name}")
            lines.append("")
            lines.append(f"Status: {'PASS' if result.passed else 'FAIL'}")
            lines.append("")
            for detail in result.details:
                lines.append("```")
                lines.append(detail.encode("ascii", "backslashreplace").decode("ascii"))
                lines.append("```")
                lines.append("")

        lines.extend(
            [
                "## Stop Rule",
                "",
                (
                    "No repair task required because all Phase 2 tests passed."
                    if passed
                    else "Repair task required before Phase 3 because at least one Phase 2 test failed."
                ),
                "",
            ]
        )
        RESULT_PATH.write_text("\n".join(lines), encoding="utf-8")


def claim_worker(project_root: Path, task_id: str, agent: str, barrier: mp.Barrier, queue: mp.Queue) -> None:
    try:
        barrier.wait(timeout=10)
        script = project_root / ".claude" / "skills" / "claude-codex-collab" / "scripts" / "collab_task.py"
        result = subprocess.run(
            [sys.executable, str(script), "claim", task_id, agent],
            cwd=project_root,
            text=True,
            capture_output=True,
        )
        queue.put(
            {
                "agent": agent,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        )
    except Exception as exc:  # noqa: BLE001 - worker reports failures through queue.
        queue.put({"agent": agent, "returncode": 99, "stdout": "", "stderr": repr(exc)})


def main() -> int:
    harness = Harness()
    try:
        harness.setup()
        harness.record("Sequential event append consistency", harness.test_sequential_event_append)
        harness.record("Atomic claim simulation", harness.test_atomic_claim_simulation)
        harness.record("Independent analysis event status", harness.test_independent_analysis_status)
        harness.record("Gemini dry-run artifact creation", harness.test_gemini_dry_run_artifact_creation)
        harness.write_results()

        for result in harness.results:
            print(f"{'PASS' if result.passed else 'FAIL'}: {result.name}")
        print(f"Result artifact: {RESULT_PATH}")
        return 0 if all(result.passed for result in harness.results) else 1
    finally:
        harness.cleanup()


if __name__ == "__main__":
    sys.exit(main())
