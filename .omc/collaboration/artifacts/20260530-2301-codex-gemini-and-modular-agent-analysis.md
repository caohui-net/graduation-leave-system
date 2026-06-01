# Codex Analysis: Gemini Invocation And Modular Agent Configuration

**Task:** TASK-20260530-06
**Timestamp:** 2026-05-30T15:01:35Z
**Agent:** Codex
**Topic:** Gemini usage contract, validation criteria, and dynamic agent registration

## Executive Position

Claude's proposals point in the right direction, but both are too permissive at the boundary where correctness matters.

For Gemini, the priority should be a narrow, direct-CLI, read-only artifact workflow with a manifest and objective validation. MCP or a generic `omc ask gemini` facade can come later after the contract is proven. The current "required fields only" validation is not enough; it proves shape, not usefulness or protocol safety.

For modular agents, do not make arbitrary dynamic agents a P0 feature. First harden the fixed Claude/Codex/Gemini model. Then introduce a registry as a gated adapter layer, where custom agents are disabled by default and can only produce artifacts unless they pass protocol conformance checks.

## Question 1: Gemini Usage And Validation

### 1. Invocation Interface

`omc ask gemini --mode=X --manifest=Y` is reasonable as a future user-facing facade, but it should not be the first authority layer.

Recommended P0:

```text
.omc/collaboration/scripts/invoke-gemini-analysis.sh --manifest <json> [--dry-run]
```

The script should call Gemini directly:

```text
gemini -p "<prompt>" --approval-mode plan --output-format text
```

Reasoning:

- Direct CLI is already locally viable and avoids MCP setup risk.
- The protocol needs deterministic artifact/event behavior more than a polished command.
- A manifest gives the collaboration layer a stable input contract independent of Gemini's prompt surface.
- `omc ask gemini` can wrap the script later without changing the underlying evidence model.

MCP should stay P2 unless there is a concrete requirement for interactive tool routing or remote execution. It expands the trust boundary before the basic read-only path is proven.

### 2. Output Validation

Checking only `analysis/findings/recommendations` is insufficient. That validates formatting, not quality or safety.

Use three validation layers:

1. **Structural validation**
   - Artifact exists under `.omc/collaboration/artifacts/`.
   - Artifact contains task id, mode, prompt summary, file manifest hash, analysis, findings, recommendations, and limitations.
   - Event is one of `analysis_requested`, `analysis_completed`, or `analysis_failed`.
   - `state.json.last_event_id` matches `events.jsonl` max id after logging.

2. **Grounding validation**
   - Every material finding references at least one input file path, line range, log excerpt, or explicit "inference" marker.
   - Recommendations are tied back to findings.
   - The artifact lists files Gemini could not inspect.
   - The artifact records the model/tool exit code and whether the run was dry-run or live.

3. **Decision validation**
   - Gemini output is advisory evidence, not an automatic decision.
   - Claude or Codex must synthesize/accept/reject findings for workflow impact.
   - Any recommendation that changes code, protocol, locks, or state must be verified by Codex or another deterministic check.

Quality should be judged by usefulness against the task, not by Gemini confidence language. A usable analysis should have source-grounded findings, actionable recommendations, explicit uncertainty, and no protocol-unsafe write behavior.

### 3. Triggering Rules

Default trigger should be Claude as router, not user-only and not autonomous Gemini.

Recommended routing:

- **User manual trigger:** allowed for explicit "ask Gemini" requests.
- **Claude trigger:** default for large-context analysis, long logs, broad document comparisons, or independent-analysis workflows.
- **Codex trigger:** allowed when implementation/review discovers a large-context question that would otherwise consume too much local context.
- **Gemini self-trigger:** disallowed.

Trigger preconditions:

- Task id exists.
- Manifest exists.
- Mode is declared.
- Expected output sections are declared.
- Failure handling is declared before live call.

### 4. Rate Limits And Timeout

The previous Gemini API 400/500-style failures mean live Gemini must be non-blocking unless the task's explicit objective is to test Gemini.

Recommended behavior:

- Use a fixed timeout, e.g. 120s for normal analysis and configurable max 300s.
- Retry at most once for transient rate/5xx errors, with short backoff.
- Do not retry 400-class invalid request errors unless the wrapper can mechanically repair the request.
- Always create a failure artifact with command, mode, sanitized error, exit code, timestamp, and retry count.
- Append `analysis_failed` with `details.error_class` such as `rate_limited`, `invalid_request`, `auth`, `timeout`, `tool_missing`, or `unknown`.
- Do not move the task to `in_progress` or `blocked` solely because Gemini failed, unless Gemini was the acceptance gate.

## Question 2: Modular Agent Configuration

### 1. P0 Or Not

Modular agents are not P0. They are a P1/P2 governance feature.

P0 should remain:

- Fixed Claude/Codex/Gemini roles.
- Read-only Gemini artifact workflow.
- Journal/state validation.
- Failure artifacts.
- Protocol-safe event typing.

Reasoning: dynamic agents multiply trust and consistency risks before the current three-agent contract is fully enforced. The current protocol already has signs of drift, for example scripts that default unknown event types to `in_progress` and state schemas that originally named only Claude/Codex/none.

### 2. Constraints If Dynamic Agents Are Supported

Dynamic agents should be treated as adapters, not peers with automatic protocol authority.

Required constraints:

- Disabled by default.
- No direct writes to `events.jsonl` or `state.json`; all writes go through collaboration scripts.
- Default permission is `artifact_only`.
- Repository writes require explicit user authorization plus isolated worktree or patch artifact.
- Agent capabilities are allowlisted, not free-form.
- Event types are allowlisted per capability.
- A custom agent cannot change protocol files, registry files, or lock behavior unless explicitly granted `governance` capability.
- Every invocation records manifest hash, command id, timeout, exit code, artifact path, and mode.

### 3. Registry Location

Use project-local registry first:

```text
.omc/collaboration/agents.json
```

This is correct for reproducibility and task-local governance. User-global skill configuration can generate or propose registry entries later, but the active runtime registry should live in the repository so collaborators see the same enabled agents.

Optional future split:

- `.omc/collaboration/agents.schema.json`
- `.omc/collaboration/agents.json`
- user-level templates outside the repo only as installation sources, not runtime truth.

### 4. Suggested Registry Schema

Minimum useful fields:

```json
{
  "version": 1,
  "agents": [
    {
      "id": "gemini",
      "display_name": "Gemini",
      "type": "cli",
      "enabled": true,
      "trust_level": "built_in",
      "default_mode": "read_only",
      "allowed_modes": ["read_only"],
      "capabilities": ["large_context_analysis", "document_review"],
      "invoke": {
        "command": ".omc/collaboration/scripts/invoke-gemini-analysis.sh",
        "args": ["--manifest", "{manifest}"],
        "timeout_seconds": 120
      },
      "inputs": {
        "requires_manifest": true,
        "max_files": 200,
        "allow_globs": false
      },
      "outputs": {
        "artifact_required": true,
        "required_sections": ["analysis", "findings", "recommendations", "limitations"]
      },
      "events": {
        "allowed_types": ["analysis_requested", "analysis_completed", "analysis_failed"]
      },
      "write_policy": {
        "repo_write": false,
        "state_write": false,
        "event_write": "via_collaboration_script"
      },
      "healthcheck": {
        "command": "gemini --version",
        "timeout_seconds": 10
      }
    }
  ]
}
```

Important: do not let `invoke_cmd` be arbitrary shell text. Store command plus args as arrays to avoid shell injection and ambiguous quoting.

### 5. Conformance Validation

A custom agent is acceptable only if it passes a canary suite:

- Registry schema validates.
- Healthcheck succeeds or the agent remains disabled.
- Dry-run invocation creates exactly one artifact.
- Dry-run invocation appends exactly one allowed event through the wrapper.
- Journal validation passes after invocation.
- The agent cannot write to repo files outside its declared artifact or worktree path in read-only/artifact-only mode.
- Timeout produces an `analysis_failed` artifact and leaves no residual lock.
- Malformed output produces `validation_failed` or `analysis_failed`, not a silent success.

These checks should run before enabling an agent and after changing its registry entry.

## Critique Of Claude's Proposals

### Gemini proposal

Good:

- Introduces explicit mode and manifest.
- Treats failure as artifact plus event.
- Separates expected output from raw model text.

Weak:

- `omc ask gemini` is a facade without specifying the enforcement layer.
- Required fields are too shallow to evaluate analytical quality.
- It does not define who accepts Gemini recommendations.
- It does not classify API errors or define non-blocking behavior.
- It does not prove read-only behavior.

### Agent registry proposal

Good:

- Project-local registry is the right default.
- `enabled` flag and capabilities are necessary.
- Dynamic routing is useful eventually.

Weak:

- `invoke_cmd` as an unconstrained string is unsafe.
- It does not separate agent identity from protocol authority.
- It lacks trust levels, write policy, event allowlists, output contracts, and healthchecks.
- It does not define a conformance test before enabling custom agents.
- It risks solving extensibility before the built-in three-agent path is stable.

## Verifiable Decision Criteria

Adopt Claude's approach only if it satisfies these tests:

1. A Gemini dry-run works without Gemini CLI installed and still creates artifact plus event.
2. A live Gemini failure creates `analysis_failed` and does not corrupt task status.
3. A Gemini success artifact can be mechanically validated for required metadata, source grounding, and limitations.
4. Journal validation passes after every Gemini path: success, failure, timeout, dry-run.
5. A custom disabled agent cannot be invoked.
6. A custom enabled read-only agent cannot write repo files except declared artifacts.
7. Registry changes fail closed when schema validation fails.
8. Dynamic routing emits an auditable reason: why this agent, why this mode, and what acceptance gate applies.

## Implementation Priority

Recommended sequence:

1. **P0:** Harden current fixed-agent workflow.
   - Add explicit Gemini manifest schema.
   - Fix Gemini event types and status mapping.
   - Add output validator.
   - Add timeout/retry/failure classification.
   - Ensure dry-run does not require Gemini CLI.

2. **P0/P1:** Add conformance tests.
   - Gemini dry-run.
   - Gemini failure path.
   - Journal/state validation after invocation.
   - Artifact shape and grounding checks.

3. **P1:** Add `.omc/collaboration/agents.json` for built-in agents only.
   - Claude, Codex, Gemini.
   - No user-defined agents yet.
   - Registry acts as documentation plus routing metadata.

4. **P2:** Allow user-added agents through a skill.
   - Generate registry entry disabled by default.
   - Run canary validation.
   - Enable only after explicit user approval.

5. **P2/P3:** Add MCP or richer `omc ask gemini` facade.
   - Only after the direct CLI contract is stable.

## Bottom Line

Gemini should become a disciplined read-only evidence producer before it becomes a routed peer. Modular agents should become a controlled adapter system after the built-in three-agent protocol is mechanically enforced. The core invariant is simple: models may produce artifacts; only trusted collaboration scripts update shared workflow state.
