# Setup

An ordered checklist. Times are honest estimates for a first-time setup, not best-case.
Steps are ordered deliberately: you can use the system in draft mode for a while before you
need to create a single account. Don't skip ahead to connecting live tools before you've
proven the focus and brain fills are right — the drafts an agent produces are only as good
as those two folders.

If you haven't already, do the 60-second refusal demo in [`README.md`](README.md) first.
That's step zero — it costs nothing and shows you the safety gate before you invest any
setup time.

---

## 1. Fill the control surface — ~15 minutes

Open `active-focus/focus.md`. This is the one file every agent reads first. Fill in:

- The market/vertical you're targeting
- The ICP one-liner
- The offer
- The conversion goal (what "it worked" means, concretely)
- The channels you intend to use

No accounts required. This is plain-text editing.

## 2. Fill the five brain files — ~45–90 minutes

`brain/` holds five files, each a market fill referenced by every agent:

- `brain/vertical-profile.md` — who this market is and how it operates
- `brain/icp.md` — the precise qualification filter (and disqualifiers)
- `brain/positioning.md` — the angle you lead with
- `brain/offer.md` — what you're actually offering and why now
- `brain/voice.md` — tone, banned phrases, what "on-brand" means for this outreach

Highest leverage: `voice.md` and `positioning.md` — get those two right first, drafts
downstream depend on them most.

No accounts required. You can draft these yourself, or hand a strategy document to the
CMO (Orchestrator) agent (`agents/cmo.md`) and ask it to draft fills for you to review.

## 3. Connect a CRM — ~20–40 minutes (first account required)

The agents need a live, searchable CRM with Contacts, Companies, and an Interactions/activity
log, so the never-duplicate rule (`_agent/SCHEMA.md`, rule 1) has something real to search
against. Notion is a common fit; anything with a comparable data model and an integration
Claude Code can call works. Wire the identifiers into `sync/` and replace the
`<CRM_CONTACTS_DB>`, `<CRM_COMPANIES_DB>`, and `<CRM_INTERACTIONS_DB>` tokens (see the table
in step 5).

You can source and qualify leads once this is connected. You still cannot send anything —
that gate is separate and later.

## 4. (Optional) Connect an app database — ~20–40 minutes

Only needed once you have a real product with a conversion event to track (a subscription,
a signup, a purchase) and want the Pipeline agent to reconcile outreach against it. This
connection is strictly read-only from the suite's side — see `rules/00-draft-first.md` and
the boundaries in `CLAUDE.md`. Skip this step entirely if you don't have this yet; nothing
else in the system depends on it.

### Environment variables `scripts/pull_funnel_truth.py` reads

The script is env-var configured, not token-configured — set these directly in your shell or
runner, separately from the placeholder-token replacements in step 5 below:

| Variable | Required? | What it holds |
|---|---|---|
| `APP_DB_URL` | required | Base REST URL of your app database (same value as the `<APP_DB_URL>` token) |
| `APP_DB_READ_KEY` | required | A READ-ONLY credential (falls back to the legacy `APP_DB_SERVICE_KEY` if that's what's set — still must be read-only) |
| `APP_DB_TABLE_SIGNUPS` | optional | Table name for signup/waitlist events |
| `APP_DB_TABLE_CONTACTS` | optional | Table name for inbound contact/lead records |
| `APP_DB_TABLE_CONVERSIONS` | optional | Table name for the conversion event (paid/subscription status) — same value as the `<APP_DB_TABLE_CONVERSIONS>` token |
| `APP_DB_TABLE_PLANS` | optional | Table name for plan/pricing definitions |

Any table variable you don't set is simply skipped in the script's output. Run
`python3 scripts/pull_funnel_truth.py --help` at any time to see this same list from the
script itself.

## 5. Configure the placeholder tokens

Every file in this repo that needs an environment-specific value uses a placeholder token
instead of a real identifier. Search the repo for each and replace it:

| Token | Where its value comes from |
|---|---|
| `<CRM_CONTACTS_DB>` | Your CRM's Contacts collection identifier |
| `<CRM_COMPANIES_DB>` | Your CRM's Companies collection identifier |
| `<CRM_INTERACTIONS_DB>` | Your CRM's Interactions/activity log identifier |
| `<HUB_BATCHES_DB>` | The Outreach Batches store this suite owns |
| `<HUB_MESSAGING_DB>` | The Messaging Library store this suite owns |
| `<APP_DB_URL>` | Your app database's connection URL (read-only credential — see `rules/06-compliance.md` and `CLAUDE.md` boundaries) |
| `<APP_DB_TABLE_CONVERSIONS>` | The table/view in your app database that records the conversion event |
| `<REPO_PATH>` | The absolute path to this repo on the machine running the agents |
| `<FOCUS_NAME>` | The short name you gave this focus in `active-focus/focus.md` |
| `<SENDER_EMAIL>` | The real, working email address outreach will be sent from (required for CAN-SPAM compliance — see `rules/06-compliance.md`) |
| `<SENDER_POSTAL_ADDRESS>` | The real physical address CAN-SPAM requires in commercial email footers |
| `<PRODUCT_NAME>` | The name of what you're actually selling |

## 6. Run the validator

```
python3 tools/validate.py
```

This reports which `brain/` files are still unfilled templates and which placeholder tokens
remain unconfigured. Fix everything it flags before your first live-connected run. It's safe
to run at any point, including before step 3 — run it early and often.

## 7. Dry run

With the CRM connected and tokens configured, ask Claude Code to run the Sourcing agent for
your focus. Everything it produces is a draft — nothing sends. Review the output against
`brain/positioning.md` and `brain/voice.md` before deciding whether to connect a sender and
move toward approving real sends. See `rules/01-approval-gates.md` for exactly what always
requires your explicit, in-chat approval — that never changes, regardless of setup.

## After setup: how you actually run this

Setup is done once per focus. Running it is ongoing — see [`docs/RUNNING.md`](docs/RUNNING.md)
for the three ways to do that (interactive, a local scheduled task, or a Claude Cowork
scheduled task) and how the draft-first gate holds in each one.
