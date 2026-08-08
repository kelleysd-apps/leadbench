SYNTHETIC EXAMPLE — every company, person, and address below is invented. Do not contact
anyone listed here.

# ACTIVE FOCUS — worked example

> This is the filled version of `active-focus/focus.md` for a fictional market. See
> `examples/ANNOTATED.md` for the reasoning behind each choice.

---

## Status

- **Focus name:** `bike-shop-scheduling-v1`
- **Activated:** 2026-03-01 (example date)
- **Owner:** the Founder (example persona — no real person)
- **Prior focus archived at:** none — first focus for this fictional product
- **Strategic role:** Direct revenue play. This is the whole business, not a bridge to
  something else — SpokeDesk is a scheduling tool built specifically for independent bike
  repair shops, and this cold-outreach motion is how it gets its first paying shops.

---

## 1. Product / what we lead with

- **Product:** SpokeDesk — appointment scheduling and repair-ticket tracking built
  specifically for independent bicycle repair shops.
- **Capability sold:** never lose track of whose bike is next, or what work it's in for,
  even when the shop is three-deep on a Saturday.
- **Hero offer:** a 14-day free trial that imports an existing paper or spreadsheet booking
  system in one step — no card required to start.
- **Why now:** spring tune-up season is when every independent shop's manual system visibly
  breaks; that's the moment a shop owner is most willing to try something new.

## 2. Target (the niche — DATA, not architecture)

- **Method:** single segment, committed from the start — independent bike shop owners are a
  narrow enough, well-understood enough market that a wide multi-segment blast isn't needed.
- **Behavior or segment we target:** owner-operators of independent bicycle repair shops who
  are still booking repairs by phone, paper ticket, or spreadsheet.
- **Segment hypotheses (if testing several):** single segment — no parallel hypotheses running.
- **ICP one-liner:** an owner-operator of an independent bike repair shop who's still
  scheduling repairs manually and is visibly backed up during peak season. (Full filter:
  `brain/icp.md`.)
- **Disqualifiers:** big-box or chain service counters, retail-only shops with no repair
  bench, shops already on a competing scheduling tool. (Full list: `brain/icp.md`.)

## 3. Conversion goal (the revenue event)

- **Primary conversion event:** `subscription_started` — a trial converting to any paid plan.
- **Measured from:** `<APP_DB_URL>` — `<APP_DB_TABLE_CONVERSIONS>` (`subscriptions.status =
  'active'`).
- **Funnel entry point fed by outreach:** `trial_signups` (cold reply → trial start).
- **Secondary/leading events:** trial started, spreadsheet imported, first ticket created.

## 4. Channels (cold)

- **Primary channel:** cold email — shop owners are reachable at a public shop email address
  and don't expect or want LinkedIn outreach.
- **Secondary channel:** none.
- **Constraint:** all channels run draft-first — nothing sends without explicit operator
  approval, every time.

## 5. Source of truth wiring (for this focus)

- **Operator cockpit:** `<CRM_CONTACTS_DB>` board, reviewed daily during active outreach.
- **CRM tables:** `<CRM_CONTACTS_DB>`, `<CRM_COMPANIES_DB>`, `<CRM_INTERACTIONS_DB>`.
- **Outreach hub tables:** `<HUB_BATCHES_DB>`, `<HUB_MESSAGING_DB>`.
- **Funnel truth:** `<APP_DB_URL>` (production).
- **Segment instrumentation:** not applicable — single segment; no per-segment tagging needed.

## 6. Success metric for the outreach engine

- **North-star (revenue):** new paid subscriptions per month attributable to cold outreach.
- **Niche-detection metric:** not applicable — single segment already committed.
- **Engine health (leading):** sourced → replied → trial started → spreadsheet imported →
  subscribed.
- **Narrow rule:** not applicable — no segment-promotion decision to make; this focus reviews
  reply rate and trial-to-paid conversion instead, monthly.

---

## How to switch focus

See `active-focus/focus.md` at the repo root — the mechanics are identical regardless of
market.
