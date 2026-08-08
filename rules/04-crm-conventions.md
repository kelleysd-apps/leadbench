# Rule 04 — CRM Conventions

This rule is written against the abstract shared-CRM layer (contacts/companies/interactions).
Examples below reference Notion (workspace/hub) and Supabase (app database) only because
they're common, recognizable stand-ins for what "the shared CRM" and "the app database" mean
in practice — not because either is required. Substitute your own CRM and database; the
discipline below doesn't change.

## The shared CRM — SSOT (single source of truth) discipline (workspace-wide)

- **The shared CRM is the SSOT (single source of truth) for people and accounts.** A workspace-level hub contains the
  canonical `Contacts` and `Companies` collections — reference them as `<CRM_CONTACTS_DB>` and
  `<CRM_COMPANIES_DB>` in your own setup. ALL departments use them. LeadBench REFERENCES them
  via relations; never duplicates Contact or Company data inside a bench-owned database.
- **Departmental "people-adjacent" databases are activity/pipeline tables, not contact
  stores.** Other departments may keep their own tracking tables (an interview pipeline, a
  deal pipeline, a support-ticket queue) that *relate* to the shared CRM Contact rather than
  storing identity themselves. LeadBench's Outreach Batches follow the same pattern.
- **LeadBench owns only bench-specific data**: Outreach Batches (`<HUB_BATCHES_DB>`),
  Messaging Library (`<HUB_MESSAGING_DB>`), Active Focus. Don't build bench operations inside
  another department's zone of the workspace.
- Vertical/Focus is always a VALUE (select option or tag), never a new column. Agnostic by
  design.

## CRITICAL — Before creating ANY Contact or Company

**Always search the shared CRM by name first.** Most likely the record already exists.

Specifically:
1. Search `<CRM_CONTACTS_DB>` (Contacts) for the person's name and any name variants (nickname
   forms, maiden/married names, alternate spellings).
2. If another department's pipeline table has a row for this person, check its relation back
   to the shared CRM Contact — that's already the authoritative pointer to the right record.
3. If a Contact exists: ENRICH it (append to Notes, set relations, update Status if you have
   new evidence). Do NOT create a new one.
4. Only create a new Contact if it genuinely doesn't exist anywhere.
5. The same rule applies to Companies (`<CRM_COMPANIES_DB>`).

**Why this rule exists:** if an agent extracts names from a synthesis document without first
checking the existing CRM, it creates duplicate Contacts. The original record is usually the
richer one — accurate Status, already linked into other departments' pipelines — so a
duplicate doesn't just clutter the CRM, someone has to find it and reverse it by hand. The
cost of a search is zero; the cost of a duplicate is real cleanup work every time.

## CRM — operational hygiene

- Archive-first: nothing deleted without explicit operator confirmation. Deprecated rows get
  marked, not removed.
- Adding a NEW select option or RELATION to existing databases may require manual action in
  your CRM's UI — API/MCP integrations often hit an approval gate for schema changes. Flag
  this to the operator with the exact change needed.
- Notes is shared territory across departments — append, never overwrite. Tag your appends
  with a date so future readers know what came from where.

## The app database (reference: Supabase project at `<APP_DB_URL>`)

- Read-only. Funnel-truth tables are operator-configured — see sync/field-map.md for the
  current mapping (signups, contacts, subscription status, subscription events, plans,
  usage/credit ledger, or whatever your product tracks).
- Conversion event = whatever your product database defines as "converted" (e.g. an active
  subscription flag), corroborated by an events/audit table if you have one. Define it once in
  sync/sync-contract.md and reuse that definition everywhere.
- Never invent a price or plan value; read it live from the app database's plans table.
- **Enforce read-only at the credential, not just by convention.** Use a SELECT-only role, an
  anon key with RLS, or a read-scoped MCP connector. Do NOT use a service-role / admin key for
  funnel pulls — it bypasses row-level security and can write/delete, which contradicts this
  rule at the one layer that actually enforces it. (`scripts/pull_funnel_truth.py` reads its
  key from an env var for exactly this reason — never hard-code a credential into the script.)

---

## CRITICAL — Relations + Rollups discipline

Before adding ANY rollup field on a database, confirm the underlying relation is wired
correctly to support it:

1. **The relation must be present ON the database where the rollup will live.**
   If you want a rollup on Contacts, Contacts must have the relation field — not just the
   other side. Check the schema; if the relation is one-way pointing INTO your database
   from elsewhere, you need to convert it to DUAL first.

2. **DUAL conversion via an API/MCP integration may wipe existing data.**
   Converting a one-way relation to DUAL on a relation that has existing one-way values can
   clear those values when done through an automated integration. The native UI usually
   preserves them. Before doing a DUAL conversion through an integration on production data:
   - Count records with the field populated
   - Save the source-of-truth URLs/IDs (export or note them)
   - Have a recovery path identified
   - Re-verify immediately after; expect to repair
   - Prefer the native UI when existing data is at stake

3. **API/MCP fetch ≠ ground truth for relation/rollup display.**
   Empty relations often don't appear in API fetch output. Rollups can render as empty/omitted.
   When confirming "did this work", ask the operator to check the CRM's UI directly.

---

## Interactions log discipline

The `Interactions` table (`<CRM_INTERACTIONS_DB>`) is the workspace's chronological cross-hub
activity log. Every department writes here on every meaningful touchpoint.

### When to create an Interactions row
ANY of the following creates a new row, by ANY department:
- A message is sent (email, DM, call) — log it
- An interview, sales call, or other rich-content touchpoint happens — log the lightweight
  cross-hub row here even if a department-owned record holds the rich content
- A Contact's Status materially changes (Lead → Customer, etc.) — log the cause
- Any meaningful touchpoint that future-you would want to find later

### Required fields on every Interactions row
- **Contact** (relation) — required; this is what makes the row cross-hub
- **Date** — required
- **Type** — required (e.g. Presentation / Note / Email / Call / Message / Meeting /
  Follow-Up / Interview — adapt to your CRM's options)
- **Department** — required — codes who/which-team owned this touch (operator-defined values;
  LeadBench uses whichever tag your CRM assigns to outbound/marketing touches)
- **Internal / External** — set appropriately
- **Outcome** — one-sentence summary

### Optional but encouraged
- **Deal** (relation) — for sales touches
- **Client** (relation) — when the touch is at a company level too
- **Follow-up Required** — checkbox; surfaces in operator review

### Department field is empty by default in templates
By convention, page templates (New Call / Email / Meeting / Presentation) do NOT pre-set
Department. Every interaction requires a conscious Department selection. Why:
- Templates may be used by any department
- An empty default forces the tag; a wrong default silently mis-tags
- Mis-tagged interactions break the cross-hub views

### How Interactions cross-references with department-owned records
Other departments may keep richer records (full notes, segment links, synthesis fields) in
their own database. The Interactions row for that touch is the lightweight cross-hub signal.
Both exist; they cross-reference via the shared Contact. Don't try to merge them.
