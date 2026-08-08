# docs/ — index

Architecture and operating docs for LeadBench. Read `CLAUDE.md` and `SETUP.md` first if you
haven't; those two, plus this folder, are the full operator-facing documentation set.

- **`ARCHITECTURE.md`** — the three-layer data architecture (shared CRM / LeadBench hub / the
  read-only app database), why that boundary is load-bearing, the agent roles, the rules
  layer, and the "niche is data, not architecture" principle in full. Read this to understand
  *why* the system is shaped the way it is.
- **`RUNNING.md`** — the three ways to execute LeadBench: interactive in Claude Code, a local
  scheduled task in Claude Code, or a Claude Cowork scheduled task. What each one is, when to
  choose it, concrete setup steps, real limitations, and how the draft-first gate holds up in
  each. Read this after `SETUP.md` if you're past the dry run and deciding how to run this on
  an ongoing basis.
- **`OPERATOR-RUNBOOK.md`** — how to run a batch end to end, day to day, and weekly. The doc
  you use after `SETUP.md`, once the focus and brain are filled and connectors are live.
- **`SCHEDULED-RUNNERS.md`** — how to build, schedule, rebuild, and verify unattended scheduled
  runners; the six-step run contract every runner implements; the connector list; the
  staggering guidance for running more than one track in parallel. Pairs with the portable
  runner definitions in `scheduled-runners/`.
- **`ENRICHMENT-SOURCES.md`** — the free-first lead-enrichment waterfall as a pattern, with a
  paid provider hard-gated behind explicit operator approval. Points you at
  `brain/vertical-profile.md` to list your own vertical's actual sources.
- **`OUTREACH-STAGE-STATE-MACHINE.md`** — the stage state machine that drives a single
  Contact through the funnel, and how it relates to the CRM's own lifecycle `Status` field
  and the Qualifier's `Priority` field.

## What's intentionally not here

This folder ships only the docs listed above. Internal planning notes and anything dense with
environment-specific identifiers are not part of the public template — see `CLAUDE.md` for the
boundary between what LeadBench documents publicly and what stays operator-private per
deployment.
