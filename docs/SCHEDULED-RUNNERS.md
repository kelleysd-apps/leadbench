# Scheduled Runners — build, schedule, rebuild, verify

A scheduled runner is an unattended, timed re-run of the same cold-outbound loop the operator
runs by hand in `docs/OPERATOR-RUNBOOK.md` — source, enrich, draft, track, reconcile, digest —
on a cron schedule instead of on request. This doc covers how to build one, how to run more
than one in parallel safely, and how to verify one is actually working.

This doc defines the run contract every runner implements — what it does, not the platform
mechanics of scheduling it. For the actual "where do I click to schedule this" steps, and the
concrete difference between a local scheduled task and a Claude Cowork scheduled task, see
[`docs/RUNNING.md`](RUNNING.md).

The portable copy of every runner you've built lives in `scheduled-runners/`; that folder is
the record, not the runtime — see `scheduled-runners/_README.md` for why the split exists and
the state model that makes rebuilding one lossless.

## The six-step run contract

Every runner, regardless of focus or track, implements the same six steps, always in this
order, reading `active-focus/` and `brain/` fresh at the start of each run rather than caching
anything about the market:

1. **Source** — top up the batch with new candidate leads matching the current focus. Always
   runs, never pauses for a quiet enrichment queue. Pre-flight dedupe against the live CRM
   before every create (`rules/04-crm-conventions.md`). Priority is scored here, against
   `brain/icp.md`, at creation time — not as a separate pass.
2. **Enrich** — run the free-first waterfall (`docs/ENRICHMENT-SOURCES.md`) against every
   batch Contact missing data, highest Priority first. No operator gate on the free waterfall
   itself; a paid provider is never called from inside a runner.
3. **Draft** — compose outreach for Contacts that are `Ready to send` with a verified email
   and no active draft. Uses `brain/voice.md` and the relevant `outreach/` file. Creates a
   draft only — never sends.
4. **Send & reply tracking** — once the operator has actually sent a drafted message (outside
   the runner), the next run detects it, advances the record, and tracks any reply.
5. **Reconcile** — read the app database (read-only) and update Status per the conversion
   definition in `sync/sync-contract.md`.
6. **Digest** — append one dated entry to `digests/` summarizing what the run did, what needs
   operator attention, and any errors.

`scheduled-runners/TEMPLATE/SKILL.md` implements this contract with every market detail
replaced by a read from `active-focus/` and `brain/` — see that file for the exact prompt.

## Connectors a runner needs

Generic list; substitute your own tools per `SETUP.md`:

- The shared CRM's Contacts, Companies, and Interactions collections
  (`<CRM_CONTACTS_DB>`, `<CRM_COMPANIES_DB>`, `<CRM_INTERACTIONS_DB>`).
- The LeadBench hub's Outreach Batches and Messaging Library (`<HUB_BATCHES_DB>`,
  `<HUB_MESSAGING_DB>`).
- A draft-only sending connector (create drafts; never send).
- The app database, connected **read-only** (`<APP_DB_URL>`) — see
  `rules/04-crm-conventions.md` on enforcing this at the credential, not just by convention.
- This repo, connected at a stable, absolute path (`<REPO_PATH>`).

A runner should never have a paid-enrichment-provider connector wired to auto-approve spend,
and should never have write access to the app database, under any configuration.

## Building a runner

1. Copy `scheduled-runners/TEMPLATE/SKILL.md`.
2. Fill in every `<...>` token — repo path, focus name, track name, CRM/DB identifiers.
3. Create the scheduled task in your coding agent's scheduler with a cron expression and the
   filled-in prompt, verbatim. See [`docs/RUNNING.md`](RUNNING.md) for the concrete steps in
   Claude Code's local scheduled tasks and in Claude Cowork's scheduled tasks — including the
   real difference in file access between the two.
4. Save the filled-in copy back into `scheduled-runners/<track-name>/SKILL.md` in this repo —
   that's what makes it recoverable later.

## Running N tracks in parallel — and staggering them

If you split one focus into multiple parallel tracks (by segment, region, or channel), give
each its own copy of the template with a distinct `<TRACK_NAME>`, and **stagger their
schedules** — never start two tracks at the same wall-clock time, even a minute apart.

This isn't a theoretical concern. Running tracks concurrently against the same CRM records
without staggering is exactly how two runners end up racing to enrich or draft the same
Contact at once, each unaware of the other's in-flight edit — the "skip Contacts edited in
the last ~15 minutes" rule in every runner prompt only protects you if the runs are actually
spaced further apart than that. A safe default: space each track's start time by at least
60–90 minutes, and keep the total number of concurrently-scheduled tracks small enough that
the last one in the day still starts well clear of the first one's finish.

## Rebuilding a runner (after moving the repo, or losing scheduler state)

1. Open the saved copy in `scheduled-runners/<track-name>/SKILL.md`.
2. Update `<REPO_PATH>` if the repo moved.
3. Recreate the scheduled task with the same cron expression and the (possibly path-updated)
   prompt, verbatim.
4. Verify per the next section before trusting it.
5. If you're moving off an old scheduler entirely, delete the originals there once the new
   ones are confirmed working, so nothing double-runs.

Because runners hold no local state (see `scheduled-runners/_README.md`), recreating one
against the same CRM records and repo simply resumes — there's nothing to reconcile.

## Verifying a runner is working

- List your scheduler's tasks and confirm the runner is present, enabled, and has the
  schedule you expect.
- Trigger one run by hand and confirm: it only drafts, never sends; it appends a digest entry
  to `digests/`; new or enriched Contacts show a Notes line dated today.
- After a live scheduled run, check `digests/` for that day's entry and skim it for errors or
  a stalled step.
- If leads stop appearing, check first for a stale `<REPO_PATH>` (the most common failure
  after moving a repo) before assuming a source dried up.
