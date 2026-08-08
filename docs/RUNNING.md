# Running LeadBench — the three ways to execute it

`SETUP.md` gets the focus, brain, and connectors ready. This doc covers what to actually do
once that's done: how you invoke the agents, in which of three modes, and what changes about
the draft-first gate in each one.

All three modes run the exact same agents, reading the exact same `active-focus/` and
`brain/` files, obeying the exact same `rules/`. What changes is *where the run executes* and
*whether a human is watching it happen*. Nothing here changes what the agents are allowed to
do — see `CLAUDE.md` and `rules/00-draft-first.md` for that.

---

## The three modes at a glance

| | 1. Interactive | 2. Local scheduled task | 3. Cowork scheduled task |
|---|---|---|---|
| **Where it runs** | Your machine, Claude Code, driven by you turn by turn | Your machine, unattended | The cloud by default, or your machine if you choose a local Cowork task |
| **Machine must stay awake?** | Only while you're at the keyboard | Yes — the task only fires while Claude Code Desktop is open and the computer is awake (a "Keep computer awake" option exists) | No, for a cloud task. Yes, for a local Cowork task |
| **File access model** | Direct local filesystem — Claude Code reads/writes this repo like any other tool | Direct local filesystem, same as interactive | Cloud task: MCP connectors plus a **read-only** GitHub sync (file contents only, no write-back, no commit history). Local Cowork task: direct local filesystem, same as mode 2 |
| **Draft-first still enforced?** | Yes, and you're watching it happen live | Yes, in the sense that the agent still only creates drafts — but no human watches the run as it happens; enforcement is entirely the prompt and the rules, not a click-to-approve step | Same caveat as mode 2 — see "The draft-first gate in unattended modes" below |
| **Best for** | First runs, tuning `brain/`/`active-focus/`, anything you want to watch and steer | Ongoing runs once the loop is proven, when you're fine leaving a machine on | Fully cloud-hosted automation, when your CRM and sending tool are reachable through connectors and you don't need this repo's own files (like `digests/`) written back to disk |

The rest of this doc walks through each mode: what it is, when to choose it, how to set it
up, and its real limitations.

---

## Mode 1 — Interactive, in Claude Code

**What it is.** You open this repo in Claude Code and ask it, by hand, to act as one of the
five agents. This is what the 60-second demo in `README.md` does, and it's how
`docs/OPERATOR-RUNBOOK.md` walks you through your first batch.

**When to choose it.** Always choose this first. Every other mode is this same loop run
unattended — prove it works by hand before you let it run without you. It's also the right
mode any time you're editing `brain/` or `active-focus/` and want to see how the agents react
before locking anything into a schedule.

**Setup.** Nothing beyond what `SETUP.md` already covers: open the folder in Claude Code, and
talk to it — "run the sourcing agent," "act as the qualifier agent and score today's new
leads," and so on. `docs/OPERATOR-RUNBOOK.md` has the full walkthrough.

**Limitations.** It only runs while you're present. Nothing happens between sessions unless
you start one.

**Draft-first in this mode.** This is the mode the gate was designed around: every draft is
produced with you in the room, and every approval in `rules/01-approval-gates.md` happens in
the same conversation, in real time.

---

## Mode 2 — Local scheduled task in Claude Code

**What it is.** Claude Code Desktop's **Routines** page can create a *local scheduled task*:
a saved prompt that fires on a schedule you pick, starting a fresh Claude Code session on
your own machine with direct access to this repo's files. This is the mechanism
`docs/SCHEDULED-RUNNERS.md` and `scheduled-runners/TEMPLATE/SKILL.md` are written against —
"your coding agent's scheduler," concretely, is this feature.

Claude Code Desktop also offers `/loop` (a session-scoped repeat, only alive while a terminal
session stays open) and cloud **Routines** (see mode 3's cloud-connector caveats, but for
Claude Code itself rather than Cowork — check
[the Routines docs](https://code.claude.com/docs/en/routines) if fully cloud-hosted execution
of the *Claude Code* agents, rather than Cowork, is what you want). This doc focuses on the
local scheduled task because it's the closest match to what `scheduled-runners/` already
assumes: direct filesystem access to `<REPO_PATH>`, no connector-based file sync.

**When to choose it over the others.** You want unattended, repeating runs, you're fine
leaving a machine on (or turning on "Keep computer awake"), and you want the agent reading
and writing this repo's files directly rather than through a connector.

**Setup.**
1. In Claude Code Desktop, click **Routines** in the sidebar, then **New routine**, and
   choose **Local**.
2. Fill in a name, a description, and the instructions — this is where you paste the filled-in
   prompt from `scheduled-runners/<track-name>/SKILL.md` (see `docs/SCHEDULED-RUNNERS.md` for
   how to build that file first).
3. Pick the working folder (this repo, at `<REPO_PATH>`) and a schedule. The built-in presets
   are Manual, Hourly, Daily, Weekdays, and Weekly; for anything else (every 15 minutes, the
   first of the month), describe it in plain language to Claude in a session and it will set
   the underlying cron expression for you.
4. Set the task's permission mode. Run it once by hand first ("Run now") and approve each
   tool it needs, so future scheduled runs don't stall waiting on a permission prompt you're
   not there to answer.
5. Save `scheduled-runners/<track-name>/SKILL.md` back into this repo per
   `docs/SCHEDULED-RUNNERS.md` step 4, so the task is recoverable if the scheduler's own state
   is ever lost.

**Limitations.**
- The task only fires while Claude Code Desktop is running and your computer is awake. If the
  machine sleeps through a scheduled time, that run is skipped — there's an optional
  "Keep computer awake" setting to prevent that, at the obvious cost of leaving the machine
  running.
- If the computer was asleep or the app was closed, Desktop runs one catch-up execution for
  the most recently missed time when it next wakes, and discards any other missed runs — it
  does not run once per missed interval.
- Moving the repo means updating `<REPO_PATH>` in the saved task, same as
  `docs/SCHEDULED-RUNNERS.md`'s rebuild instructions already describe.
- The exact UI may have moved since this was written — check
  [the current Claude Code Desktop scheduled-tasks docs](https://code.claude.com/docs/en/desktop-scheduled-tasks)
  for the authoritative steps.

**Draft-first in this mode.** Nothing about scheduling changes what the agent is allowed to
do — the same `rules/00-draft-first.md` prompt discipline applies. What changes is that no
human is watching the run happen turn by turn. Two things matter more here than in mode 1:
- Only ever connect a **draft-only** sending tool to a scheduled task, exactly as
  `docs/SCHEDULED-RUNNERS.md`'s connector list already specifies — never a connector capable
  of an actual send.
- Review each run's digest entry in `digests/` and the CRM Notes it left, the same way you'd
  review a run you watched live, before you approve anything for real. Unattended does not
  mean unreviewed.

---

## Mode 3 — Claude Cowork scheduled task

**What it is.** Claude Cowork is a separate Anthropic product from Claude Code, aimed at
general knowledge work rather than a coding CLI. Its scheduled tasks save a prompt and a
cadence, and by default run as cloud-hosted sessions on Anthropic's infrastructure — they
fire on schedule even when your computer is off or asleep. Cowork can also run a task
*locally*, through the Desktop app, in which case it behaves like mode 2: direct local file
access, machine must stay on.

**When to choose it over the others.** You want a run that doesn't depend on any machine of
yours being on at all, and everything the agent needs — the shared CRM, the sending tool — is
reachable through a Cowork connector. Choose this over mode 2 specifically when "the machine
has to stay awake" is the blocker.

**Setup.**
1. In Cowork, type `/schedule` in a task, or click **Scheduled** in the sidebar and create a
   new one.
2. Either describe what you want and let Claude propose a configuration, or fill in the task
   name, prompt, approval mode, frequency (hourly, daily, weekly, weekdays, or manual), model,
   and folder yourself.
3. For the prompt, use the same filled-in text as `scheduled-runners/TEMPLATE/SKILL.md` —
   every `<...>` token replaced, all six run-contract steps intact.
4. Connect the shared CRM, the LeadBench hub, and a **draft-only** sending tool as Cowork
   connectors before the first run, the same connector list `docs/SCHEDULED-RUNNERS.md`
   already gives.
5. For this repo's own files (`active-focus/`, `brain/`, `rules/`, `agents/`), connect GitHub
   as a Cowork connector and select this repository — see the real limitation below before
   you rely on this for anything that needs writing back.

**Limitations — read this before you pick this mode for LeadBench specifically.**
- A cloud Cowork task cannot see your local filesystem at all. If a scheduled task needs
  local files or local apps, Cowork's own documentation says it will only run locally — not
  in the cloud.
- The GitHub connector Cowork uses to read this repo's files is **read-only**: it syncs file
  names and contents from a single selected branch, and explicitly does not retrieve commit
  history or pull requests. There is no path for a cloud Cowork task to write a new entry
  back into `digests/`, or to commit anything to this repo, the way a mode-2 local task can.
  If your runner needs to append to `digests/` per `docs/SCHEDULED-RUNNERS.md` step 6, either
  run it as a *local* Cowork task, or have the runner write that record somewhere your CRM or
  hub connector can reach instead of the git working tree.
- Cost and plan requirements, exact approval-mode names, and the connector-setup UI are the
  kind of thing that changes between releases — check
  [the current Cowork scheduled-tasks documentation](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork)
  for the authoritative steps before you build on this.

**Draft-first in this mode.** Same principle as mode 2, with the gap made sharper by the fact
that a cloud run is even further from your direct observation: the safety property is the
prompt itself (`rules/00-draft-first.md`, `rules/01-approval-gates.md`), not any platform
permission screen. Set the task's approval mode as conservatively as Cowork allows, connect
only a draft-only sending tool — never a connector capable of a real send — and review every
run's output before you approve anything for real, exactly as in mode 2. Unattended and
cloud-hosted is not a reason to relax that discipline; if anything, it's the strongest reason
to keep it, since nobody is watching the run as it happens.

---

## Choosing between the two unattended modes

If you're deciding between mode 2 and mode 3 for an already-proven loop: mode 2 gives direct,
two-way access to this repo's own files (including `digests/`) at the cost of needing a
machine to stay on; mode 3 removes that machine-uptime cost but, run in the cloud, only reads
this repo's files one-way and can't write `digests/` entries back to it. Neither mode changes
what the agents are allowed to do or loosens `rules/00-draft-first.md` — that gate travels
with the prompt, not the platform it runs on.
