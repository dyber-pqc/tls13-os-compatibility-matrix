# Container Images

> Generated from [`data/container-images.yaml`](../data/container-images.yaml) — edit the YAML, not this file. Regenerate with `python scripts/build.py`.

| Image family | Capable tags | Not capable | System TLS stack | Notes | Status |
|---|---|---|---|---|---|
| debian | bullseye (11), bookworm (12), trixie (13) | stretch (9) and older | OpenSSL 1.1.1 / 3.0 / 3.5 | bullseye leaves free security support 2026-08-31; bullseye-slim is embedded in thousands of derived images | High confidence |
| ubuntu | 18.04 (updated) and later | 16.04 and older | OpenSSL 1.1.1 / 3.x | Stale cached layers can pin pre-1.1.1 packages; rebuild images rather than retagging | High confidence |
| alpine | 3.9 and later | 3.8 and older (LibreSSL era) | OpenSSL 1.1.1 and later | Roughly two years of support per branch; musl-related caveats for some TLS tooling | High confidence |
| redhat/ubi8, ubi9, ubi10 | All | n/a | OpenSSL 1.1.1 / 3.x | Tracks RHEL content and lifecycle | High confidence |
| amazonlinux | 2023 | 2 (default stack) | OpenSSL 3.x vs 1.0.2 default | amazonlinux:2 is past end of life as of 2026-06-30 | High confidence |
| Chainguard / Wolfi images | All (rapid rebuild cadence) | n/a | Current OpenSSL 3.x | Minimal, continuously rebuilt; track OpenSSL 3.5 adoption for PQC (confirm current) | *Needs verification* |
| distroless (gcr.io) | n/a (no shell, minimal userland) | n/a | Application runtime provides TLS | Static and base variants carry no OpenSSL; the bundled runtime (Go, Java, Node) sets the TLS ceiling | High confidence |
| busybox / scratch | n/a | n/a | None | No TLS stack at all; the application binary brings everything. Audit the binary's build, not the image | High confidence |
| Language and runtime images (python, node, golang, eclipse-temurin) | Depends on the bundled runtime, not only the base OS |  | Bundled runtime stack | Static Go binaries carry Go's own TLS stack; the base image is irrelevant to their TLS ceiling. Java and Node images are governed by the bundled JDK or Node line | High confidence |
