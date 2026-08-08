SYNTHETIC EXAMPLE — every company, person, and address below is invented. Do not contact
anyone listed here.

# ICP Filter — bike-shop-scheduling-v1 (worked example)

## ICP one-liner

An owner-operator of an independent bicycle repair shop who's still scheduling repairs by
phone, paper ticket, or spreadsheet, and is visibly backed up during peak season.

## MUST-HAVE qualifiers (all required)

- [ ] **Independently owned repair shop** — not a chain location, not a big-box service
  counter (evidence: single-location website, "family owned" / "independently owned" language,
  or absence from any known chain's location list).
- [ ] **Actually repairs bikes, not just sells them** — a repair bench or service department
  visible on the shop's website or listing, not a retail-only storefront.
- [ ] **Visible evidence of manual scheduling** — the shop's website or booking page says "call
  to book," "walk-ins only," links to a plain contact form, or otherwise shows no online
  scheduling widget.

## STRONG-FIT signals (nice-to-have, raise priority)

- Public reviews mentioning long waits, lost tickets, or "they lost track of my bike."
- Recent social post about being fully booked or backed up.
- Second mechanic hired in the last year (growth outpacing the old system).
- Multiple service bays or an "express tune-up" line — implies higher repair volume, more
  pain from a manual system.

## DISQUALIFIERS (any one = out)

- Chain or corporate-owned location (even if the storefront looks independent).
- Retail-only — no repair bench.
- Already advertises online booking or a named scheduling tool on their site.
- Fewer than roughly 5 repairs/week by any visible signal (seasonal hobby shop, not enough
  volume for the pain to be acute yet).

## How to score → writes to the CRM Priority field

| Fit tier | Test | Persisted Priority |
|---|---|---|
| Strong | all must-haves + 1+ strong-fit signal | `High` |
| Medium | all must-haves, no strong-fit signal | `Medium` |
| Weak | missing a must-have but worth nurturing | `Low` (nurture) |
| Disqualified | hits a disqualifier | `Low` + dated note; flag for operator review |

Reach candidates = Priority `High` or `Medium`.

## What disqualifies someone who otherwise looks like a fit?

A shop that *looks* independent — friendly name, local branding, a single storefront photo —
but is actually a franchise location of a regional chain. Franchise agreements often mandate
a corporate scheduling system the owner has no authority to replace, so even a warm reply
here dead-ends. Check the shop name against known chain rosters before reaching out, not
after a reply comes back saying "I don't actually control that."
