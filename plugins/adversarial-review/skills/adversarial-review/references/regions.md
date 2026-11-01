# Region defaults

Start each profile here, then adjust it to the item. IDs point to [lenses.md](lenses.md) and to
the standards files below. The personal overlay may add a house region or change a default.

## Standards files

| Region | File | Holds |
| --- | --- | --- |
| Global | [standards/global.md](standards/global.md) | ISO, WCAG, NIST, OECD, OWASP, PCI DSS, SOC 2, IFRS, ISSB, GRI, GHG, FATF |
| United States | [standards/us.md](standards/us.md) | FTC, COPPA, CAN-SPAM, GLBA, HIPAA, ADA, 508, SEC, GAAP, FDA, state privacy |
| European Union | [standards/eu.md](standards/eu.md) | GDPR, ePrivacy, AI Act, DSA, Data Act, CRA, NIS2, DORA, UCPD, green claims, CSRD, EAA, GPSR, MDR |
| United Kingdom | [standards/uk.md](standards/uk.md) | UK GDPR, DUAA, PECR, Equality Act, DMCC, CAP Code, Consumer Duty, Online Safety, governance code |
| Australia and New Zealand | [standards/australia-nz.md](standards/australia-nz.md) | Privacy Act, ACL, Spam Act, DDA, Corporations Act, ASIC, ASX, APRA, Essential Eight, AI guidance, TGA, Fair Work |
| Asia Pacific | [standards/asia-pacific.md](standards/asia-pacific.md) | Singapore, Japan, India, South Korea, Hong Kong, China, Malaysia, Philippines |
| Canada | [standards/canada.md](standards/canada.md) | PIPEDA, Quebec Law 25, CASL, Competition Act, Accessible Canada Act |

## Defaults by region

| Region | Spelling and dates | Style bar | Default obligations | Default audiences |
| --- | --- | --- | --- | --- |
| **Global** | The item's own variant, used the same way throughout. ISO dates (2026-11-01) where readers are mixed | `GL-PLAIN`, `sty-translated` | `GL-WCAG` for anything digital | `aud-public`, `aud-vulnerable` |
| **United States** | US English. Month day, year (November 1, 2026) | `US-PLAIN`, `US-SECPLAIN` for disclosures | `US-FTC`, `US-ADA`, `US-STATES`, `US-CANSPAM` for email | `aud-customer`, `aud-regulator`, `aud-legal` |
| **European Union** | The language of each market. UK English for EU English text. Day month year | `EU-STYLE` | `EU-GDPR`, `EU-EPRIV`, `EU-UCPD`, `EU-EAA`, `EU-AIACT` if AI is used | `aud-customer`, `aud-regulator`, `aud-vulnerable` |
| **United Kingdom** | UK English. Day month year (1 November 2026) | `UK-STYLE` | `UK-GDPR`, `UK-DUAA`, `UK-PECR`, `UK-EQ`, `UK-DMCC`, `UK-CAP` | `aud-customer`, `aud-regulator`, `aud-vulnerable` |
| **Australia** | Australian English (UK-based, with -ise). Day month year | `AU-STYLE` | `AU-PRIV`, `AU-ACL`, `AU-SPAM`, `AU-DDA` | `aud-customer`, `aud-regulator`, `aud-vulnerable` |
| **New Zealand** | NZ English (UK-based). Day month year. Te reo Māori terms where the audience expects them | `NZ-PLAIN` | `NZ-PRIV`, `NZ-FTA` | `aud-public`, `aud-customer` |
| **Singapore** | UK English. Day month year | `GL-PLAIN` | `SG-PDPA`, `SG-AIGOV` if AI is used | `aud-customer`, `aud-regulator` |
| **Japan** | Japanese for local readers. Year month day | Local house style | `JP-APPI` | `aud-customer`, `aud-regulator` |
| **India** | Indian English (UK-based). Day month year | `GL-PLAIN` | `IN-DPDP` | `aud-customer`, `aud-regulator` |
| **South Korea** | Korean for local readers. Year month day | Local house style | `KR-PIPC` | `aud-customer`, `aud-regulator` |
| **Hong Kong** | UK English or Traditional Chinese. Day month year | `GL-PLAIN` | `HK-PDPO` | `aud-customer`, `aud-regulator` |
| **Mainland China** | Simplified Chinese. Year month day | Local house style | `CN-CAC` | `aud-regulator`, `aud-customer` |
| **Canada** | Canadian English (US-based with UK -our). English and French where required | `CA-STYLE` | `CA-PIPEDA`, `CA-CASL`, `CA-COMP`, `CA-QC25` for Quebec | `aud-customer`, `aud-regulator` |

**More than one region:** take the union of obligations, the strictest style bar, and add a
local market reviewer for each region with its own language.

**A region not listed:** say so, use the global defaults, and ask the user whether a local expert
should join the panel. Add the region's main laws to the report as registry updates.
