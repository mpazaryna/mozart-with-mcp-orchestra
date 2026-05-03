# Mozart + mcp-orchestra: Proof of Concept

Two tools that cover the full software delivery loop. **mcp-orchestra** owns deterministic planning (PRD → Spec → Gherkin). **Mozart** owns execution (research → implement → verify → ship). Together they remove the two biggest failure modes in AI-driven development: the model skipping planning steps and the model losing track of a multi-agent execution.

---

## The problem each tool solves

### mcp-orchestra — probabilistic planning fails at scale

Encoding a multi-phase developer playbook as AI skills produces a probabilistic system. Steps that must always fire don't. Gates that must block don't. The model interprets instructions and gets it wrong often enough to cause real pain at scale.

mcp-orchestra moves the planning pipeline into code. Python owns the state machine, enforces the gates, and writes the files. The model is called only to generate content — a PRD draft, a spec derivation, a set of Gherkin scenarios. The model cannot skip a step, forget to write a file, or advance without approval. Python either runs the function or it doesn't.

### Mozart — complex execution needs a conductor

A single Claude Code session cannot run multiple specialist agents in parallel, enforce review gates, or maintain a coherent plan across phases. Mozart acts as a senior delivery conductor: it reads approved artifacts, spawns the right specialists at the right time, tracks state across phases, and surfaces conflicts rather than silently resolving them.

---

## How the two tools integrate

```
mcp-orchestra                       Mozart
──────────────────────────────      ──────────────────────────────────────
Roadmap draft / revise / approve    ←─ reads approved roadmap (HEAVY tier)
PRD draft / revise / approve        ←─ reads approved PRD
Spec draft / revise / approve       ←─ reads approved spec; skips harry if present
Gherkin draft / revise / approve    ←─ reads scenarios as acceptance criteria
                                    →─ research → plan → review → implement → verify → ship
```

Mozart detects existing approved artifacts from mcp-orchestra and skips re-drafting. The tier classification determines when the full planning pipeline is warranted:

| Tier | Planning | When |
|------|----------|------|
| TINY | Harry improvises — no orchestra | Small, well-scoped changes |
| STANDARD | Mozart reads approved orchestra spec | Most feature work |
| HEAVY | Full orchestra pipeline first, then Mozart executes | Large or high-risk work |

---

## Installation

### Mozart (Claude Code plugin)

Mozart is installed as a Claude Code plugin from the local marketplace:

```bash
# The marketplace is already registered; install with:
claude plugin install mozart-orchestration
```

Invoke via the `/mozart` slash command at the top level of a Claude Code session. Mozart must run at the top level (not inside a Task subagent) because its job is to spawn subagents via the `Task` tool — which is only available at the session root.

### mcp-orchestra (Python MCP server)

**Requirements:** Python 3.12+, [uv](https://docs.astral.sh/uv/), an Anthropic API key.

```bash
git clone https://github.com/mpazaryna/mcp-orchestra.git
cd mcp-orchestra
uv sync
```

Create `.env` in the mcp-orchestra root:

```
ANTHROPIC_API_KEY=sk-ant-...
```

This project's `.mcp.json` already connects mcp-orchestra to Claude Code:

```json
{
  "mcpServers": {
    "orchestra": {
      "command": "uv",
      "args": ["run", "--directory", "/Users/mpaz/workspace/mcp-orchestra", "mcp-orchestra"],
      "env": {
        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}"
      }
    }
  }
}
```

---

## mcp-orchestra reference

Eight MCP tools exposed by the server:

| Tool | Description |
|------|-------------|
| `orchestra_scaffold` | Create `.orchestra/` folder structure and README Brief template |
| `orchestra_roadmap_draft` | Generate roadmap draft from README Brief |
| `orchestra_roadmap_revise` | Revise current roadmap draft with feedback |
| `orchestra_roadmap_approve` | Write `roadmap.md` and milestone stub PRDs |
| `orchestra_plan_draft` | Draft PRD, spec, or Gherkin for a work item |
| `orchestra_plan_revise` | Revise current stage draft with feedback |
| `orchestra_plan_approve` | Write approved artifact, advance pipeline state |
| `orchestra_status` | Return current pipeline state for a work item |

### Gate enforcement

The planning pipeline enforces hard gates — each stage blocks until the previous is approved:

```
Roadmap approved → PRD drafting unlocked
PRD approved     → Spec drafting unlocked
Spec approved    → Gherkin drafting unlocked
```

State is persisted in `pipeline.json` per work item inside `.orchestra/`. Sessions, crashes, and context resets cannot bypass a gate.

### Project layout (mcp-orchestra)

```
mcp_orchestra/
├── server.py          MCP entry point — 8 registered tools
├── client.py          Anthropic API wrapper (injectable for testing)
├── state.py           Pipeline state machine (pipeline.json)
├── errors.py          GateError, DraftNotFoundError
├── prompts/           Content generation rules per stage
│   ├── prd.md
│   ├── spec.md
│   ├── gherkin.md
│   ├── roadmap.md
│   └── review.md
└── tools/
    ├── scaffold.py
    ├── roadmap.py
    ├── plan.py
    └── status.py
```

---

## Mozart reference

### Invoke

```
/mozart <your request>
```

Examples:

```
/mozart add SSO via Authentik for the admin panel
/mozart investigate why pgvector queries are slow on staging
/mozart audit the codebase for tech debt
/mozart have xander review my auth middleware
/mozart resume thoughts/shared/plans/<slug>.state.md
/mozart drive these 3 tickets in parallel: <list>
```

### Agent roster

| Agent | Role |
|-------|------|
| mozart | Conductor — orchestrates the pipeline |
| harry | Planning architect — drafts the plan |
| sarah | Researcher — prior art and best practices |
| bob | Architectural plan reviewer |
| dexter | Code-health auditor |
| xander | Security reviewer (adversarial) |
| ruby | UI/UX designer and frontend reviewer |
| otto | Infra / k8s / ops reviewer |
| ian | Change-impact analyst |
| jackson | Senior software engineer (implementer) |
| valerie | Plan-vs-reality validator |
| scott | Technical writer |
| dick | Investigator (DIAGNOSE pipeline) |
| librarian | Knowledge base curator |

### DELIVER pipeline (13 stages)

```
1.  Intake          — classify tier, mode, shape; create state file + flow sketch
2.  Research        — sarah surveys prior art (skipped on TINY)
3.  Plan            — harry drafts thoughts/shared/plans/<slug>.md
4.  Internal review — bob (always) + xander/dexter/ruby/otto (conditional, parallel)
5.  Codex on plan   — external architect review (skipped on TINY)
6.  Iterate         — harry revises; capped 3 rounds
7.  Implement       — jackson, phase by phase
8.  Mid-build gate  — per-phase specialist review before commit
9.  Codex on diff   — external review of final diff (mandatory on HEAVY)
10. Validate        — valerie checks plan vs. reality
11. Reconcile       — jackson fixes + valerie re-checks; capped 3 rounds
12. Documentation   — scott updates README, CHANGELOG, wiki
13. Report          — mozart final summary
```

### Work shapes

| Shape | Use for |
|-------|---------|
| DELIVER | Build / change / ship |
| AUDIT | Review against a goal (can hand off to DELIVER for remediation) |
| DIAGNOSE | Investigate a specific failure |

### Operating modes

| Mode | Behavior |
|------|----------|
| AUTONOMOUS (default) | Mozart runs end-to-end without pausing |
| LOOP-IN | Per-phase user gate with explicit test instructions |

### Artifacts

| Artifact | Path |
|----------|------|
| Plan | `thoughts/shared/plans/<slug>.md` |
| State file | `thoughts/shared/plans/<slug>.state.md` |
| Flow sketch | `thoughts/shared/plans/<slug>.flow.md` |
| Research brief | `thoughts/shared/research/<slug>.md` |
| Audit report | `thoughts/shared/audits/<slug>.md` |

State files persist across sessions. If a run crashes or the session resets, `/mozart` at intake will offer to resume any in-progress campaigns.

---

## Typical workflow

**For STANDARD or HEAVY work:**

1. Run `orchestra_scaffold` to create `.orchestra/` in the target project.
2. Use `orchestra_roadmap_draft` → `revise` → `approve` to lock the roadmap.
3. Use `orchestra_plan_draft` → `revise` → `approve` to produce a PRD, then a spec, then Gherkin scenarios.
4. Invoke `/mozart <task>` — Mozart reads the approved spec, skips re-planning, and goes straight to implementation.

**For TINY work:**

Skip mcp-orchestra entirely. Invoke `/mozart <task>` — harry improvises a lightweight plan inline.

**For review or investigation only:**

Invoke `/mozart` with a passthrough phrase and Mozart routes directly to the relevant specialist without creating a plan or state file:
- `"have xander review my auth middleware"` → routes to xander
- `"investigate why queries are slow"` → routes to dick (DIAGNOSE)
- `"audit the codebase for tech debt"` → routes to dexter and bob (AUDIT)

---

## Running mcp-orchestra tests

```bash
cd /Users/mpaz/workspace/mcp-orchestra
uv run pytest              # all tests (no model required)
uv run pytest -m evals     # eval suite (real model, slow)
```

Unit tests mock the Anthropic API. Gate enforcement, file I/O, and state management are fully testable without network access.

## Usage

### currency-converter CLI

The currency converter is the proof-of-concept application built by the mcp-orchestra + Mozart pipeline. It converts a monetary amount between supported currencies and prints the result to stdout.

**Requirements:** Python 3.12+

**Install:**

```bash
pip install -e ".[dev]"
```

**Command:**

```bash
currency-converter <amount> <from_currency> <to_currency>
```

**Examples:**

```bash
currency-converter 100 USD EUR
# 92.00 EUR

currency-converter 50 EUR GBP
# 43.00 GBP

currency-converter 200 USD GBP
# 158.00 GBP
```

**Supported currencies:**

| Code | Currency |
|------|----------|
| USD  | US Dollar |
| EUR  | Euro |
| GBP  | British Pound |

**Exchange rates (static):**

| Pair | Rate |
|------|------|
| USD → EUR | 0.92 |
| EUR → GBP | 0.86 |
| USD → GBP | 0.79 |

**Error handling:**

- Unknown currency code: prints a clear error message and exits non-zero
- Non-numeric amount: prints a clear error message and exits non-zero

**Run the test suite:**

```bash
pip install -e ".[dev]"
pytest
```

82 tests across unit, integration, and e2e layers. All tests were written before the production code they cover.

---

## Brief

**Vision:** A currency converter CLI in Python, built strictly TDD, as a complete end-to-end run of the mcp-orchestra + Mozart pipeline — proving gate enforcement, Gherkin-to-test traceability, and clean handoff from planning to execution.
**Audience:** Developers evaluating the mcp-orchestra + Mozart workflow.
