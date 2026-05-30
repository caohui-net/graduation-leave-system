# Claude Analysis: GitHub Projects Review

**Task:** TASK-20260530-03  
**Agent:** Claude  
**Date:** 2026-05-30  
**Projects Analyzed:** 4

---

## Executive Summary

Analyzed 4 Claude-Codex collaboration projects. Key findings:

1. **shakacode/claude-code-with-codex** - Shared instruction file pattern (AGENTS.md)
2. **smart-lty/Claude-Team** - MCP-based orchestration with 3 agents
3. **Z-M-Huang/vcp dev-buddy** - Ralph loop with disk-backed state
4. **doccker/cc-use-exp** - Layered config system with skills

**Relevance to our mechanism:** Medium-High. Several patterns applicable.

---

## Project 1: shakacode - Shared Instructions Pattern

### Key Patterns

**Single Source of Truth:**
- `AGENTS.md` as shared instruction file
- Codex reads automatically, Claude references via `CLAUDE.md`
- Discovery hierarchy: Home → Project → Current (with `.override.md` priority)

**Workflow Patterns:**
1. Sequential handoff (implement → review)
2. Cross-validation (git worktrees, parallel branches)
3. Spec-first development (one writes tests, other implements)

**State Management:**
- No shared runtime state
- Coordination via: shared files + git branches + filesystem
- Isolation via git worktrees for parallel work

### Relevance to Our Mechanism

**Already implemented:**
- ✅ Shared instruction files (AGENTS.md, CLAUDE.md)
- ✅ Sequential handoff pattern
- ✅ Filesystem-based coordination

**Could integrate:**
- ⚠️ Git worktree isolation for parallel tasks
- ⚠️ Cross-validation workflow (both analyze same problem)
- ⚠️ Spec-first pattern (one writes acceptance criteria, other implements)

**Best practices:**
- Keep AGENTS.md under 150 lines (ours: protocol.md is 212 lines - acceptable)
- Wrap commands in backticks (we do this)
- Switch tools when stuck (our handoff mechanism supports this)

---

## Project 2: Claude-Team - MCP Orchestration

### Key Patterns

**Three-Agent Architecture:**
- Claude: Orchestrator + deep understanding
- Codex: Code specialist
- Gemini: Long-context specialist

**Single Entry Point:**
- User interacts only with Claude
- Claude auto-routes to Codex/Gemini based on task
- Transparent delegation (user doesn't manually switch)

**MCP Integration:**
- `codexmcp` server - Claude → Codex bridge
- `gemini-mcp-tool` - Claude → Gemini bridge
- Automatic task distribution based on characteristics

### Relevance to Our Mechanism

**Comparison:**
- Their approach: Automatic routing via MCP
- Our approach: Manual handoff via filesystem state

**Could integrate:**
- ✅ **Gemini integration** - Add GEMINI.md + extend protocol
- ⚠️ MCP-based invocation (requires MCP server development)
- ⚠️ Automatic routing logic (adds complexity, may not fit MVP)

**Key insight:**
- Their model: Single conversation, transparent delegation
- Our model: Explicit handoff, visible collaboration
- Both valid - depends on use case

**Gemini integration path:**
1. Create `GEMINI.md` with collaboration rules
2. Extend protocol.md to support 3-way state
3. Add Gemini as valid agent in event log
4. Test with simple task

---

## Project 3: vcp dev-buddy - Ralph Loop Pattern

### Key Patterns

**Disk-Backed State:**
- State survives context compaction + process restarts
- Immutable plan files (`.md`) + mutable state (`.json`)
- Auto-archives after 7 days

**Multi-AI Adversarial Validation:**
- Different model families review each other
- Catches "same-family training biases"
- Parallel execution for discovery/requirements/review

**10-Layer Enforcement Stack:**
1. Unit plan contracts
2. Plan-lint (pre-validation)
3. Mechanical backpressure (compile/type/lint)
4. Semantic review
5. Orchestrator verification
6. Code review
7. UAT (Playwright)
8. User checkpoints
9. Task management
10. Disk-backed state

**Pipeline Stages:**
- Fixed 6-stage: Discovery → Requirements → Decomposition → Build → Code Review → UAT
- Nested loops: BUILD ↔ CODE REVIEW (inner), UAT → BUILD (outer)

### Relevance to Our Mechanism

**Already implemented:**
- ✅ Disk-backed state (events.jsonl + state.json)
- ✅ Immutable artifacts + mutable state pattern
- ✅ Task lifecycle management

**Could integrate:**
- ✅ **Auto-archive old tasks** (7-day expiry)
- ✅ **Plan-lint stage** (validate before execution)
- ⚠️ Multi-AI adversarial validation (requires 3+ agents)
- ⚠️ Mechanical backpressure (compile/test validation)
- ⚠️ Nested loop pattern (retry logic)

**Key insight:**
- Ralph focuses on **correctness enforcement** (10 layers)
- Our mechanism focuses on **coordination** (handoff + state)
- Complementary - could add validation layers to our protocol

**Immediate integration:**
- Add `expires_at` field to task documents
- Add cleanup script to archive old tasks
- Add pre-execution validation step

---

## Project 4: cc-use-exp - Layered Config System

### Key Patterns

**Three-Tier Activation:**
1. Zero-effort (Rules): Auto-loaded safety checks
2. Low-effort (Skills): Context-triggered by file/language
3. Medium-effort (Commands): Explicit `/command` invocation

**Cross-Platform Sync:**
- Unified skill definitions
- Platform-specific adapters (.claude/, .codex/, .gemini/, .cursor/)
- Sync scripts for distribution

**Safety Skills:**
- `api-contract-safety`, `redis-safety`, `query-performance-safety`
- `time-zone-safety`, `async-task-pattern`
- Auto-activate when relevant files accessed

**Installation Patterns:**
- Plugin marketplace (one-click)
- Full sync (requires marketplace first)
- Incremental deployment (preserves local state)

### Relevance to Our Mechanism

**Already implemented:**
- ✅ Skill-based encapsulation
- ✅ Auto-loading via AGENTS.md/CLAUDE.md

**Could integrate:**
- ✅ **Cross-platform sync** - Make skill work with Codex + Gemini
- ✅ **Safety skills pattern** - Add validation skills to protocol
- ⚠️ Three-tier activation (our skill is medium-effort only)
- ⚠️ Plugin marketplace distribution (requires OMC PR)

**Key insight:**
- They focus on **reusable workflows** across projects
- Our mechanism is **project-specific** collaboration
- Could make our skill distributable via sync scripts

**Immediate integration:**
- Create `.codex/` and `.gemini/` versions of skill
- Add sync script to distribute across platforms
- Add safety validation skills (protocol-lint, state-validate)

---

## Synthesis: What to Integrate

### Priority 1: Gemini Integration (User Requested)

**Rationale:** User confirmed Gemini CLI available and wants integration.

**Implementation:**
1. Create `GEMINI.md` with collaboration rules (copy AGENTS.md pattern)
2. Extend protocol.md to support 3-way collaboration
3. Update state.json schema to track 3 agents
4. Add Gemini to valid agent list in scripts
5. Test with simple 3-way task

**Effort:** Low (2-3 hours)  
**Value:** High (enables 3-agent collaboration)

### Priority 2: Cross-Platform Skill Distribution

**Rationale:** Make skill work with Codex + Gemini, not just Claude.

**Implementation:**
1. Create `.codex/skills/claude-codex-collab/` version
2. Create `.gemini/skills/claude-codex-collab/` version (if Gemini supports skills)
3. Add sync script to distribute updates
4. Update documentation for multi-platform usage

**Effort:** Medium (4-6 hours)  
**Value:** High (makes skill truly cross-platform)

### Priority 3: Task Auto-Archive

**Rationale:** Prevent state bloat, borrowed from Ralph pattern.

**Implementation:**
1. Add `expires_at` field to task YAML front matter
2. Add cleanup script to archive tasks older than 7 days
3. Add `/claude-codex-collab cleanup` command
4. Update protocol.md with archival rules

**Effort:** Low (1-2 hours)  
**Value:** Medium (maintenance hygiene)

### Priority 4: Pre-Execution Validation (Plan-Lint)

**Rationale:** Catch issues before consuming collaboration cycles.

**Implementation:**
1. Add validation step before task claim
2. Check: task file exists, well-formed YAML, acceptance criteria present
3. Reject malformed tasks early
4. Add to protocol.md as mandatory step

**Effort:** Low (1-2 hours)  
**Value:** Medium (prevents wasted cycles)

### Priority 5: Adversarial Validation Pattern

**Rationale:** Different agents review each other's work.

**Implementation:**
1. Add review stage to protocol
2. Require different agent to review completed work
3. Add review checklist to protocol
4. Track review events in event log

**Effort:** Medium (3-4 hours)  
**Value:** High (improves quality)

### Not Recommended

**MCP-based auto-routing:**
- Requires MCP server development
- Changes collaboration model from explicit to implicit
- High complexity, unclear value for our use case

**10-layer enforcement stack:**
- Overkill for collaboration coordination
- Better suited for code generation pipelines
- Could add selectively (e.g., mechanical backpressure for code tasks)

**Plugin marketplace distribution:**
- Requires OMC PR and approval
- Premature - should validate mechanism first
- Can do later if mechanism proves valuable

---

## Recommendations for Codex Review

**Questions for Codex:**

1. **Gemini integration approach** - Do you agree with Priority 1 plan? Any concerns about 3-way state management?

2. **Cross-platform distribution** - Is the sync script approach viable? Should we use symlinks instead?

3. **Validation patterns** - Which validation layers from Ralph are most valuable for our use case?

4. **MCP consideration** - Do you see value in MCP-based invocation vs. filesystem handoff?

5. **Protocol extensions** - What changes to protocol.md are needed for Priorities 1-5?

**Areas needing your expertise:**

- Codex CLI skill system (does it support our pattern?)
- Gemini CLI capabilities (what can it do in collaboration?)
- State machine extensions for 3-way collaboration
- Validation script implementation (plan-lint logic)

---

## Next Steps

1. **Await Codex analysis** - Your perspective on these 4 projects
2. **Discuss priorities** - Reach consensus on what to integrate
3. **Plan implementation** - Break down agreed priorities into tasks
4. **Execute** - Implement highest-priority items first
5. **Validate** - Test with real collaboration scenarios

**Estimated total effort for P1-P5:** 12-18 hours  
**Highest ROI:** Gemini integration + Cross-platform distribution
