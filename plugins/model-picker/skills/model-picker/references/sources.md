# Where this design comes from

Written fresh for this repo. No text was copied.

- **Tiered model routing.** Using small models for volume and large models for judgement is
  common practice across AI vendors, and is behind this repo's `gauntlet` skill
- **Evaluation before switching.** Testing a cheaper model on real examples against a fixed bar
  before moving a workload, as vendors' own evaluation guides advise
- **Private use.** The "strongest model for the bar, not the bulk" rule and the blind comparison
  come from a pilot of the `gauntlet` skill

## Design choices

- **Tiers, not model names,** so the skill stays vendor neutral and does not age with each release
- **Script first,** because the cheapest model call is the one not made
- **Never trust a remembered price.** Prices change, so the skill reads them or asks
- **Limits before price,** because data rules and stakes can rule out a cheaper model regardless
  of saving
