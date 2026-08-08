# Outreach Batch — schema

The portable, agnostic schema for one cold-acquisition push, sized to be lightweight enough to
fill in by hand and structured enough for the Pipeline agent to reconcile. It mirrors the
Outreach Batches database (see rules/04-crm-conventions.md — `<HUB_BATCHES_DB>`). A batch is
the source-of-truth record for one cold push.

| Field | Type | Notes |
|---|---|---|
| Batch Name | title | e.g. "`<FOCUS_NAME>` / cold-email / wave-1" |
| Vertical / Focus | select | MUST match active-focus. Agnostic value, not a column. |
| Objective | text | What this batch must achieve |
| Channel | select | cold-email / cold-linkedin / community / multi-channel / other |
| Conversion Goal | select | operator-defined; whatever "converted" means for your offer (e.g. purchase, signup, booked call, other) |
| Status | select | draft / pending-approval / approved / sending / sent / completed / paused |
| Leads Sourced, Leads Reached, Replies, Signups, Paid Conversions | number | funnel counters (separate fields; set by Pipeline agent) |
| Target ICP (snapshot) | text | frozen copy of brain/icp.md one-liner at launch |
| Message Refs | text | links to Messaging Library assets used |
| Constraints / Guardrails | text | batch-specific do-nots |
| Launch Date | date | |
| Created / Last Updated | created_time / last_edited_time | system-managed |

`Vertical / Focus` is an operator-defined enum: one select option per market you run, plus
`other`. Populate it from active-focus/focus.md — it is never hard-coded here. Example, for
illustration only: `<FOCUS_NAME>`, `other`.

## Lifecycle (draft-first)
draft → pending-approval → [OPERATOR APPROVES] → approved → sending → sent → completed
`paused` is an off-ramp from any active state (operator halts a batch). Nothing past
'approved' runs without operator sign-off (rule 01).
