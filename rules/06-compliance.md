# Rule 06 — Compliance

This rule binds every agent that touches sourcing, drafting, or sending. It is not guidance
for the human operator to keep in mind — it is a set of hard constraints an agent must
enforce on its own output before that output is ever presented for approval. If an agent
produces a draft or a sourcing result that violates one of these, that is a bug in the
agent's behavior, not a judgment call left to the operator to catch.

---

## Every outbound template carries a working opt-out and truthful headers

- Every email template must include a real, working opt-out mechanism (an unsubscribe link
  or a plain-text reply-to-opt-out instruction) and the sender's true identity and physical
  address in the footer, per CAN-SPAM. `<SENDER_EMAIL>` and `<SENDER_POSTAL_ADDRESS>` must
  resolve to real, working values before any template is used — a placeholder left unfilled
  is a template that isn't ready to send.
- Subject lines and "From" fields must accurately describe the message. No deceptive subject
  lines, no impersonation, no disguising the commercial nature of the message.
- **Why:** this is the floor set by CAN-SPAM (and comparable regimes elsewhere) for
  commercial email. It exists independent of volume — even a single email needs a real way to
  opt out and truthful headers. An agent that drafts a template without a working opt-out has
  produced something that cannot legally be sent, and presenting it for approval as if it
  could be is a failure to catch that before the operator has to.

## A suppression list is checked before every send, and honored permanently

- Before any send (individual or batch), the agent must check the intended recipient against
  the suppression list and refuse to send to anyone on it.
- Once someone opts out, unsubscribes, or is added to the suppression list by any means, that
  suppression is permanent. It is never re-added to an active sequence, never re-contacted
  under a different campaign or segment tag, and never silently dropped from the list to
  "clean it up" for reuse.
- **Why:** an opt-out that doesn't stick isn't an opt-out. Re-contacting someone who
  unsubscribed is both a compliance failure and the fastest way to convert a mildly annoyed
  recipient into a spam complaint, which damages deliverability for every future recipient.

## EU/UK contacts are gated behind explicit operator review

- An agent must not draft or approve outreach to a contact identified as based in the EU or
  UK without first flagging that contact for explicit operator review.
- GDPR's "legitimate interest" basis for unsolicited B2B contact is a case-by-case legal
  analysis — whose interests, what relationship, what the recipient would reasonably expect
  — not something an agent can determine from a CRM record. Treat it as unresolved until a
  human resolves it, every time.
- **Why:** legitimate interest is an analysis, not a default. An agent has no way to weigh
  the specific facts GDPR requires, and guessing wrong here carries real regulatory exposure
  that the operator, not the agent, bears.

## No sourcing from a source whose terms prohibit scraping

- Before an agent sources contact or company data from any website, database, or platform,
  it must confirm that source's terms of service permit the extraction method being used. If
  the terms prohibit scraping, automated collection, or bulk export, that source is off
  limits for sourcing, full stop — there is no workaround an agent may reach for instead.
- **Why:** scraping in violation of a platform's terms is both a contract violation and,
  depending on jurisdiction and method, can carry legal exposure beyond contract. "The data
  was technically accessible" is not the same as "the terms allowed taking it this way."

## A stated data-retention limit for sourced contact records

- Contact records sourced but never converted to an active relationship (no reply, no
  qualified interest, no ongoing contact) must not be retained indefinitely. Set and document
  a retention limit for your focus in `active-focus/focus.md` or `brain/icp.md`, and have the
  Pipeline agent flag records that have aged past it for archival or deletion review.
- **Why:** holding personal data with no ongoing purpose and no defined endpoint is both bad
  practice and, for EU/UK-linked data specifically, a separate GDPR obligation on top of the
  legitimate-interest question above. A retention limit that's never enforced isn't a limit.

## No automation of any channel whose terms of service forbid it

- If a channel's terms of service prohibit automated activity, no agent may automate that
  channel — not sourcing from it, not messaging through it, not any workflow step that
  interacts with it programmatically.
- **LinkedIn is the specific, named example.** LinkedIn's terms of service prohibit automated
  activity on the platform, including automated connection requests, automated messaging, and
  automated scraping of profiles or search results. No agent in this system may log into
  LinkedIn, scrape it, or send anything through it. If LinkedIn is part of your outreach plan,
  it is a manual, human channel: the agent may draft a connection note or message for the
  operator's own review, but the operator sends it by hand, from their own logged-in session,
  never through an agent action.
- **Why:** automating a channel against its own terms risks the account behind it — a
  platform that detects automation can flag, restrict, or permanently ban the account, which
  is a much larger loss than whatever the automation saved. Naming LinkedIn specifically
  because it's the channel most likely to be assumed as automatable by habit; it isn't, here.
