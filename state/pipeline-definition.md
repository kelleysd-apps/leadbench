# Pipeline Definition (conceptual funnel → where each stage is persisted)

Cold funnel, terminating in paid. **There is no single "Stage" field in the CRM.** The
funnel below is the *conceptual* model; each stage is persisted across three real surfaces:

- **Contacts.Status** (select: `Lead` / `Active` / `Customer` / `Inactive` / `Churned`) —
  the coarse lifecycle of the person.
- **Contacts.Priority** (select: `High` / `Medium` / `Low`) — the Qualifier's ICP-fit output.
- **Outreach Batch counters** (`Leads Sourced` / `Leads Reached` / `Replies` / `Signups` /
  `Paid Conversions`) + the **Interactions** log — the per-batch funnel movement.

Read this table as the source of truth for "where does stage X live":

| # | Conceptual stage | Persisted as | Owner |
|---|---|---|---|
| 1 | **Sourced** | `Contacts.Status = Lead`; related to the Batch; `Leads Sourced`++ | Sourcing |
| 2 | **Reached** | Status stays `Lead`; `Leads Reached`++; an Interaction row (Type=Email/Message, Department=bench) | Sequencer (post-approval) |
| 3 | **Replied** | Status stays `Lead`; `Replies`++; an inbound Interaction row | Sequencer / operator |
| 4 | **Qualified** | `Contacts.Priority = High` or `Medium` (set by Qualifier) | Qualifier |
| 5 | **Signed Up** | `Contacts.Status = Active`; `Signups`++; Interaction logged | Pipeline (app database match) |
| 6 | **Paid** | `Contacts.Status = Customer`; `Paid Conversions`++; Interaction logged | Pipeline (app database match) |
| — | **Churned** | `Contacts.Status = Churned` (corroborated by the app database's event log, if present) | Pipeline (app database match) |
| — | **Disqualified** | `Contacts.Priority = Low` + dated Note; `Status → Inactive` **only after operator review** | Qualifier (flag) → operator |
| — | **Nurture** | `Contacts.Status = Lead`, `Priority = Low` — revisit later | Qualifier / Pipeline |

Key consequences:
- **Status is the lifecycle, not the funnel position.** Reached/Replied/Qualified do NOT
  move Status off `Lead` — they're tracked by Priority, the Batch counters, and Interactions.
  Status only advances when the funnel-truth event fires (signup → `Active`, paid → `Customer`).
- **Conversion truth for stages 5–6 (and Churned) comes from the app database**, reconciled by
  the Pipeline agent on email match. The CRM never invents these.
- **Disqualified is never a destructive change.** It sets Priority Low + a note; any Status
  change to `Inactive` waits for operator review, because other departments may have context.
