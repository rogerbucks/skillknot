# Lenses, audiences, styles and experts

Pick from these at Stages 1 and 2. Add your own in the personal overlay at
`~/.config/skillknot/adversarial-review.md`. Region defaults are in [regions.md](regions.md).

## Audiences

| ID | Audience | What they want | How they attack |
| --- | --- | --- | --- |
| `aud-exec` | Executives and boards | The decision, the cost, the risk, in one page | Skip to the ask. Distrust anything without a number |
| `aud-public` | The general public | To understand fast, on a phone | Stop reading at the first unclear line |
| `aud-customer` | Customers and users | What it means for them, what to do next | Look for the catch, the fee, the opt-out |
| `aud-regulator` | Regulators and auditors | Evidence the obligation is met | Read every claim as a promise to be tested |
| `aud-investor` | Investors and analysts | Material facts, consistency with past statements | Compare with the last report |
| `aud-staff` | Employees | What changes for them, and why | Read between the lines for job risk |
| `aud-technical` | Engineers and specialists | Precision, edge cases, working examples | Try the example. Hunt the edge case |
| `aud-legal` | Counsel, the other side's counsel | Obligations, ambiguity, liability | Read each word for the worst meaning |
| `aud-media` | Journalists | A headline, a contradiction, a quote | Lift one line out of context |
| `aud-vulnerable` | People in hardship, with disability, low literacy or a second language | Plain, accessible, respectful text | Cannot use what they cannot read or reach |
| `aud-child` | Children and their parents | Safety, age-fit language | Parents read for harm, not intent |

## Language styles

| ID | Style | Bar |
| --- | --- | --- |
| `sty-plain` | Plain language | Readers find, understand and use it first time. See `GL-PLAIN` |
| `sty-exec` | Executive | Bottom line first, one idea per paragraph, decisions and owners named |
| `sty-formal` | Formal or legal | Defined terms used the same way every time, no loose synonyms |
| `sty-technical` | Technical | Exact, tested, consistent terms, examples that run |
| `sty-marketing` | Persuasive | Every claim provable. No hidden conditions |
| `sty-gov` | Public sector | The region's government style manual |
| `sty-inclusive` | Inclusive | No needless gendered, ableist or cultural assumptions |
| `sty-variant` | Spelling variant | US, UK, Australian or Canadian English, applied the same way throughout |
| `sty-translated` | For translation | Short sentences, no idiom, one meaning per word |

## Expectations

Check the item meets what its form promises:

- **Structure:** a report has a summary, a policy has scope and owner, a contract has defined terms
- **Evidence:** every number has a source and a date
- **Action:** the reader knows what to do, by when, and who to ask
- **Consistency:** with the organisation's earlier statements, and within the item
- **Format:** the length, channel and file type the audience will accept
- **Accessibility:** usable by people with disability. See `GL-WCAG` and the region's law

## Lenses

A lens is one way of attacking. A user may ask for any of these by name, or for one not listed.

| ID | Lens | Asks |
| --- | --- | --- |
| `len-hostile` | Hostile reader | How could this be misread, resented or used against us? |
| `len-legal` | Legal and regulatory | Which obligation does each line touch, and is it met? |
| `len-privacy` | Privacy | What personal data is used, on what basis, with what notice? |
| `len-security` | Security | What could an attacker learn or do from this? |
| `len-ai` | AI governance | Is AI use disclosed, risk-assessed and overseen? |
| `len-access` | Accessibility | Can everyone perceive, operate and understand it? |
| `len-consumer` | Consumer fairness | Is anything misleading, hidden or unfair? |
| `len-finance` | Financial | Do the numbers add up, reconcile and match the standard? |
| `len-esg` | Sustainability and ESG | Are the claims measured, or greenwash? |
| `len-brand` | Brand and reputation | Does it sound like us, and would we defend it in public? |
| `len-plain` | Plain language | Could the audience use it first time? |
| `len-culture` | Cultural and local | Does it land in each region, language and culture? |
| `len-ethics` | Ethics | Who could be harmed, even if it is lawful? |
| `len-ops` | Operational | Can this actually be done, by whom, with what? |
| `len-competitor` | Competitor | How would a rival exploit or rebut this? |
| `len-premortem` | Pre-mortem | It failed in a year. Why? |

## Expert roster

Each expert holds one or more lenses. Name them by role, never as a real person.

| Expert | Lenses | Bring in when |
| --- | --- | --- |
| Hostile reader | `len-hostile` | Always |
| Domain expert | the item's field | Always |
| Regulatory counsel, per jurisdiction | `len-legal`, `len-consumer` | Obligations in scope |
| Privacy officer | `len-privacy` | Personal data is collected, used or mentioned |
| Security reviewer | `len-security` | Systems, data flows or credentials appear |
| AI governance lead | `len-ai`, `len-ethics` | AI builds, decides or writes any part |
| Accessibility specialist | `len-access` | Public, customer or staff facing |
| Plain-language editor | `len-plain` | Read by the public, customers or a second-language audience |
| Financial controller or auditor | `len-finance` | Numbers, forecasts or financial claims |
| Sustainability assurer | `len-esg` | Environmental or social claims |
| Brand and communications lead | `len-brand`, `len-hostile` | External or all-staff |
| Local market reviewer, per region | `len-culture` | More than one region or language |
| Ethicist | `len-ethics` | People could be harmed, even lawfully |
| Operations lead | `len-ops` | The item commits people to act |
| Competitor strategist | `len-competitor` | Pitches, launches, pricing, bids |
| Target-audience proxy | the main audience | Always worth one seat on a customer or public item |
| Pre-mortem facilitator | `len-premortem` | Plans, strategies, launches |
