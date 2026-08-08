---
status: unfilled
---

# ACTIVE FOCUS

<!-- TODO: this file is the control surface for the entire LeadBench system. -->

> **This is the control surface for the whole system.**
> Every agent — sourcing, qualifying, sequencing, pipeline — reads this file first, before
> anything else. To re-point the system at a new market, replace the values below and fill
> `brain/`. Never edit an agent, a rule, or a schema to change focus — if you find yourself
> doing that, stop; the market belongs here, not there.
>
> **If this file is still unfilled** (status above, or any `<FILL:>` / `TODO` left below), every
> agent must refuse to run a sourcing, qualifying, sequencing, or send action and tell the
> operator to fill this file first. That refusal is correct behavior — it is the system
> working as designed, not a bug to route around.

---

## Status

- **Focus name:** `<FILL: a short slug for this market, e.g. "midwest-hvac-v1" — matches the
  value you'll tag records with in the CRM/hub>`
- **Activated:** `<FILL: date you turned this focus on>`
- **Owner:** `<FILL: who owns this focus — a name, not a role>`
- **Prior focus archived at:** `<FILL: active-focus/archive/<prior-focus-name>/, or "none">`
- **Strategic role:** `<FILL: what is this focus FOR? A direct revenue play? A bridge that
  funds something else? A validation test before a bigger bet? Say it plainly — this framing
  changes how hard downstream agents should push and what "success" means.>`

---

## 1. Product / what we lead with

- **Product:** `<PRODUCT_NAME>` — `<FILL: one line: what it is>`.
- **Capability sold:** `<FILL: the specific thing this market would actually pay for — not
  your whole feature list, the one capability that's the wedge>`.
- **Hero offer:** `<FILL: what a cold lead is offered first — a demo, a free sample deliverable,
  a trial, a call. See brain/offer.md for the full mechanics.>`
- **Why now:** `<FILL: why this product, why this market, why this moment — one sentence>`.

## 2. Target (the niche — DATA, not architecture)

- **Method:** `<FILL: are you pre-committing to one segment, or blasting several hypotheses
  and letting reply data pick the winner? Say which, and why.>`
- **Behavior or segment we target:** `<FILL: the defining behavior/role/trigger that makes
  someone reachable and relevant — not just a job title>`.
- **Segment hypotheses (if testing several):** `<FILL: list the segment tags you're running in
  parallel, or "single segment" if you've already committed>`.
- **ICP one-liner:** `<FILL: one sentence a stranger could use to recognize this person. Full
  filter lives in brain/icp.md — do not duplicate it here, link to it.>`
- **Disqualifiers:** `<FILL: the one or two things that knock someone out even if they look
  like a fit. Full list in brain/icp.md.>`

## 3. Conversion goal (the revenue event)

- **Primary conversion event:** `<FILL: the one event that counts — name it exactly as it
  appears in the system of record, e.g. a table/column/status value>`.
- **Measured from:** `<APP_DB_URL>` — `<APP_DB_TABLE_CONVERSIONS>` (`<FILL: the field/status
  that flips true on conversion>`).
- **Funnel entry point fed by outreach:** `<FILL: what table/list captures a cold lead's first
  action — signup, inquiry, reply>`.
- **Secondary/leading events:** `<FILL: earlier signals worth tracking on the way to
  conversion — demo booked, trial started, reply received>`.

## 4. Channels (cold)

- **Primary channel:** `<FILL: cold email, LinkedIn, cold call, other — and why this one>`.
- **Secondary channel:** `<FILL: or "none">`.
- **Constraint:** all channels run **draft-first** — nothing sends without explicit operator
  approval, every time, no exceptions inferred from a prior approval.

## 5. Source of truth wiring (for this focus)

- **Operator cockpit:** `<FILL: where the operator reviews and approves work>`.
- **CRM tables:** `<CRM_CONTACTS_DB>`, `<CRM_COMPANIES_DB>`, `<CRM_INTERACTIONS_DB>`.
- **Outreach hub tables:** `<HUB_BATCHES_DB>`, `<HUB_MESSAGING_DB>`.
- **Funnel truth:** `<APP_DB_URL>` (`<FILL: which system/environment is authoritative>`).
- **Segment instrumentation:** `<FILL: how a segment gets tagged on a record so results can be
  compared segment-to-segment>`.

## 6. Success metric for the outreach engine

- **North-star (revenue):** `<FILL: the one number that means this focus is working>`.
- **Niche-detection metric (if blasting multiple segments):** `<FILL: the metric that decides
  which segment hypothesis wins — usually positive-reply rate plus volunteered-pain quality>`.
- **Engine health (leading):** `<FILL: the funnel stages you track between "sourced" and
  "converted">`.
- **Narrow rule:** `<FILL: the rule that decides when to stop testing and commit — e.g. after N
  qualified touches per segment, promote the top performer, pause the rest>`.

---

## How to switch focus

1. `mkdir active-focus/archive/<this-focus-name>` and move the current `focus.md` plus the
   filled `brain/` files there.
2. Write a new `focus.md` with the new target, offer, conversion goal, and channels.
3. Refresh `brain/` for the new focus (see `brain/_README.md` for fill order).
4. Run the system. Agents, rules, and schema are unchanged — that's the point.
