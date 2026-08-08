# Sync Contract — Shared CRM ⇄ LeadBench ⇄ App Database

Defines exactly which data flows which direction. By design:
**The app database stays the system of record. The shared CRM is the workspace-level operator
truth. LeadBench owns only bench-specific records (Batches, Messaging).**

This file is a CONTRACT SHAPE. Fill in your own table/database names using the placeholder
tokens below; a worked example follows, clearly labeled, so you can see a filled-in version.

## Direction of truth

| Layer | Owns | Reads from |
|---|---|---|
| **Shared CRM** (`<CRM_CONTACTS_DB>`, `<CRM_COMPANIES_DB>`, `<CRM_INTERACTIONS_DB>`) | Contacts, Companies, Deals, Interactions | App database (reconciled) |
| **LeadBench** (`<HUB_BATCHES_DB>`, `<HUB_MESSAGING_DB>`) | Outreach Batches, Messaging Library, Active Focus | Shared CRM (via relations), App database (read-only) |
| **App database** (`<APP_DB_URL>`) | Funnel truth: signups, paid status, plans | nothing — system of record |

The shared CRM (or LeadBench) NEVER writes to the app database in the MVP. Two-way write-back
is a future option, not a default.

## App database → Shared CRM (read-only reconciliation)
The Pipeline agent reads these and updates **shared CRM Contacts** (not a bench-owned CRM):

| App database source | Shared CRM target | Rule |
|---|---|---|
| Signups table (email match) | Contacts.Status = "Active" (was "Lead"), add Interaction record | match on email |
| Inbound-contacts table (email match), if you have one | Contacts.Status updates from inbound status | inbound inquiries |
| Conversion table, "active" state | Contacts.Status = "Customer" | THE conversion event (`<APP_DB_TABLE_CONVERSIONS>`) |
| Conversion-events table, if you have one | corroborate paid/churn status; add Interaction | event log |
| Plans table, if you have one | brain/offer.md pricing source | never invent a price |

## LeadBench → Shared CRM (via relations)
- Outreach Batches.Target Contacts → references shared CRM Contacts (many-to-many).
- Outreach Batches.Target Companies → references shared CRM Companies.
- An approved send creates an Interaction record (logged against the Contact).

## Shared CRM → Outside (future, via adapters)
- Approved Messaging Library assets → outreach sender (when chosen).
- Sender uses the Target Contacts relation as the address list.
- Adapters are pluggable; the bench assumes connection POINTS, not specific tools.

## Reconciliation cadence (MVP)
- Triggered: operator (or an automation) runs scripts/pull_funnel_truth.py, Pipeline agent
  reconciles.
- Match key: email (lowercased, trimmed). Flag ambiguous/multiple matches for human review.

## Boundary rules (architectural)
- LeadBench NEVER duplicates Contact data. If you need lead info in an Outreach Batch, use
  the relation; don't copy fields.
- Sales/CS/other departments will add their own hubs that reference the same shared CRM. The
  CRM is workspace-level; future hubs follow the same "reference, don't own" rule.

---

## Worked example (illustrative only — replace with your own values)

Shown only so you can see the contract filled in with placeholder names. None of these names
carry over to your instance — swap them for your own app database's real tables:

- App database: a Postgres project accessed via a read-scoped key.
- Conversion table: a `conversions`-style table, conversion = `status = 'active'`.
- Signups table: a `signups`-style table, matched to Contacts by email.
