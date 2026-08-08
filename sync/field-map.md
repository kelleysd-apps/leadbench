# Field Map (quick reference)

This file is a CONTRACT SHAPE, not live data. Fill in your own field names, table names, and
select options as you set up LeadBench against your CRM and app database. A worked example
(clearly labeled) follows the shape so you can see what a filled-in version looks like.

## The shape

Contacts.Status options: an operator-defined enum, minimally covering the lifecycle stages in
state/pipeline-definition.md (something like `Lead` / `Active` / `Customer` / `Inactive` /
`Churned`).
Contacts.Priority options: `High` / `Medium` / `Low` (set by Qualifier; ICP-fit signal — this
one is fixed by the suite's design, not operator-configurable).

### Shared CRM — Contacts (`<CRM_CONTACTS_DB>`) ← app database (`<APP_DB_URL>`)
- Email                    ← match key (lowercased, trimmed)
- Status "Active"          ← [your signup-completed signal]
- Status "Customer"        ← [your paid/subscription-active signal]
- Status "Churned"         ← [your canceled/past-due signal] (corroborate via an events table if you have one)
- Last Contact             ← most recent of your signup/event timestamps
- Notes (append-only)      ← record reconciliation events; never destructive
- Priority                 ← NOT synced from the app database; set by Qualifier from brain/icp.md

### Shared CRM — Companies (`<CRM_COMPANIES_DB>`) ← app database
- Email domain match       ← derive from Contacts.Email if Company unknown
- Status                   ← progresses with associated Contact statuses

### LeadBench — Outreach Batches (`<HUB_BATCHES_DB>`) → Shared CRM
- Target Contacts          → relation, many Contacts per Batch (dual relation)
- Target Companies         → relation, many Companies per Batch (dual relation)
- Counters: `Leads Sourced` / `Leads Reached` / `Replies` / `Signups` / `Paid Conversions`
  are real **number** fields on the Batch, updated by the Pipeline agent (NOT auto-derived
  rollups). Pipeline sets them from the count of related Contacts in each Status + the app
  database's truth.

### Never synced (operator intent fields, CRM-only)
- Outreach Batch: Objective, Constraints/Guardrails, Status (draft→approved→...)
- Messaging Library: Body, Approval state, Voice Notes Used

---

## Worked example (illustrative only — replace with your own values)

This is a mapping with placeholder table/column names, shown only so you can see the shape
filled in. None of these names are meaningful to your instance — replace them with your own
app database's real tables and columns.

- App database table `signups` (email match) → Contacts.Status = "Active"
- App database table `conversions`, column `status = 'active'` → Contacts.Status = "Customer"
- App database table `conversions`, column `status IN ('canceled','past_due')` →
  Contacts.Status = "Churned", corroborated by a `conversion_events` table
