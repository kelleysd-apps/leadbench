# brain/ — the per-focus knowledge base

<!-- TODO: this whole folder is unfilled until each of the five files below is filled. -->

These five files are the ONLY place market detail may live in this system. `active-focus/
focus.md` names the focus and points here; everything downstream — sourcing, qualifying,
sequencing, pipeline reporting — reads these files, never a hard-coded assumption baked into
an agent, a rule, or a schema. If you ever catch yourself about to write a market fact
somewhere else, that is the signal to put it here instead.

They ship as TEMPLATES: structured skeletons with `<FILL: ...>` prompts, not blank pages. A
blank page gets filled by imitating whatever example you last saw. A pointed question forces
an actual decision. Answer the question, don't just describe the market — the value of this
folder is operator judgment, not a paragraph of description.

## Fill order

Fill them in this order — each one narrows the next:

1. **`vertical-profile.md`** — the market. Who they are, where they're reachable, how they
   buy. Broadest file; sets the boundaries everything else works inside.
2. **`icp.md`** — the precise filter. Given the market above, exactly who counts as a
   qualified lead, and what disqualifies someone who otherwise looks right.
3. **`positioning.md`** — the wedge. Given who they are and what disqualifies them, what's the
   one pain you lead with and the one thing you deliberately don't say.
4. **`offer.md`** — what you actually sell, and what counts as the tracked conversion event.
5. **`voice.md`** — highest-leverage file, loaded on every copy-drafting task. Tone rules,
   banned phrases, and good/bad examples so every draft sounds like the same operator wrote it.

## Status conventions

Each file marks its fill state three redundant ways so tooling can detect it reliably:
a `status: unfilled` frontmatter line, a `TODO` comment near the top, and `<FILL: ...>`
placeholders in every section that still needs an answer. `tools/validate.py` checks all
three. When a file is genuinely filled, remove all three markers from it — don't leave a
`status: unfilled` line sitting above real content.

## When you switch focus

Archive the filled versions to `active-focus/archive/<old-focus-name>/brain/` before
overwriting them with the new market's answers (see `active-focus/focus.md` → "How to switch
focus"). Never delete a prior fill — archive it.
