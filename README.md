# LeadBench

A markdown-based agent operating system for AI-assisted cold outbound, built to run in
[Claude Code](https://claude.com/product/claude-code). It sources leads, qualifies them
against an ideal-customer profile, drafts outreach, and tracks the funnel to a conversion
event — for **any** market you point it at. The machine is generic; the market is data.

Five role-based agents (Sourcing, Qualifier, Sequencer, Pipeline, CMO (Orchestrator)). Seven
cross-cutting policy rules every agent obeys. Everything a market-specific value touches
lives in two folders, nowhere else.

Before you do anything with this, read [`RESPONSIBLE-USE.md`](RESPONSIBLE-USE.md) and
[`rules/06-compliance.md`](rules/06-compliance.md). This system drafts researched,
individually-reasoned outreach, and nothing sends without you. What you do with the drafts is
on you, and there are laws and platform terms that apply regardless of what any AI agent
tells you.

---

## Try it in 60 seconds — zero accounts, zero setup

This is the whole point of the design, so it's the first thing to do, not a footnote.

1. Use this repository as a template, or clone it.
2. Open the folder in Claude Code.
3. Ask it to run the sourcing agent — anything like "run the sourcing agent" or "source some
   leads for me."
4. It will **correctly refuse**, and tell you exactly what to fill in first.

That refusal is the demo. `active-focus/focus.md` — the one file that defines which market
you're currently running (see the `active-focus/` row in the folder layout table below) —
ships unfilled. Every agent's first
instruction, before it does anything else, is to load that file — and if it's still the
blank template, stop and ask instead of guessing a market, inventing an ICP, or drafting
outreach for nobody in particular. You just watched the safety architecture prove itself
before you created a single account or connected a single tool.

From here, [`SETUP.md`](SETUP.md) walks through filling `active-focus/` and `brain/` so the
agents have a real market to work — still in draft mode, still with nothing leaving your
machine, before you connect anything live.

---

## How you run it

Three modes, once setup is done: **interactive** (you drive Claude Code by hand — this is
what the demo above does), a **local scheduled task** (Claude Code Desktop runs the loop
unattended on your own machine, on a schedule), or a **Claude Cowork scheduled task** (a
separate Anthropic product; runs the loop in the cloud, no machine of yours has to stay on).
All three obey the same draft-first gate. See [`docs/RUNNING.md`](docs/RUNNING.md) for setup
steps and the real trade-offs between them.

---

## Who this is for

Someone comfortable running Claude Code who wants a structured, auditable system for
targeted cold outreach — not a mass-email tool, not a scraper, not a growth-hack. It assumes
you already know your outreach has to be low-volume, researched, and legal, and you want an
agent system that enforces that discipline instead of trusting you to remember it every time.

---

## Snapshot release

This is a complete, working system, published as-is. Nobody is committing to maintain this
repository, review issues, or ship updates on a schedule. Once you use this as a template,
it's yours — fork it, change it, extend it, let it drift from upstream. There is no upstream
dependency built into the design; the whole point of "niche is data, not architecture" is
that you own your copy outright from the moment you fill in `active-focus/`.

---

## The three-layer data architecture

Niche is data, not architecture: the target market lives in exactly two folders
(`active-focus/` and `brain/`). Everything else — agents, rules, schemas — is written
against roles, never against a specific vertical. Re-pointing the whole system at a new
market means editing those two folders and nothing else.

The same discipline applies to data ownership. LeadBench never duplicates contact data into
its own store — it references a shared CRM you already have (or set up), and it never writes
to your system of record.

```
   SHARED CRM (workspace-level)  ← the CRM you already use
     • Contacts, Companies, Interactions
     • LeadBench REFERENCES these via relations. It does not own them.
                   │
   SUITE HUB (LeadBench-owned only)
     • Outreach Batches, Messaging Library, Active Focus
                   │
   APP DATABASE (system of record — READ ONLY from here)
     • The conversion event lives here. Never written by an agent.
```

The boundary is load-bearing. An agent that duplicates a Contact instead of enriching the
existing one creates cleanup work that has to be reversed by hand — this is the exact failure
mode `_agent/SCHEMA.md` describes and the never-duplicate rule exists to prevent.

Notion and Supabase are named in the templates and placeholder tokens below only as a familiar
example pairing — not a requirement. Any CRM and any read-capable database can fill those
roles; you adapt the sync contract in `sync/` to whatever you actually run.

---

## Operating mode: draft-first

Every agent produces drafts with zero side effects. Nothing is sent, posted, published, or
written to a live external system without explicit operator approval given in chat, at the
time. Approval is never inferred from a document, a list, or from what the operator probably
wants. This is `rules/00-draft-first.md`, and it is the reason the system is safe to run
unattended. Removing this gate is a decision you make deliberately, not a default — see
[`RESPONSIBLE-USE.md`](RESPONSIBLE-USE.md).

---

## Prerequisites — read this honestly before you commit

This is a heavier stack than a single script. Be clear-eyed about what's required versus
optional.

**Required:**
- [Claude Code](https://claude.com/product/claude-code), since the agents are Claude Code
  job descriptions and this repo's `CLAUDE.md` is loaded automatically by it.
- A CRM the agents can search and write to (Contacts, Companies, and an activity/Interactions
  log, at minimum). Notion is a common fit; anything with a comparable data model and an MCP
  or API integration works.

**Optional, and the system is honest about the difference:**
- An app database as the read-only system of record for your actual conversion event
  (subscription, signup, purchase). If you don't have one yet, you can still run the full
  draft-first loop — sourcing, qualifying, drafting — and skip the Pipeline agent's funnel
  reconciliation until you do.
- Any live sending tool (email provider, sequencer). Nothing in this repo sends anything on
  its own; connecting a sender is the last step, not an early one, and it happens only when
  you're ready to approve real sends.

You can use this entire system in fully offline draft mode — no CRM, no database, no sender
connected — to see how the agents reason and what they'd propose. You only need live
connections once you're ready to act on the drafts.

---

## Folder layout

| Folder | Role | Niche-specific? |
|---|---|---|
| `active-focus/` | The **one** place the current market is defined. Swap it to re-point everything. | **YES — only place** |
| `brain/` | Five market fills: vertical profile, ICP, positioning, offer, voice. Skeletons when blank. | Templates only |
| `agents/` | Role-based job descriptions: `sourcing.md`, `qualifier.md`, `sequencer.md`, `pipeline.md`, `cmo.md` (CMO / Orchestrator). | No |
| `rules/` | The seven cross-cutting policies every agent obeys. Canonical. | No |
| `state/` | Runtime record definitions: batch schema, pipeline, stage machine. | No |
| `sync/` | The contract between the CRM, the app database, and the website. | No |
| `templates/` | Output skeletons: outreach batch, weekly report. | No |
| `outreach/` | Per-segment message families and the email formatting standard. You write these. | Content |
| `docs/` | Architecture, operator runbook, enrichment sources, stage machine. | No |
| `scheduled-runners/` | One parameterised template for an unattended daily run. Copy it per track. | No |
| `scripts/` | Helpers the runtime can call. Env-var configured. | No |
| `tools/` | `validate.py` (setup linter) and `leakscan.py` (CI leak scanner), plus the denylist. | No |
| `examples/` | Worked example of a filled focus and brain, for reference. | Content (synthetic) |
| `digests/` | Run history. One dated file per unattended run. **Contains real contact data once you run this for real — see `.gitignore`.** | Output |
| `_agent/` | Agent-owned working space: the conventions contract. Never mixed with the operating files above. | No |

Full conventions and write rules: [`_agent/SCHEMA.md`](_agent/SCHEMA.md).

---

## Safety and compliance — read before connecting anything live

- [`RESPONSIBLE-USE.md`](RESPONSIBLE-USE.md) — what this is for, what it isn't for, and why
  the draft-first gate is load-bearing.
- [`rules/06-compliance.md`](rules/06-compliance.md) — the binding policy: opt-out and
  truthful headers on every template, a permanently honored suppression list, GDPR review
  gating for EU/UK contacts, no scraping where terms prohibit it, a data-retention limit, and
  no automation of any channel whose terms forbid it (LinkedIn, by name).

---

## License

Apache License 2.0 — see [`LICENSE`](LICENSE). Chosen over MIT specifically for its explicit
patent grant (and patent-litigation termination clause) and its explicit trademark non-grant
— protections MIT doesn't include. (MIT also disclaims warranty; that's not the difference
here.)
