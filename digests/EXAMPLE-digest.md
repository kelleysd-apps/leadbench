SYNTHETIC EXAMPLE — every company, person, and address below is invented. Do not contact
anyone listed here.

# Digest — bike-shop-scheduling-v1 — 2026-03-14 (worked example)

**Focus:** bike-shop-scheduling-v1 · **Batch:** example-batch-0007 · scheduled run

## STEP 1 — Sourcing (+4 net-new)

Sourced from public shop listings and review sites for independent repair shops matching
`brain/icp.md`. Checked 11 candidate shops; 4 passed the must-have filter, 7 were dropped
(5 for having no visible repair bench, 2 for already advertising online booking).

| Lead | Shop | Signal | Priority |
|---|---|---|---|
| Owner-Operator | Rolling Wrench Bicycle Co. (example.com) | Review: "waited a week to hear back about my bike" | High |
| Owner-Operator | Spoke & Sprocket Cycles (example.org) | Site: "walk-ins only, call ahead" | Medium |
| Service Manager | Pedal Pushers Repair Collective (example.net) | Social post: "board's a disaster this week, bear with us" | High |
| Owner-Operator | Wanderwheel Bike Shop (example.com) | Site: no booking widget, phone-only contact | Medium |

One shop (name withheld — example only) was flagged and dropped mid-review: looked
independent from its storefront branding but its domain redirects to a known regional chain's
franchise page. Logged as a disqualifier hit, not sourced.

## STEP 2 — Enrichment (4 contacts)

All 4 leads already had a public contact email on their shop website — no paid enrichment
needed, so the paid queue was not touched this run. Verified each email's domain matches the
shop's own site (not a third-party booking platform) before marking ready.

## STEP 3 — Drafts

Drafted Email 1 of `examples/outreach/bike-shop-scheduling.md` for all 4 leads, each with its
own `{{observed_signal}}` pulled from the sourcing table above. All 4 held as drafts —
**zero sent.** Nothing in this system sends without explicit operator approval, and none was
given this run.

## STEP 4 — Send / reply tracking

**No-op — zero replies, and here's why.** No emails from the prior batch (example-batch-0006,
run 2026-03-07) have been approved for send yet, so there is nothing to have received a reply
to. This is not a report of "no interest" — it's a report of "nothing has gone out." The
operator's approval queue currently holds 6 drafts total across two batches, none actioned.

## STEP 5 — Reconcile against app database

**No-op.** Checked the `subscriptions` table for `subscription_started` events in the last
30 days attributable to this focus: 0. Expected, given 0 emails have been sent. No conversions
fabricated or estimated to fill this section — there are none, so it says none.

## STEP 6 — Funnel state & next action

Totals across all batches for this focus: 11 Sourced-review, 4 Ready-to-send (this run), 6
Drafted-pending-approval, 0 Sent, 0 Replied, 0 Converted.

**This run accomplished sourcing and drafting, nothing more, and that's a fair summary — not
a soft one.** The bottleneck isn't lead supply or copy; it's that 6 drafts have been sitting in
the approval queue for a full week with no operator action. Sourcing more leads onto an
already-stalled queue would make the number look better without moving anything forward.

**Best next operator action:** review and approve (or reject) the 6 pending drafts before the
next sourcing run — specifically the 2 flagged `High` priority from Rolling Wrench Bicycle Co.
and Pedal Pushers Repair Collective, where the observed signal (a public complaint about lost
tickets) is time-sensitive and loses relevance the longer it sits unsent.
