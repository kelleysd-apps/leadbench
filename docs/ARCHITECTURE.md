# LeadBench Architecture

A vertical-agnostic, agent-run cold acquisition system that sources leads, reaches them,
qualifies them, and drives them toward a conversion event — for **any** focus, vertical, or
niche you point it at, now or in the future.

> **Design principle #1 — Niche is data, not architecture.**
> LeadBench never hard-codes who you sell to or what you say. The target vertical, the ICP,
> the offer, the message, the channels, and the conversion goal are all *parameters* that
> live in `active-focus/` and `brain/`. To re-point the entire machine at a new market, you
> edit those two folders. Nothing else changes. If a change would require editing an agent
> file, a rule, or a schema to serve a different market, the change is wrong — push it into
> `brain/` instead.

> **Design principle #2 — Shared infrastructure belongs to the workspace, not the bench.**
> The CRM (Contacts, Companies, Interactions) is workspace-level and shared across every
> function that touches a person or an account. LeadBench *references* the CRM via
> relations; it does not own it. Bench-specific data — Outreach Batches and the Messaging
> Library — lives in LeadBench's own hub.

---

## The three-layer data architecture

```
   ┌─────────────────────────────────────────────────────────────┐
   │ SHARED CRM (workspace-level)  ← used by every function        │
   │  • Contacts, Companies, Interactions                          │
   │  • LeadBench UPDATES contact records (Status, Last Contact)   │
   │  • Other functions own their own record types; everyone logs  │
   │    Interactions                                                │
   └───────────────┬─────────────────────────────────────────────┘
                   │  LeadBench REFERENCES via relations
                   ▼
   ┌─────────────────────────────────────────────────────────────┐
   │ LEADBENCH HUB (bench-specific only)                            │
   │  • Outreach Batches (campaigns; relate to Contacts/Companies) │
   │  • Messaging Library (drafts → approved)                      │
   │  • Active Focus (the swappable control surface)               │
   └───────────────┬─────────────────────────────────────────────┘
                   │  reads/writes
                   ▼
   ┌─────────────────────────────────────────────────────────────┐
   │ APP DATABASE — read-only system of record for conversion      │
   │  • Whatever your product tracks: signups, subscriptions,      │
   │    usage, plans, events                                       │
   │  • THE conversion event lives here                            │
   └───────────────┬─────────────────────────────────────────────┘
                   │
                   ▼
   ┌─────────────────────────────────────────────────────────────┐
   │ SENDING & MARKETING TOOLS (interchangeable limbs)              │
   │  • Landing pages, signup, checkout                            │
   │  • Email sender, ad platforms, whatever you plug in            │
   │  • Connected via pluggable adapters, never assumed             │
   └─────────────────────────────────────────────────────────────┘
```

- **Shared CRM** = the cross-functional system of record for people and accounts. Referenced
  in rules and schemas as `<CRM_CONTACTS_DB>`, `<CRM_COMPANIES_DB>`, `<CRM_INTERACTIONS_DB>`.
- **LeadBench hub** = the bench's own cockpit. Owns batches and messaging only.
- **App database** = the queryable truth for whether outreach actually converted. Read-only
  from LeadBench's side — see `<APP_DB_URL>` and `<APP_DB_TABLE_CONVERSIONS>` in `SETUP.md`.

A workable reference stack is a workspace-wide collaborative database as the shared CRM and
hub, with a hosted Postgres instance as the app database — but any tools that fill the same
three roles work. Name your own equivalents; the three-layer boundary is what matters, not the
vendor. See `rules/04-crm-conventions.md` for the full write discipline this boundary implies.

### Why the boundary is load-bearing

The shared CRM is not LeadBench's. Every function that touches a person — sales, support,
whatever else exists in your workspace — reads and writes the same Contact and Company
records. LeadBench treats that as ground truth it references, never a private copy it
maintains. Two failure modes this prevents:

1. **Duplicate identity.** If LeadBench kept its own copy of "who this person is," it would
   drift from what every other function sees, and a lead already known elsewhere in the
   workspace would get sourced again as if new. Rule 04's pre-flight search exists
   specifically to prevent this — see that rule for the failure mode it's guarding against.
2. **Overwritten funnel truth.** The app database is the one place "did this actually
   convert" is answered. If LeadBench could write to it, a bad run could quietly fabricate a
   conversion, or erase one it didn't understand. Read-only access enforced at the credential
   — not just by convention — is what keeps the app database trustworthy.

The hub layer exists so LeadBench can operate a full cold-outbound campaign — batches,
message drafts, the active focus — without needing write access to either of the layers
around it.

---

## What this is (and isn't)

**It is:** an operator cockpit and lead factory — a structured set of job descriptions
(agents), policies (rules), and source-of-truth records (`state/`, the hub databases) that
turn an AI coding agent into an acting head of outbound working a cold funnel toward a
conversion event.

**It isn't:** the CRM. The CRM is a workspace-level shared resource. LeadBench reads from and
writes to it (Contacts, Companies) via relations, but does not contain it.

**It isn't:** a content library, a campaign, or a niche strategy. Those are *outputs*
LeadBench produces once a focus is loaded. Any example payload in `examples/` is a sample
output, not part of the machine.

**Build depth:** designed to run inside an AI coding agent, single-operator-in-the-loop,
draft-first. See `docs/SCHEDULED-RUNNERS.md` for the unattended-automation path once you've
proven the loop by hand.

---

## Folder map

| Folder | Role | Niche-specific? |
|---|---|---|
| `active-focus/` | The **one** place that defines current target, offer, message, channels, conversion goal. Swap to re-point everything. | **YES — only place** |
| `brain/` | Templates the operator fills per focus: vertical profile, ICP, positioning, offer, voice. | No (templates) |
| `agents/` | Role-based job descriptions: Sourcing, Qualifier, Sequencer, Pipeline, plus the orchestrator. Written against *roles*, never niches. | No |
| `rules/` | Cross-cutting policies every agent obeys — seven of them: draft-first, approval gates, channel etiquette, data privacy, CRM conventions, message guardrails, compliance. | No |
| `templates/` | Output skeletons: outreach batch, weekly report. | No |
| `state/` | Source-of-truth runtime records: the outreach-batch schema, pipeline definition. | No |
| `sync/` | The CRM ⇄ app database ⇄ website sync contract and field maps. | No |
| `scripts/` | Lightweight helpers that can be run to e.g. pull funnel truth from the app database. | No |
| `scheduled-runners/` | Portable template for unattended scheduled runs. The record, not the runtime. | No |
| `docs/` | This architecture doc, the operator runbook, the scheduled-runner guide, enrichment sources, the stage state machine. | No |

---

## How a focus gets loaded (the whole point)

1. Operator fills `active-focus/focus.md` (target vertical, ICP one-liner, offer, conversion
   goal, channels).
2. Operator fills the `brain/` templates for that focus (or asks the agent to draft them from
   a strategy doc).
3. From then on, every agent reads `active-focus/` + `brain/` first, and works the cold funnel
   against *that* target — sourcing the right leads, qualifying against the right ICP,
   drafting the right message, tracking toward the right conversion event.
4. To switch markets: archive the current `active-focus/` and `brain/` fills to
   `active-focus/archive/<focus-name>/`, drop in new ones. The agents, rules, schemas, and
   sync contract are untouched.

---

## The cold funnel LeadBench owns

```
SOURCE ──▶ REACH ──▶ QUALIFY ──▶ NURTURE ──▶ CONVERT ──▶ (retain)
  │          │          │           │           │
Sourcing  Sequencer  Qualifier  Sequencer   tracked in
 agent     agent      agent      agent      app database
                                          (conversion event)

  └──── all stages update the SHARED CRM Contact records ────┘
```

MVP scope: LeadBench drives **SOURCE → REACH → QUALIFY → NURTURE → CONVERT**, with the
conversion event measured from app-database truth, as defined once in `sync/sync-contract.md`
and reused everywhere. The CRM Contact's Status field tracks the lead through its lifecycle
(e.g. Lead → Active → Customer); Outreach Batch counters track bench-specific funnel metrics.

---

## Operating mode: draft-first, human-approved

Every agent produces drafts with **zero side effects**. Nothing is sent, posted, or written
to a live external system until the operator approves, in chat, at the time. See
`rules/00-draft-first.md` and, for anything that touches sending, `rules/06-compliance.md`.

---

See `docs/OPERATOR-RUNBOOK.md` to run your first batch, and `docs/SCHEDULED-RUNNERS.md` for
the unattended-automation path.
