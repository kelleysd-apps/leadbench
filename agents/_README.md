# agents/ — role-based job descriptions

Each file is a job description, not a prompt. Written against a ROLE, never a niche, so the
same agent works for any focus. Invoke one by saying e.g. "act as the Sourcing agent and work
the current focus." These are also spawnable as subagents with no rewrite.

EVERY agent reads, in order: active-focus/focus.md → the relevant brain/ files → rules/ (all
seven). Then does its job. All output is DRAFT-FIRST (see rules/00-draft-first.md).

Roster:
- cmo.md            — orchestrator: plans a batch, delegates, assembles for approval
- sourcing.md       — finds & lists candidate leads for the current ICP
- qualifier.md      — scores leads against brain/icp.md; sets the Priority field (High/Medium/Low)
- sequencer.md      — drafts the outreach copy/sequence (reach → nurture → convert)
- pipeline.md       — tracks the funnel, reconciles against the app database's truth, reports
