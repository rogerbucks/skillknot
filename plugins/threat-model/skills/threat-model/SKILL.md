---
name: threat-model
description: Use when the user asks what could go wrong, wants a security or risk review of a feature, system, process, vendor, AI tool, trip or plan, or is about to launch, buy, connect or share something sensitive. Builds a plain-English threat model - what is worth protecting, who might harm it and how, how likely and how bad - and ranks fixes so the cheapest big wins come first. Reports only; changes nothing.
license: MIT
compatibility: Works with any agent. Needs no tools. Reads files only if the user points to them. Produces a Markdown report.
---

# threat-model: what could go wrong, and what to do first

**Security advice fails in two ways:** a vague "be careful", or fifty findings with no order.
This gives a short, ranked list a non-specialist can act on this week.

**It reports. It never changes settings, runs scans or tests attacks.** Anything active needs
the owner's written permission and a specialist.

**Read the personal overlay at `~/.config/skillknot/threat-model.md` if it exists.** It may set
the rules you must meet, your risk appetite, or the systems you care about most.

```text
1 Scope -> 2 What to protect -> 3 Map it -> 4 Find threats -> 5 Rate -> 6 Fixes -> 7 Report
```

## 1. Scope it in one line

*"The new customer portal: login, payments and the support inbox. Not the internal HR system."*
Name what is out. A model of everything is a model of nothing.

## 2. Name what is worth protecting

List the **assets**: what would hurt to lose, leak or have changed.

| Kind | Examples |
| --- | --- |
| **Data** | Customer records, payment details, health data, passwords, source code, contracts |
| **Money** | Payments, refunds, invoices, account balances |
| **Access** | Admin accounts, keys, the email account that resets all the others |
| **Operations** | The service staying up; a supplier that cannot be replaced quickly |
| **Trust** | Reputation, regulator standing, a key relationship |

## 3. Map how it fits together

Draw or list, in a few lines: **who uses it, what it talks to, where data goes, and where it
crosses a trust boundary** (from the public internet to your system, from you to a vendor, from
a person to an AI agent). Threats cluster at those crossings.

## 4. Find threats with six questions

Walk each crossing and each asset through these:

| Ask | Threat | Typical example |
| --- | --- | --- |
| **Could someone pretend to be someone else?** | Impersonation | Phished password; fake invoice from a "supplier" |
| **Could data or code be changed without anyone noticing?** | Tampering | Edited bank details; a poisoned software package |
| **Could someone deny they did it?** | No audit trail | No log of who approved a payment |
| **Could data leak?** | Disclosure | Public file share; secrets in a repo; an AI tool trained on uploads |
| **Could it be knocked over or locked?** | Denial of service | Ransomware; one supplier outage stops everything |
| **Could someone get more power than they should?** | Elevation | Shared admin login; a helper tool with full access |

**For AI agents and assistants, also ask:**

- **Could text it reads give it orders?** A web page, email or file can hide instructions
  (prompt injection)
- **Can it act without a person seeing?** Sending, paying, deleting or publishing
- **What can it reach?** Every connector and folder is in scope if the agent is fooled

**For people and processes, also ask:** who can be rushed, flattered or frightened into an
exception? Most real losses start with a person, not a computer.

## 5. Rate each threat, simply

Score **likelihood** and **impact** from 1 (low) to 3 (high). Risk is the product, 1 to 9.

- **Likelihood:** has it happened to others like you? Is it easy? Is it already exposed?
- **Impact:** money, harm to people, legal duty, how long to recover
- **Be honest about confidence.** Mark a rating as a guess when you lack facts

## 6. Pick fixes, cheapest big wins first

For each threat rated 4 or more, name **one fix**, its **effort** (S, M, L), and **who** would
do it. Prefer, in this order:

1. **Remove it:** delete the data, close the access, drop the feature
2. **Prevent it:** multi-factor sign-in, least privilege, a second approver for payments
3. **Detect it:** alerts, logs someone actually reads
4. **Recover from it:** tested backups, a written plan, insurance

Then **rank fixes by risk removed per unit of effort.** Small fixes to high risks go first.

## 7. Report

```markdown
# Threat model: customer portal (1 Mar)
**Bottom line:** 2 high risks, both fixable this month for small effort.

| # | Threat | L | I | Risk | Fix | Effort | Owner |
|---|---|---|---|---|---|---|---|
| 1 | Admin login has no second factor | 3 | 3 | 9 | Turn on multi-factor sign-in | S | IT |
| 2 | Support inbox AI can send email unprompted | 2 | 3 | 6 | Require approval to send | S | Ops |

**Accepted risks:** ... (with who accepted them)
**Not covered:** ... (what this did not look at)
```

**Never put a live secret, password or exploit detail in the report.** Name the weakness, not
the key.

## Limits, said plainly

- **A desk review, not a test.** It finds likely gaps. Only testing, with permission, proves them
- **Regulated areas** such as payments, health data and critical infrastructure need a qualified
  specialist to sign off. Say so in the report

Sources and design notes: [references/sources.md](references/sources.md).
