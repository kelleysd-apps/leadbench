# Operator Runbook — running LeadBench day to day

This is the doc you use after `SETUP.md`. Setup happens once per focus; this runbook is what
you do every time you run a batch, and every week after that.

## One-time setup per focus

1. Open `active-focus/focus.md`. Set target vertical, ICP one-liner, offer, conversion goal,
   channels.
2. Fill the `brain/` templates for this focus (or paste a strategy doc and ask the agent to
   draft fills for you to review).
   - Highest leverage: `brain/voice.md` and `brain/positioning.md` — get those two right
     first, everything downstream depends on them most.
3. Confirm the LeadBench hub is connected (Outreach Batches, Messaging Library).
4. Confirm the shared CRM is connected. LeadBench agents read and write Contact records
   there — see `rules/04-crm-conventions.md`.
5. If you have a product with a conversion event to track, confirm the app database is
   connected read-only, and that `sync/sync-contract.md` defines the conversion event.

## Running a cold batch (the core loop)

With the CRM and (optionally) the app database connectors on:

1. **Plan** — "Act as the orchestrator agent. Plan a cold batch for the current focus aiming
   for ~20 qualified leads into reach." → the orchestrator confirms the focus, drafts the
   batch plan.
2. **Source** — "Run the Sourcing agent." → adds candidate Contacts to the shared CRM with
   Status = "Lead", relates them to the new Outreach Batch. Pre-flight dedupe search runs
   before every create — see `rules/04-crm-conventions.md`.
3. **Qualify** — "Run the Qualifier agent." → sets Priority on each Contact against
   `brain/icp.md`; appends rationale to Notes.
4. **Draft copy** — "Run the Sequencer agent." → drafts reach + follow-ups + convert CTA into
   the Messaging Library as drafts. Nothing is sent at this step.
5. **Approve** — review the approval packet. Nothing sends until you say so, explicitly, in
   chat, at the time. See `rules/00-draft-first.md` and `rules/01-approval-gates.md`.
   - Includes a check that no Contact's Notes contains a hold flag (e.g.
     "review-before-contact") unless you've explicitly cleared it.
   - Includes a compliance check against `rules/06-compliance.md` — sender identification,
     working opt-out, suppression-list check, no deceptive subject lines.
6. **Send** — only after approval, and only via a channel/tool you've connected. On send: log
   an Interaction on each Contact; move Status from "Lead" toward "Active".
7. **Track** — "Run the Pipeline agent." → reconciles shared CRM Contacts against the app
   database's truth, updates Outreach Batch counters, reports conversions and the one thing
   to change next batch.

## Weekly

- Run the Pipeline agent for a funnel snapshot.
- Review Contacts held at a "review-before-contact" or equivalent flag — these are
  carry-forward contacts from prior work; clear or recontextualize before reaching out.
- Skim `digests/` if scheduled runners are active (see `docs/SCHEDULED-RUNNERS.md`) — each
  unattended run appends one dated digest.

## Switching focus

- Archive `active-focus/focus.md` and the `brain/` fills to `active-focus/archive/<focus>/`.
- Write new ones. Agents, rules, schemas, shared CRM, sync contract — all unchanged.

## Guardrails you can rely on

- Draft-first everywhere (`rules/00-draft-first.md`). Approval gates
  (`rules/01-approval-gates.md`).
- The app database is read-only. The CRM never gets funnel truth overwritten by LeadBench.
- The shared CRM is shared: agents append to Notes, never overwrite. Other functions write
  there too.
- No fabricated leads, quotes, prices, or personalization — see `CLAUDE.md`'s reporting rule.
- Compliance basics (suppression, CAN-SPAM/GDPR footer requirements, platform ToS) are always
  in force — `rules/06-compliance.md` — regardless of what any single batch plan says.

## One-time hub setup

Before the first run, confirm the relation fields between the hub's Outreach Batches database
and the shared CRM are wired as **dual relations** in both directions: Outreach Batches ↔
Contacts, and Outreach Batches ↔ Companies. Most collaborative-database platforms need this
done once, by hand, in the UI — API/MCP-driven schema changes often can't create a dual
relation cleanly. Do this once per workspace, not once per focus.
