# Where this design comes from

Written fresh for this repo. No text was copied from the sources below. The links were read on
1 Nov 2026.

- **[OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html).**
  The four questions: what are we working on, what can go wrong, what will we do about it, did we
  do a good job
- **STRIDE.** Spoofing, tampering, repudiation, information disclosure, denial of service and
  elevation of privilege, a threat list first published at Microsoft. Step 4 asks them in plain
  words
- **[OWASP Top 10 for Large Language Model Applications](https://genai.owasp.org/llm-top-10/).**
  Prompt injection and excessive agency, behind the extra questions for AI agents
- **Risk matrices.** Likelihood times impact, as used in common risk management practice such as
  ISO 31000

## Design choices

- **Plain questions instead of acronyms,** so a non-specialist can run it
- **A 3 by 3 score,** because finer scales give false precision on guesses
- **Rank by risk removed per effort,** so the report leads to action this week
- **Report only.** Active testing needs permission and expertise this skill cannot check
- **Never print a secret,** because a threat model is shared widely and kept for a long time
