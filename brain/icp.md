---
status: unfilled
---

# ICP Filter — `<FOCUS_NAME>`

<!-- TODO: fill after vertical-profile.md. This is the pass/fail test the Qualifier applies. -->

> Governs: the exact test a lead either passes or doesn't. Read by: the Qualifier agent, every
> lead, every run — this is the file that decides Priority. If this file is vague, the
> Qualifier's scoring is vague, and every downstream report is noise.

## ICP one-liner

`<FILL: one sentence a stranger could use to recognize a qualified lead on sight>`

## MUST-HAVE qualifiers (all required)

`<FILL: list the 2-4 things that MUST all be true, or the lead doesn't advance. Each one
should be checkable from a public profile/website/listing — if you can't verify it without
guessing, it's not a usable qualifier. Example shape:>`

- [ ] `<FILL: qualifier 1>`
- [ ] `<FILL: qualifier 2>`
- [ ] `<FILL: qualifier 3 — or delete if only two apply>`

## STRONG-FIT signals (nice-to-have, raise priority)

`<FILL: what, in addition to the must-haves, makes a lead worth reaching first? Tool mentions,
recent posts, trigger events, second-degree connections — the things that turn a Medium into
a High.>`

## DISQUALIFIERS (any one = out)

`<FILL: who signs the cheque? What breaks in their week that you fix — specific enough that
they'd recognize it? And now the disqualifier question: what disqualifies someone who
otherwise looks like a fit? Be honest here — a vague disqualifier list is how junk leads get
through.>`

## How to score → writes to the CRM Priority field

The Qualifier reasons in fit tiers but persists the result as a single field
(`<CRM_CONTACTS_DB>` → Priority: High / Medium / Low). There is no separate "ICP Fit" field —
don't invent one.

| Fit tier | Test | Persisted Priority |
|---|---|---|
| Strong | all must-haves + 1+ strong-fit signal | `High` |
| Medium | all must-haves, no strong-fit signal | `Medium` |
| Weak | missing a must-have but worth nurturing | `Low` (nurture) |
| Disqualified | hits a disqualifier | `Low` + dated note; flag for operator review |

Reach candidates = Priority `High` or `Medium`.

## What disqualifies someone who otherwise looks like a fit?

`<FILL: this is worth asking twice — it's the question operators skip and regret. Write the
specific case you've actually seen or expect to see, not a generic "not a good fit" line.>`
