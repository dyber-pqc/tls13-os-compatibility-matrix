# TLS 1.3 / PQC Readiness Matrix

[![Validate data](https://github.com/dyber-pqc/tls13-os-compatibility-matrix/actions/workflows/validate.yml/badge.svg)](https://github.com/dyber-pqc/tls13-os-compatibility-matrix/actions/workflows/validate.yml)
![Rows](https://img.shields.io/endpoint?url=https%3A%2F%2Fdyber-pqc.github.io%2Ftls13-os-compatibility-matrix%2Fbadge-rows.json)
![Verified](https://img.shields.io/endpoint?url=https%3A%2F%2Fdyber-pqc.github.io%2Ftls13-os-compatibility-matrix%2Fbadge-verified.json)
![Needs verification](https://img.shields.io/endpoint?url=https%3A%2F%2Fdyber-pqc.github.io%2Ftls13-os-compatibility-matrix%2Fbadge-open.json)
[![License: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-lightgrey.svg)](LICENSE)

**What can negotiate TLS 1.3 today — and what never will.**

Hybrid post-quantum key exchange (X25519MLKEM768) is specified for **TLS 1.3 only**, and the
IETF has frozen TLS 1.2. Every post-quantum migration therefore starts with the same inventory
question: *which of my platforms can even speak TLS 1.3?* The answers exist, but scattered
across vendor docs one slice at a time — and popular secondary sources contradict each other.
This repo builds the consolidated answer **in public, with a primary source attached to every
claim**.

### [Browse the interactive matrix →](https://dyber-pqc.github.io/tls13-os-compatibility-matrix/)

Searchable, filterable, with a live migration timeline. Or read the
[generated markdown tables](docs/README.md) right here on GitHub.

---

## The 30-second version

| Tier | Meaning | Examples | Cost |
|---|---|---|---|
| **A** | Capable & on by default | RHEL 8+, Ubuntu 20.04+, Server 2022+, Windows 11 | Config hygiene |
| **B** | Capable after a patch or config flip | Ubuntu 18.04 (old patch level), PAN-OS 11 mgmt, old `ssl_protocols` lines | Routine maintenance |
| **C** | Capable only via a supported major upgrade | RHEL 7 to 8 (Leapp), Win10 to 11 on eligible hardware | Upgrade project |
| **D** | Never capable — migrate or replace | **Windows Server 2019 (supported to 2029!)**, RHEL 6, Amazon Linux 2, HP-UX, sub-14.x F5s | Capital refresh |

The trap this matrix exists to catch: **support lifecycle is not capability.** Windows Server
2019 is vendor-supported until 2029 and will *never* speak TLS 1.3. Windows 10 IoT Enterprise
LTSC 2021 is supported until **2032** — past both US federal PQC deadlines — and is permanently
incapable. Lifecycle-based planning misses these; capability-based planning catches them.

## Hall of lifecycle-vs-capability shame

1. **Windows 10 IoT Enterprise LTSC 2021** — supported to 2032-01-13, never TLS 1.3. Outlives both EO 14412 PQC deadlines.
2. **Windows Server 2019 domain controllers** — cap LDAPS at TLS 1.2 *for the entire forest* until 2029.
3. **F5 BIG-IP** — TLS 1.3 capable since v14, still shipped **disabled by default** through 21.x.
4. **vSphere 8.0 U3** — the stack does TLS 1.3, but port 443 stays at 1.2 because the FIPS module wasn't certified for it. FIPS validation, not capability, is the real gate — and it will be for PQC too.

## What's in the box

```
data/        <- the matrix: one YAML file per category (THE source of truth)
docs/        <- generated markdown tables (don't edit; run build.py)
site/        <- the interactive site (GitHub Pages)
scripts/     <- validate.py, build.py, convert_xlsx.py (provenance)
archive/     <- the original community-draft spreadsheet this grew from
```

16 categories, 239 rows: [Linux](docs/linux.md) · [Windows](docs/windows.md) ·
[macOS & BSD](docs/macos-bsd.md) · [Mobile](docs/mobile.md) ·
[Network appliances](docs/network-appliances.md) ·
[Virtualization & cloud](docs/virtualization-cloud.md) ·
[Enterprise Unix & mainframe](docs/enterprise-unix-mainframe.md) ·
[Container images](docs/container-images.md) · [Embedded & IoT](docs/embedded-iot.md) ·
[Libraries & runtimes](docs/libraries-runtimes.md) ·
[Applications & middleware](docs/applications-middleware.md) ·
[Milestone timeline](docs/timeline.md) · [Decision framework](docs/decision-framework.md) ·
[Verification methods](docs/verification-methods.md) ·
[PQC forward view](docs/pqc-forward-view.md) · [Sources](docs/sources.md)

## Status legend — read this before trusting anything

| Status | Meaning |
|---|---|
| **Verified** | Checked by **two or more contributors** against a primary source. *No row carries this yet — that's where you come in.* |
| **High confidence** | Seeded from a primary source, awaiting independent review |
| **Needs verification** | Seeded with a known open question, stated in the row |

Where two credible sources disagree, both values appear inline marked *sources conflict*.
**Nothing here is authoritative until its status says Verified.**

## How to contribute (it's designed to be easy)

Pick a block that matches **what you actually run**, check each row against the primary source
named in it, and open a PR that corrects or confirms it. One row is a great PR.

1. Edit the row in the relevant `data/*.yaml`
2. Flip `status`, add your initials + date to `caveats`/`notes`
3. `python scripts/validate.py && python scripts/build.py`
4. Open the PR — CI re-checks everything

Full details in [CONTRIBUTING.md](CONTRIBUTING.md). Not a YAML person? Just
[open a verification issue](../../issues/new?template=verify-row.yml) — the interactive site
has a *"Verify this row"* link on every unverified row.

**Wanted:** OT/ICS, storage & backup appliances, session border controllers, SaaS TLS floors,
telecom core, Arista/Aruba/MikroTik depth, RTOS ecosystems, NAS firmware. If you run it, that
block is yours. Automating the lifecycle-date columns against the
[endoflife.date](https://endoflife.date) API is an open project — say so in an issue if you
want it.

## Quick verification cheatsheet

```bash
# Does this service actually negotiate TLS 1.3?
openssl s_client -connect host:443 -tls1_3 -brief

# Can it do hybrid PQC key exchange? (also a middlebox stress test)
openssl s_client -connect host:443 -tls1_3 -groups X25519MLKEM768
```

More in [Verification methods](docs/verification-methods.md) — including why you must scan
**per listener, not per host**, and why version strings lie on enterprise distros.

## License

- **Data & docs** (`data/`, `docs/`, `site/data.json`): [CC BY 4.0](LICENSE)
- **Code** (`scripts/`, `site/index.html`): [MIT](LICENSE-CODE)

Prior art this builds on (rather than duplicating): Microsoft's Schannel docs, Cisco's product
matrix, Wikipedia's TLS implementation comparison, endoflife.date. See [Sources](docs/sources.md).
