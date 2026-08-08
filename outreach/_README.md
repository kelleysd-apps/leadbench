# outreach/ — message families

This folder holds the actual send-ready copy for the current focus: one message family per
segment (or one overall, if `active-focus/focus.md` names a single segment). It ships empty in
this repo — real message copy is market-specific and belongs here only once you've filled
`brain/positioning.md`, `brain/offer.md`, and `brain/voice.md` for your own focus. Draft
copy that hasn't been written for a real, filled focus doesn't belong here.

## What belongs in a message family

Each file in this folder is one sequence, written for one segment, and should contain:

- A short header naming the segment, the value prop it's built on (link back to
  `brain/positioning.md`, don't restate it), and the merge fields it uses.
- **Email 1 — first touch:** a specific, honest subject line and a short message that names a
  real reason this recipient specifically is being contacted. One ask, and it should be small
  — usually just a reply or a low-commitment next step, not a purchase.
- **Follow-up email(s):** proof/credibility, then a soft close. Each spaced out (note the delay,
  e.g. "+4d").
- An optional secondary-channel touch, if `active-focus/focus.md` names one, marked manual-only
  unless the operator has explicitly approved automation for that channel.

## The email formatting standard

Every email in every family must include:

- A subject line that describes the actual content of the email — no fake "re:" on a thread
  that never existed, no manufactured urgency.
- A working, honest opt-out line (e.g. "reply STOP and I won't follow up again") — and honor it
  immediately and permanently once used.
- The sender's postal address in the footer (`<SENDER_POSTAL_ADDRESS>` — fill with a real,
  correct mailing address; required for compliant commercial email in most jurisdictions).
- No false urgency, no fake scarcity, no "following up on our conversation" framing when no
  conversation has happened.

See `examples/outreach/` for a fully worked message family that models this format for the
fictional bike-shop-scheduling market — read it before writing your own; the compliant form
matters more than the specific words, and it's the thing forkers will copy and re-skin, so it
needs to be right.

## Draft-first, always

Nothing in this folder is a live send target. A message family is copy waiting for an operator
to approve a specific batch of recipients — see `rules/00-draft-first.md`.
