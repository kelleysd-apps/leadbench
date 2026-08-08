# Enrichment Sources — the free-first waterfall pattern

LeadBench's own enrichment is the default; a paid provider is gap-fill only, and only ever
operator-approved. For most verticals, free public sources beat a paid provider on data
that's already published — the free waterfall just has to be run consistently.

**This file is the pattern, not a source list.** The categories below are generic on purpose.
List your own vertical's actual sources — the directories, registries, and page types where
your specific ICP publishes contact-adjacent information — in `brain/vertical-profile.md`.
Do not treat any example in this file as a source that applies to every market; it doesn't.

## Email waterfall (stop at the first verified hit)

Run automatically on every lead, no operator gate, until a verified address is found or the
waterfall is exhausted:

1. **A public professional directory relevant to your vertical** — a licensing board roster,
   an industry association member list, a marketplace or platform profile, or any other
   authoritative "who's who" surface your ICP appears on. Whatever that surface is for your
   market, put it first. List it in `brain/vertical-profile.md`.
2. **Company or organization "team" / "about" / "contact" pages** (fetch + extract). Many
   organizations publish direct contact emails. Handle common obfuscation patterns (`name
   [at] domain.com`, `name (at) domain dot com`) when de-obfuscating.
3. **Public registries and directories** — company registries, professional licensing
   boards, chamber-of-commerce-style directories, or any public-record source specific to
   your vertical that confirms an address or at minimum a domain.
4. **A paid enrichment provider — gap-fill ONLY, operator-run in chat, with explicit
   credit-cost confirmation before every call.** Never called unattended. See "Paid provider
   as last-resort HITL" below.

Only write an address found in a public source and validated against your focus's domain
allowlist (defined in `active-focus/focus.md` or `brain/vertical-profile.md`, per your
market). **Never pattern-generate an address to have something to send to** — this is
prohibited outright, not just discouraged. See `rules/03-data-privacy.md` and
`CLAUDE.md`'s rule 3.

## Profile / metrics / affiliation

- **A public track-record source relevant to your vertical** (e.g. a portfolio, a project or
  case-study listing, a review or ratings page, a public work history). Use these to confirm
  the lead is a real fit and to build personalization hooks grounded in fact.
- **Verified employment/affiliation history sources** — a professional network profile, a
  registry entry, or any source that independently confirms current role and organization.
  This doubles as affiliation QA: if only an out-of-ICP affiliation surfaces, the lead was
  mis-sourced.
- **A public filing, disclosure, or budget-signal source specific to your vertical**, where
  applicable — these can double as a personalization hook and a budget-fit signal. Attach
  findings to Notes, not to a new schema field.

## Title / links / social

- The organization's own team or leadership page, plus whatever verified-affiliation source
  you used above, for exact role/title and canonical profile links.
- A professional network profile — write it only on a clearly-matching profile. Never guess
  which of several same-named profiles is the right one.

## Commercial / budget signal

For each lead, a targeted web search for evidence they have decision power or budget
authority (founder, co-founder, executive role, an active commercial venture, an advisory
seat) is the strongest "would pay" signal available for free. If found, record it in Notes
and bias Priority upward per `brain/icp.md`. There is rarely a dedicated connector for this —
plan on web search plus the organization's own announcements.

## Why a paid provider finds things the free waterfall can't

If you connect a paid enrichment provider, understand what it actually adds over public
sources, so you know when gap-fill is worth the spend and when it won't help:

1. **A private, crowd-sourced contact graph.** When the provider's own users connect their
   inboxes/CRMs, addresses they've emailed get ingested — so an address can be in the
   provider's database even though it appears on no public page. This is real and you cannot
   replicate it with public sourcing.
2. **SMTP-verification infrastructure.** The provider derives a likely address from a known
   domain pattern, then pings the mail server to confirm deliverability — something most
   sourcing environments can't do (outbound SMTP verification is commonly blocked).

Deriving a guessed address yourself, without that infrastructure, is unreliable and
prohibited by rule regardless of reliability — see `rules/03-data-privacy.md`. This is exactly
why a paid provider, if you use one, is the gated, operator-approved last resort — never a
shortcut the free waterfall reaches for on its own.

## Paid provider as last-resort HITL (gap-fill)

- Free waterfall finds no email → set the outreach stage to a **"Needs paid gap-fill"**
  status (not an automatic hold). This is the operator's approval queue.
- An unattended scheduled runner NEVER calls a paid provider — credit-cost confirmation is
  impossible unattended, and `CLAUDE.md` rule 4 prohibits spending without approval regardless.
- The operator reviews the gap-fill queue, and when ready says "run gap-fill for these" in
  chat. The provider runs with explicit credit-cost confirmation. Found → write the email and
  return to flow. Not found → hold/drop.

## Fields populated

Whatever your CRM schema calls them — typically: Email, Role/Title, a professional-profile
link, a commercial-signal flag, and a dated Notes line summarizing what enrichment found
(topic/focus, verified affiliation, funding or budget signal, source links). Affiliation
check: if only an out-of-ICP affiliation surfaces, move the lead to hold/drop rather than
sending to a mis-sourced contact.
