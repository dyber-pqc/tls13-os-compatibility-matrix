# Changelog

All notable changes to the matrix. Dates are UTC.

## v0.4 — 2026-08-17

**The spreadsheet becomes a repo.** Migrated from the community-draft xlsx to version-controlled
YAML with CI and an interactive site:

- One YAML file per category under `data/` — the source of truth from here on
- `scripts/validate.py`: schema, status vocabulary, required-source and Verified-trail checks,
  run by GitHub Actions on every PR
- `scripts/build.py`: generates the markdown tables in `docs/`, the site dataset, and live
  status badges; CI fails PRs whose generated files are stale
- Interactive GitHub Pages site: full-text search, status filters, per-category views, the
  milestone timeline with a today marker, and a "Verify this row" issue link on every
  unverified row
- Issue forms for verify / correct / add workflows; original spreadsheet preserved in
  `archive/`
- No data changes in this release: 239 rows carried over — 159 high confidence,
  44 needing verification, 0 verified (by design: verification requires a second pair of eyes,
  which is what going public is for)

## v0.3 — 2026-08-17

Deep multi-source verification pass covering roughly 60 open items against vendor primary
sources; most resolved or materially narrowed.

- **Corrected four seeded claims:** Apache 2.4.36 → 2.4.37; Fedora OpenSSL 3.5 crossover at
  43, not 42; Check Point inspection at R81, not R81.20; Oracle 19c gains TLS 1.3 via the
  opt-in next-generation provider from RU 19.32
- Three date conflicts now marked inline where primary sources disagree: Oracle Linux 7
  Extended, RHEL 7 ELS, Amazon Linux 2023
- About 20 items remain flagged, concentrated in appliance management planes and storage

## v0.2 — 2026-08-14

- **Added tabs:** Milestone Timeline, Mobile, Network Appliances, Virtualization and Cloud,
  Enterprise Unix and Mainframe, Embedded and IoT Stacks, Applications and Middleware,
  Verification Methods, Decision Framework
- Expanded Linux, Windows, containers, runtimes and applications to ~200 rows
- Same-day spot checks corrected three seeded claims (OpenSSL release roadmap, NIST IR 8547
  draft status, Windows PQC ship state); a same-day verification pass against vendor primary
  sources resolved or narrowed 19 more open questions and corrected four seeded claims
  (Server 2025 lifecycle months, Windows 10 consumer ESU extension to 2027, IBM i 7.3
  backport, F5 default-off persisting through current releases)

## v0.1 — 2026-08-14

First seed: 8 tabs, about 55 rows.
