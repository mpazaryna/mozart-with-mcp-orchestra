# mozart-with-mcp-orchestra Roadmap

**Objective:** A currency converter CLI in Python, built strictly TDD, as a complete end-to-end run of the mcp-orchestra + Mozart pipeline — proving gate enforcement, Gherkin-to-test traceability, and clean handoff from planning to execution.

## Success Criteria

- [x] Currency converter CLI works end-to-end from the command line
- [x] Every production line is covered by a test written before the implementation
- [x] Gherkin scenarios trace directly to passing tests
- [x] mcp-orchestra gates were enforced (PRD → Spec → Gherkin) before Mozart executed

## Context

This is a dogfood project. The currency converter is the vehicle; the real proof is the pipeline. If mcp-orchestra enforces the gates and Mozart executes cleanly against the approved spec, the workflow is validated for real projects.

## Milestones

| Material | Location | Status |
|----------|----------|--------|
| Core Converter | .orchestra/work/core-converter/prd.md | Done |

## References

- ADR-000: [The Score](.orchestra/adr/ADR-000-the-score.md)
