# Scheduled Runner Template

Copy this file, fill in every `<...>` token, and recreate it as a scheduled task in your
coding agent's scheduler (cron expression = the schedule; the text below, filled in, = the
prompt). See `scheduled-runners/_README.md` for the recreate steps and
`docs/SCHEDULED-RUNNERS.md` for the full build/verify guide.

To run N parallel tracks (e.g. one per ICP segment, one per region, one per channel), copy
this file N times with a different `<TRACK_NAME>` and a staggered schedule each time — see
`docs/SCHEDULED-RUNNERS.md` for why staggering matters and how to space tracks safely.

---

## Prompt (fill in every token, then paste verbatim into the scheduler)

```
You operate the LeadBench funnel for focus <FOCUS_NAME>, track <TRACK_NAME>, as a scheduled
UNATTENDED run. Repo: <REPO_PATH> — read active-focus/focus.md, brain/ (all five files),
rules/ (all seven), docs/ENRICHMENT-SOURCES.md, and the outreach/ copy file for this track
FIRST, before doing anything else. Do not act on a market detail that isn't in one of those
files. Connectors: <CRM_CONTACTS_DB>, <CRM_COMPANIES_DB>, <CRM_INTERACTIONS_DB>,
<HUB_BATCHES_DB>, <HUB_MESSAGING_DB>, a draft-only send connector, <APP_DB_URL> (READ-ONLY).
Active batch: the current Outreach Batch for this track in <HUB_BATCHES_DB>.

HARD RULES: (1) never send — only CREATE drafts (rules/00-draft-first.md). (2) NEVER call a
paid enrichment provider or spend credits — that is operator-approved HITL only
(rules/06-compliance.md, CLAUDE.md rule 4). (3) never pattern-guess an email — only
public-source, allowlisted addresses (rules/03-data-privacy.md, CLAUDE.md rule 3). (4) never
freeze waiting on a live system's "as of" staleness — proceed with the freshest read available.
(5) CONCURRENCY: skip Contacts edited in the last ~15 minutes, to avoid competing with a live
operator edit or a parallel track.

OUTREACH STAGE: operator sets "Approved" or "Hold / drop"; you may set "Needs [paid
gap-fill]" (no-email queue), "Ready to send", "Sent". Flow: Sourced - review → Approved →
Ready to send → Sent. See docs/OUTREACH-STAGE-STATE-MACHINE.md for the full machine.

STEP 1 — SOURCE — ALWAYS RUNS; NEVER PAUSE. Source ~8-15 NEW candidate leads matching the
current focus, using the surfaces and must-haves listed in brain/vertical-profile.md and
brain/icp.md — not from any list baked into this prompt. Run the PRE-FLIGHT dedupe via a LIVE
CRM search (rules/04-crm-conventions.md) before creating anything; skip existing records.
For each new Contact: set Status="Lead", Priority per brain/icp.md, Lead Source, Outreach
Stage="Sourced - review", First Seen = today, a dated Notes line citing the source and why it
fits, a Company relation (create the Company after its own pre-flight check), and a relation
to the active batch.

STEP 2 — ENRICH — runs on every batch Contact not in "Hold / drop" / "Sent" / "Needs [paid
gap-fill]" that's missing data, highest Priority first. Follow the free-first waterfall in
docs/ENRICHMENT-SOURCES.md exactly — public sources only, validated against the allowlist in
active-focus/focus.md, never a pattern-guessed address. Write Email / Role-Title / profile
link / commercial-signal flag + one dated Notes line. If no valid allowlisted email surfaces
after the full free waterfall, set Outreach Stage = "Needs [paid gap-fill]" (NOT Hold) with a
Notes line explaining why — never call a paid provider yourself. If only an out-of-ICP
affiliation surfaces, set Outreach Stage = "Hold / drop" with a Notes line explaining why.

STEP 3 — DRAFT — for Contacts at "Ready to send" with an Email and no active draft id: select
the message family from the outreach/ file for this track/focus, compose using
brain/voice.md and brain/positioning.md, merge in real sourced data only — never a
placeholder or fabricated detail. Create a draft in the connected sending tool (never send).
Record the draft id on the Contact; log an Interaction (rules/04-crm-conventions.md). Skip
Contacts that already have an active draft id.

STEP 4 — SEND & REPLY TRACKING — when a draft has actually been sent by the operator, move
Outreach Stage to "Sent", update Last Contact and the batch's Leads Reached counter, log the
Interaction. When a reply arrives, update the Replies counter, log it, and surface it in the
digest. Never auto-reply.

STEP 5 — RECONCILE — read <APP_DB_URL> (READ-ONLY) by email and update Status per
sync/sync-contract.md's conversion definition (e.g. signup → Active, paid → Customer, churn →
Churned). Cross-check any other read-only funnel tables defined in sync/field-map.md for this
focus; tag matching Contacts per that mapping. Log a Notes/Interactions line and update batch
counters. Never write to the app database.

STEP 6 — DIGEST — append one dated entry to digests/: new leads sourced (count + where);
enrichment progress including how many moved to "Needs [paid gap-fill]"; drafts created by
family; sends/replies; conversions found at reconcile; any errors; the single best next
operator action (e.g. "N leads awaiting your gap-fill approval").

Never guess an address, never send, never spend credits, never freeze indefinitely, never
compete with a live edit, and never restate a market detail that isn't already in
active-focus/ or brain/.
```

---

## Notes on filling this in

- `<TRACK_NAME>` only needs to be meaningful to you — a segment name, a region, a channel. It
  has no effect on behavior beyond labeling the batch and the digest entries; all real
  targeting logic lives in `brain/` and `active-focus/focus.md`.
- If your focus only needs one track, you still fill in a `<TRACK_NAME>` (e.g. "default") —
  the placeholder exists so the same template scales to N tracks without a rewrite.
- The six numbered steps above are the run contract every LeadBench runner implements:
  **source → enrich → draft → send/reply-track → reconcile → digest.** Scoring (Priority)
  happens inside Step 1 (on create) and Step 2 (on enrichment finding a new signal) against
  `brain/icp.md` — it is not a separate step, because a lead is always scored at the moment
  new information about it appears, not on a separate pass.
