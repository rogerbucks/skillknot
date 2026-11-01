# Company lifecycle and industry sweep

The same item faces different attackers at different moments. A privacy notice at launch is read by
customers. The same notice in a sale is read by the buyer's counsel. Use this at Stage 1, after
the region defaults, to add what the item's **phase** and **industry** bring. IDs point to
[lenses.md](lenses.md) and the [standards files](regions.md).

## How to use it

1. **Name the phase** the organisation is in, and the phase the item serves, if different
2. **Name the industry,** or two if the item spans them
3. **Add the rows below** for that phase and that industry to the profile
4. **Say what you added and why** in the profile, so the user sees it at the panel gate
5. **If a row names a rule not in the registry,** add it as *added this run*, with its official
   link, and list it under *Registry updates* in the report

## Phases

| Phase | Typical items | Extra audiences | Extra lenses | Extra standards and obligations | Extra experts |
| --- | --- | --- | --- | --- | --- |
| **Formation** | Founder agreements, constitution, first policies, brand | Co-founders, early hires, registrar | `len-legal`, `len-ops` | Company law of the region (`AU-CORP` and peers), IP ownership, employment terms (`AU-FWO` and peers) | Corporate counsel, IP counsel |
| **Funding** | Pitch decks, data rooms, term sheets, grant bids | Investors, due-diligence teams, grant assessors | `len-hostile`, `len-finance`, `len-competitor` | Securities and offer rules (`US-SEC`, `AU-ASIC`), forecast claims, grant conditions | Investor proxy, financial controller |
| **Launch** | Product pages, terms, privacy notice, pricing, ads | First customers, media, regulators | `len-consumer`, `len-privacy`, `len-access`, `len-brand` | Consumer law (`US-FTC`, `EU-UCPD`, `UK-DMCC`, `AU-ACL`), privacy, accessibility (`GL-WCAG`), marketing (`UK-CAP`, spam laws), product safety (`EU-GPSR`) | Target-audience proxy, accessibility specialist, privacy officer |
| **Growth** | Hiring packs, sales playbooks, vendor contracts, security questionnaires | Staff, enterprise buyers, suppliers | `len-security`, `len-ops`, `len-ethics` | `GL-ISO27001`, `GL-SOC2`, `GL-PCI` if payments, employment law, `GL-UNGP` and modern slavery for suppliers | Security reviewer, operations lead |
| **Cross-border** | Localised sites, transfer agreements, local terms | Local customers, local regulators | `len-culture`, `len-privacy`, `len-legal` | Every new region's defaults in [regions.md](regions.md), data transfer rules (`EU-PRIVHUB`), sanctions and export controls | Local market reviewer per region, regulatory counsel per region |
| **Regulated scale** | Board papers, risk registers, AI policies, resilience plans | Board, auditors, prudential regulators | `len-legal`, `len-ai`, `len-security` | `GL-ISO31000`, `GL-NISTAI`, `EU-AIACT`, `EU-NIS2`, `EU-DORA`, `AU-APRA` | AI governance lead, internal auditor |
| **Public listing** | Prospectus, annual report, continuous disclosure, ESG report | Investors, analysts, exchange, media | `len-finance`, `len-esg`, `len-hostile` | `US-SEC`, `AU-ASX`, `UK-CGC`, `GL-IFRS` or `US-GAAP`, `GL-ISSB`, `EU-CSRD`, `GL-GHG` | Securities counsel, sustainability assurer, analyst proxy |
| **Merger or sale** | Information memorandum, disclosure letter, integration plan, staff notices | Buyer's counsel, staff, competition regulator | `len-legal`, `len-hostile`, `len-ops` | Competition and merger rules, takeover rules, staff consultation duties, data transfer in a sale | M&A counsel, integration lead, staff proxy |
| **Restructure or distress** | Redundancy notices, creditor letters, turnaround plans | Staff, creditors, unions, administrators | `len-ethics`, `len-legal`, `len-hostile` | Insolvency law and director duties (`AU-CORP` and peers), employment consultation, continuous disclosure | Insolvency counsel, employee relations lead |
| **Wind-down or exit** | Closure notices, data deletion plans, final accounts | Customers, regulators, liquidators | `len-privacy`, `len-legal`, `len-consumer` | Record retention, data deletion (`EU-GDPR` and peers), refund and guarantee duties (`AU-ACL` and peers) | Records manager, privacy officer |

## Industries

| Industry | Extra audiences | Extra standards and obligations | Extra experts |
| --- | --- | --- | --- |
| **Financial services** | Prudential and conduct regulators, vulnerable customers | `UK-FCACD`, `AU-ASIC`, `AU-APRA`, `EU-DORA`, `US-GLBA`, `SG-MASTRM`, `GL-FATF`, `GL-PCI` | Conduct risk specialist, AML officer |
| **Health and life sciences** | Patients, clinicians, health regulators | `US-HIPAA`, `US-FDA`, `AU-TGA`, `EU-MDR`, health-claim advertising rules | Clinical safety officer, health privacy lead |
| **Technology, SaaS and AI** | Developers, enterprise security teams | `GL-OWASP`, `GL-SOC2`, `GL-ISO27001`, `GL-ISO42001`, `EU-AIACT`, `EU-CRA`, `EU-DATA`, `EU-DSA` | Security reviewer, AI governance lead |
| **Retail and consumer goods** | Shoppers, consumer regulators, reviewers | `EU-GPSR`, `EU-GREEN`, `UK-DMCC`, `AU-ACL`, `US-FTC`, `GL-PCI` | Consumer law counsel, product safety lead |
| **Energy, resources and industrials** | Communities, environment regulators, unions | `GL-GHG`, `GL-ISSB`, `EU-NIS2`, work health and safety law, environmental approvals | Safety engineer, environmental assurer |
| **Public sector** | Citizens, ministers, auditors-general | `US-508`, `US-PLAIN`, `UK-STYLE`, `AU-STYLE`, `NZ-PLAIN`, `CA-ACA`, freedom-of-information duties | Plain-language editor, public law counsel |
| **Education** | Students, parents, accreditation bodies | `US-COPPA`, `UK-OSA`, child safety codes, `GL-WCAG` | Child safety lead, accessibility specialist |
| **Media, telecoms and platforms** | Users, advertisers, content regulators | `EU-DSA`, `UK-OSA`, `UK-CAP`, `EU-EPRIV`, `UK-PECR` | Trust and safety lead, advertising standards reviewer |
| **Not-for-profit and charity** | Donors, beneficiaries, charity regulators | Fundraising codes, charity reporting rules, `GL-UNGP` | Governance reviewer, donor proxy |
| **Professional services** | Clients, professional bodies | Professional conduct rules, confidentiality, conflict checks | Professional standards reviewer |

## Gaps this sweep found in the registry

These rows are named above but are not yet in the standards files, because each needs one law per
region. A review that needs one adds it *this run* and reports it as a registry update.

- Employment and staff consultation law, outside Australia
- Insolvency and director-duty law, outside Australia
- Competition and merger control, and takeover rules
- Sanctions and export controls
- Work health and safety, and environmental approvals
- Child safety codes outside the UK, and charity fundraising codes
- Professional conduct rules for law, accounting and other regulated professions
