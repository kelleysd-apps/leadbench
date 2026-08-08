# Outreach Stage — status-driven control plane

The shared CRM is the SSOT and control plane. The operator drives the whole funnel with ONE
field on each Contact: **`Outreach Stage`**. The operator only ever sets **`Approved`** or
**`Hold / drop`** (from a lead-triage view scoped to that field). Agents — whether run by
hand or on a schedule — do everything else. No chat is required for the operator's own moves,
though every send still requires the draft-first approval described in
`rules/00-draft-first.md`.

`Outreach Stage` values: `Sourced - review` · `Approved` · `Ready to send` · `Sent` ·
`Needs [paid gap-fill]` · `Hold / drop`.

## Flow

```
Sourced - review ─(operator: Approved)→ Approved
   → REFINE (free public-source enrichment): find a verified, allowlisted email
       ├─ found              → write Email → Ready to send
       ├─ none, in-ICP       → stay Approved, flag "needs paid gap-fill (operator, chat)"
       └─ email is out-of-ICP → Hold / drop (mis-affiliated, out of ICP)
   → DRAFT (compose from outreach/ copy → create a draft in your sending tool → log an
     Interaction)
   → (operator approves and sends) → SEND/REPLY TRACKING → Sent + reply logged
 (operator: Hold / drop) → parked
```

## Refinement / enrichment workflow (free-first, provider-free by default)

See `docs/ENRICHMENT-SOURCES.md` for the full waterfall pattern. In short:

1. Public professional/registry sources specific to your vertical — accepted only if the
   found address is name- or domain-matched to the lead, and validated against your focus's
   domain allowlist. A real, published professional address — not a guess (rule 03 compliant).
2. Organization directory or team-page fallback for misses.
3. A paid enrichment provider — gap-fill only, operator-run in chat, capped at an
   explicitly-confirmed credit cost, never called unattended.

Never pattern-guess an unverified address, under any circumstance.

**Bonus: enrichment is also affiliation QA.** If the only emails found are at an
out-of-focus organization, the lead was mis-sourced → auto `Hold / drop`, out of ICP.

## Sending

- Your connected sending tool is the single outbound source; the CRM/hub is the full log and
  analytics surface.
- The agent **drafts** into the sending tool at `Ready to send` (never sends). The operator
  sends by hand, or via an explicit, approved send step — see `rules/00-draft-first.md` and
  `rules/06-compliance.md`.
- The next run detects the sent message and any reply, advances the record to `Sent`, logs
  Interactions, and updates batch counters (Leads Reached / Replies). Track funnel analytics
  in the hub: sent → reply → positive reply → conversion. Open/click rates need a tracking
  pixel and aren't assumed here.

## The one instant automation worth setting up

If your CRM/hub platform supports native record automations, wire the deterministic hop so it
fires the moment the operator approves, with no agent lag:

> Contacts → Automations → New: **When** `Outreach Stage` is set to `Approved` **and**
> `Email` is not empty → **then** set `Outreach Stage` = `Ready to send`.

Everything else (enrichment, drafting, send/reply tracking, reconcile) is the scheduled
runner's job — see `docs/SCHEDULED-RUNNERS.md`.

## Two (or three) fields, two (or three) jobs

- `Outreach Stage` = the LeadBench workflow/gates (this doc).
- `Status` (e.g. `Lead`/`Active`/`Customer`/`Inactive`/`Churned`) = the shared lifecycle
  field, sourced from the app database via `sync/sync-contract.md`.
- `Priority` (`High`/`Medium`/`Low`) = ICP fit, set by the Qualifier agent against
  `brain/icp.md`.

Don't conflate these into one field, and don't add a parallel scoring field — see
`_agent/SCHEMA.md`'s "one fact, one file" principle for schema fields generally.
