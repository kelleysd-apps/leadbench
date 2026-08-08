# scheduled-runners/ — portable copies of unattended run definitions

These files are **not code the agent executes from this folder.** They are portable copies
of the scheduled-task definitions (cron schedule + prompt) that live on the operating
machine, outside this repo, in whatever scheduler your AI coding agent uses to run
unattended tasks. This folder is **the record, not the runtime** — it's how you version,
review, and rebuild a runner without depending on the scheduler's own storage.

## Why this split exists

The actual scheduled task lives at the app level (in your coding agent's scheduler), not in
the repo, because the repo has no way to trigger itself on a timer. If the scheduler's
storage is ever lost, moved, or the repo itself is relocated, you rebuild the task from the
copy checked in here — that's the entire reason this folder exists.

## State model — why moving or recreating a runner is lossless

A runner holds **no local state of its own.** Everything it acts on lives in:

- The **shared CRM** (Outreach Stage, counters, live dedupe, batch relations) — see
  `rules/04-crm-conventions.md`.
- **This repo** (`active-focus/`, `brain/`, `rules/`, `outreach/` — everything the runner
  reads at the start of every run).
- **`digests/`** (the run history — one dated file per run).

None of that lives inside the scheduler. So: deleting a runner and recreating it against the
same CRM records and the same repo path simply **resumes** — there is no state to lose, and
no state to reconcile. This is deliberate: it's what makes it safe to move the repo, change
machines, or rebuild a runner from this folder after any of that.

## How to recreate a runner

1. Copy `scheduled-runners/TEMPLATE/SKILL.md`.
2. Fill in `<REPO_PATH>` (the absolute path to this repo on the machine that will run it),
   `<FOCUS_NAME>` (matching `active-focus/focus.md`), `<TRACK_NAME>` (a short label for this
   parallel track, if you're running more than one), and the CRM/DB placeholder tokens from
   `SETUP.md` step 5.
3. In your coding agent's scheduler, create a new scheduled task: give it a description, a
   cron expression (local time), and paste the filled-in prompt verbatim.
4. Verify: list scheduled tasks and confirm it's there and enabled; optionally trigger one
   run by hand. It should only draft — never send — regardless of how it's triggered.
5. If you ever move this repo to a new path, update `<REPO_PATH>` in every recreated runner
   before the next scheduled run — a stale path is the single most common way a runner
   silently stops working.

See `docs/SCHEDULED-RUNNERS.md` for the full build/schedule/verify guide, including the
six-step run contract every runner implements and the staggering guidance for running more
than one track in parallel.

## What NOT to do

- Don't put per-market detail in a runner prompt. If you find yourself naming a specific
  company, university, region, or ICP detail inline in a `SKILL.md` here, stop — that detail
  belongs in `active-focus/focus.md` or `brain/`, and the runner should read it from there.
  A runner that restates the market inline instead of reading it from `brain/` is the
  architectural failure this template exists to prevent.
- Don't give a runner write access to the app database. It's read-only from every layer of
  this system — see `rules/04-crm-conventions.md`.
- Don't let a runner send anything. Every runner drafts only; see `rules/00-draft-first.md`
  and `rules/06-compliance.md`.
