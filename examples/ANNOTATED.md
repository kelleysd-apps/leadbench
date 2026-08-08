SYNTHETIC EXAMPLE — every company, person, and address below is invented. Do not contact
anyone listed here.

# Annotated walkthrough — why the bike-shop example is filled the way it is

This is the file that actually transfers to your own market. The filled files elsewhere in
`examples/` show you the *shape* of a good fill; this one shows the *reasoning*, which is the
part you can't copy — you have to do it yourself, for your own market. Read this before you
touch your own `brain/` files.

## Why this ICP is narrowed the way it is

The ICP one-liner isn't "bike shop owner." It's "an owner-operator of an independent bicycle
repair shop who's still scheduling repairs by phone, paper ticket, or spreadsheet, and is
visibly backed up during peak season." Every clause in that sentence is load-bearing:

- **"Independent"** — excludes chains, whose owners can't unilaterally buy software even if
  they want to. Reaching a chain location wastes a touch on someone who can say "I like this"
  but never "I'm buying it."
- **"Still scheduling... by phone, paper ticket, or spreadsheet"** — this is the entire product
  fit. A shop that already has online booking has already solved the problem; you'd be
  pitching a replacement, which is a much harder sale than pitching a first solution.
- **"Visibly backed up during peak season"** — this is the difference between a lead who's
  mildly interested and one who's actively in pain right now. It's also *checkable* — a lead
  qualifier can look for it in reviews or social posts without having to guess.

Notice what's absent: no mention of shop size, revenue, or location. Those turned out not to
be load-bearing for this ICP — a lot of markets don't need every dimension filled in, and
padding the ICP with unused detail just gives the Qualifier more surface area to get wrong.

## Why each disqualifier exists

- **Chain/corporate-owned location** — not a moral judgment, a practical one: the owner isn't
  the decision-maker, so even a warm reply dead-ends. This is the single highest-value
  disqualifier in the file because it's the easiest one to miss (a franchise location can look
  identical to an independent one from the outside) and the most expensive one to get wrong
  (a full warm-lead cycle spent on someone who can't buy).
- **Retail-only, no repair bench** — the product literally has nothing to schedule for this
  segment. This isn't a "weak fit," it's a hard no — worth stating plainly rather than leaving
  it to a fuzzy priority score.
- **Already has online booking** — this one is about efficiency, not eligibility. They could
  theoretically still switch, but the message that works on a shop in pain doesn't work on a
  shop that's already solved the problem, and drafting a second message angle for switchers
  wasn't worth it for this focus. A different focus might make the opposite call — that's a
  real decision, not an oversight.

## Why the offer is phrased the way it is

The hero offer is "a 14-day free trial that imports an existing spreadsheet in one step," not
"a powerful scheduling platform." The switching cost is the actual objection a shop owner has
— not "does this work," but "do I have to redo everything I've already got." Naming the
import mechanic in the offer itself pre-answers that objection before it's raised, instead of
making the reader ask.

The reach-stage ask is "watch a 2-minute video," not "start a free trial." That's deliberate
sequencing: the trial ask comes *after* nurture, once the shop owner has seen it working on a
board that looks like theirs. Asking for the trial on first touch would be a bigger ask than
the relationship has earned yet.

## Why the wedge is one moment, not the whole job

`positioning.md`'s wedge is a single Saturday morning, not "running a bike shop" in general.
A wedge that's too broad — "bike shop owners have a lot on their plate" — doesn't give the
Sequencer anything specific to write toward, and it doesn't give the reader anything to
recognize. "I had bikes stacked three deep and no idea whose was next" is something a real
shop owner either has felt or hasn't; there's no room to read it as generic.

## Why the voice rejects the obvious "modernize" pitch

The single most common mistake a new operator would make filling this out is leading with
"digitize your shop" / "leave the spreadsheet behind" — the standard small-business-SaaS
pitch. `positioning.md` explicitly rules this out, and `voice.md`'s "what would you never say"
answer names the specific failure mode: implying the reader's current system, which built a
real business, was wrong. The chaos-moment framing gets to the same pain without the insult.

## What to do differently for your own market

Don't copy this reasoning — replicate the *process*: find the one moment the pain is sharpest,
name the disqualifier that's easy to miss and expensive to get wrong, and decide on purpose
what you'll never say even if it worked. If you can't answer those three questions for your
market yet, that's a sign to go find out — not to fill the file with something plausible-
sounding and move on.
