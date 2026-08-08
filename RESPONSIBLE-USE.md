# Responsible Use

This document is norms, not law. It tells you what this system is designed for, what it is
explicitly not designed for, and what stays your responsibility no matter what an agent
drafts. It is not legal advice, and the law here differs by jurisdiction — see the note at
the bottom.

---

## What this is for

Targeted, researched, low-volume, human-approved outreach. The system is built around a
person reviewing every batch of drafts before anything goes out, personalizing from real,
verifiable facts about the recipient, and honoring every opt-out permanently. That's the
intended shape of use: a short, well-researched list, real reasons for reaching each person,
and a human in the loop on every send.

## What this is explicitly not for

- Bulk spam. If the plan is "get this in front of as many inboxes as possible," this is the
  wrong tool, and using it that way defeats every safeguard built into it on purpose.
- Scraped or purchased contact lists. `CLAUDE.md`'s never-guess-a-contact-detail rule and
  `rules/06-compliance.md` exist specifically to keep sourcing to verified, public,
  allowlisted addresses.
- Evading spam filters, deliverability defenses, or platform detection. If a channel's terms
  prohibit automated activity, this system is designed to refuse to automate it — see
  `rules/06-compliance.md`'s LinkedIn example. Working around that refusal defeats the point
  of using it.
- Any use that violates a platform's terms of service, or the law in your jurisdiction or
  your recipient's.

## The draft-first gate is load-bearing, not decorative

Every agent in this system produces drafts with zero side effects by default. That gate —
`rules/00-draft-first.md` — is the reason it's safe to let an agent run against a real CRM
and a real contact list at all. If you remove it, disable it, or build an automation that
bypasses the approval step, you are the sender of whatever goes out. The system doesn't
absorb that responsibility for you, and neither does the fact that an AI drafted the message.
You approved the send, or nobody did, and it shouldn't have gone.

## The one-line test

If you're not sure whether you may contact this person — because you don't know their
opt-out status, you're not confident the address is real and current, or you're not sure
your relationship with them creates any legitimate basis to reach out — you may not. Resolve
the uncertainty first, or don't send.

## Not legal advice

`rules/06-compliance.md` encodes specific rules (CAN-SPAM basics, GDPR review gating for
EU/UK contacts, terms-of-service boundaries) as a working default, not as a substitute for
your own legal judgment. Rules on unsolicited commercial contact vary significantly by
country and by recipient location, and they change. If you're doing this for real, at volume,
or in a regulated industry, get real legal advice for your situation before you rely on
anything in this repository to keep you compliant.

## No compliance warranty

Nothing in this repository, including `rules/06-compliance.md`, is legal advice or a
representation that using LeadBench satisfies CAN-SPAM, GDPR, PECR, CASL, platform terms of
service, or any other law or agreement. The rules encode a floor the agents are instructed to
respect, not a ceiling that guarantees compliance. You are the sender of every message you
approve and the controller of every record you store — those obligations attach to you, not
to this template. Consult a qualified professional for your jurisdiction and use case.

## The safety model is instructions, not enforcement

Say this plainly: the draft-first gate and every other safety behavior described in this
repository are instructions given to a language model, not enforced controls. They can fail,
be misinterpreted, or be removed entirely in a fork. Do not rely on them as a control. The
control is you, approving each send.
