# Contributing

This matrix only works if people who **actually run** these platforms check the rows against
primary sources. That's the whole model: seeded claims, verified in public, one citation per
claim.

## The golden rules

1. **One claim per cell.** If a platform needs a per-feature answer (appliances always do),
   it gets multiple rows, not a mushy single one.
2. **Cite something a stranger can check.** Primary sources (vendor docs, release notes,
   lifecycle pages) beat blogs. Blogs beat nothing, but get `Needs verification`.
3. **Never delete a conflicting claim — record the conflict.** Where two credible sources
   disagree, both values go inline marked `sources conflict`, and status drops to
   `Needs verification`.
4. **Capability ≠ lifecycle.** Support dates are lifecycle facts. `native_tls13` is a
   capability fact. Keep them straight; confusing them is the failure mode this repo exists
   to fix.

## Verifying a row (the most valuable contribution)

A row becomes **Verified** when **two or more contributors** have independently checked it
against a primary source.

1. Pick any unverified row for something you run — the
   [interactive site](https://dyber-pqc.github.io/tls13-os-compatibility-matrix/) has a
   *Verify this row* link on each one, or filter `data/*.yaml` for `status: Needs verification`.
2. Check the claim against the primary source named in the row — and, where possible, against
   a live system (`openssl s_client -connect host:443 -tls1_3 -brief`; see
   [docs/verification-methods.md](docs/verification-methods.md)).
3. Edit the row:
   - correct anything wrong (say what you fixed in the PR description),
   - flip `status` — to `Verified` only if you're the **second** independent checker,
   - append your initials + date to the `caveats` (or `notes`) field, e.g.
     `Verified vs Red Hat lifecycle page, ZK 2026-08-17`.
     The validator **requires** this trail on every `Verified` row.
4. Run the checks (below) and open a PR. One row is a perfectly good PR.

No YAML? [Open a verification issue](../../issues/new?template=verify-row.yml) with your
evidence and someone will land it for you, credited.

## Adding a platform

Copy a row in the closest-matching `data/*.yaml` and fill it in. Notes:

- Statuses are exactly: `Verified`, `High confidence`, `Needs verification`.
- Appliances get **one row per plane or feature** (management, data plane, VPN, …) — a single
  yes/no per box is meaningless and the schema deliberately refuses it (`applies_to` is
  required).
- New category? Add the YAML file, register it in `SCHEMAS`/`ORDER` in
  `scripts/validate.py` and `scripts/build.py`, and mention it in the README. Or just open an
  issue with the data and we'll wire it up.

## Before you push

```bash
pip install -r requirements.txt
python scripts/validate.py   # schema + status rules
python scripts/build.py      # regenerate docs/ and site data
```

CI runs both on every PR (`build.py --check` fails if generated files are stale), so commit
the regenerated `docs/` and `site/*.json` alongside your data change.

## What NOT to do

- Don't edit `docs/*.md` or `site/data.json` by hand — they're generated.
- Don't "verify" a row you seeded yourself; verification means an independent pair of eyes.
- Don't paste vendor marketing. "Supports TLS 1.3" in a datasheet is a *claim*; a release
  note, admin guide, or a live handshake is *evidence*.
- Don't drop the source when you correct a value. A right answer without a citation is a
  future wrong answer.

## Style

- Dates: `YYYY-MM-DD` (or `YYYY-MM` when the day isn't published).
- Plain, specific prose in caveats — write for the stranger triaging an estate at 2am.
- Keep the dry humor if it carries information. ("The single worst lifecycle vs capability
  mismatch found so far" is data.)

## Conduct

Be excellent to each other. Corrections are the product — deliver and receive them about the
data, never the person. Repeated bad-faith behavior gets you banned by the maintainers.
