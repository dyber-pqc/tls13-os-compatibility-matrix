# Milestone Timeline

> Generated from [`data/timeline.yaml`](../data/timeline.yaml) — edit the YAML, not this file. Regenerate with `python scripts/build.py`.

| Date | Event | Why it matters | Status |
|---|---|---|---|
| 2018-09 | OpenSSL 1.1.1 released | TLS 1.3 arrives for the OpenSSL world; the dividing line most Linux rows reduce to | High confidence |
| 2023-09-11 | OpenSSL 1.1.1 upstream EOL | Distros carrying 1.1.1 (RHEL 8, Ubuntu 20.04, Debian 11) continue their own patching; upstream fixes end | High confidence |
| 2024-06-30 | RHEL 7 and CentOS 7 end; Debian 10 LTS ends | Three of the largest below-the-line server populations leave free support the same day | High confidence |
| 2024-10-31 | SLES 12 general support ends | Below-the-line SUSE estates move to LTSS or migrate | High confidence |
| 2025-05-31 | Ubuntu 20.04 standard support ends | A capable release, but ESM-only from here | High confidence |
| 2025-07-21 | Intel Clear Linux discontinued (final build 43800) | A rolling, always-current distro exits without a successor; migration line item | High confidence |
| 2025-10-02 | vSphere 7.x general support ends | Below-the-line hypervisor management planes lose support | High confidence |
| 2025-10-14 | Windows 10 support ends; Exchange 2016 and 2019 end | The largest below-the-line client population goes unsupported; ESU does not add TLS 1.3 | High confidence |
| 2025-12-31 | HP-UX 11i v3 support ends | A permanently incapable platform exits support entirely | High confidence |
| 2026-06-10 | Debian 12 regular support ends | Bookworm moves to LTS; upgrade target shifts to 13 | High confidence |
| 2026-06-30 | Amazon Linux 2 end of life | A very large partial-capability cloud population goes unsupported | High confidence |
| 2026-08-31 | Debian 11 LTS ends | The last free support for a 1.1.1-era Debian; also embedded in countless container images | High confidence |
| 2026-09-07 | OpenSSL 3.0 upstream security fixes end | The stack under Ubuntu 22.04/24.04, Debian 12, RHEL 9, AL2023 loses upstream fixes; vendors carry on alone | High confidence |
| 2026-10-13 | Windows Server 2022 mainstream ends; Server 2012 and 2012 R2 final ESU | First capable Windows Server enters extended; final patches for the 2012 line | High confidence |
| 2027-01-12 | Windows Server 2016 extended support ends; Windows 10 Enterprise LTSC 2021 ends | Two incapable lines exit; forcing function for migration budgets | High confidence |
| 2027-04 | Ubuntu 22.04 standard support ends | Capable, moves to ESM | High confidence |
| 2027-10-12 | Windows 10 consumer ESU ends (extended from 2026 in June 2026) | The consumer tail of the largest incapable client population loses its last patches | High confidence |
| 2027-10-31 | SLES 12 LTSS ends (LTSS Core continues to 2030) |  | High confidence |
| 2028-03-15 | Amazon Linux 2023 end of life per the AWS support statement (trackers list 2029-06; sources conflict) | The default AWS distro generation turns over | *Needs verification* |
| 2028-04 | Ubuntu 18.04 ESM ends | Final paid patches for a huge transitional population | High confidence |
| 2028-06-30 | RHEL 7 ELS ends (some trackers cite 2029-05; sources conflict) | Final paid patches for the largest below-the-line server population | *Needs verification* |
| 2028-06-30 | Debian 12 LTS ends |  | High confidence |
| 2028-10 | Windows 10 commercial ESU final year ends | Truly the end of the Windows 10 line | High confidence |
| 2029-01-09 | Windows Server 2019 extended support ends | The flagship supported-but-incapable platform finally exits; any 2019 still serving TLS in 2029 spent a decade below the line | High confidence |
| 2029-04 | Ubuntu 24.04 standard support ends |  | High confidence |
| 2029-05-31 | RHEL 8 maintenance ends | Last 1.1.1-era RHEL exits standard lifecycle | High confidence |
| 2030-04-08 | OpenSSL 3.5 LTS support ends | The first PQC-capable LTS completes its run; successors carry hybrids forward | High confidence |
| 2030-12-31 | EO 14412: FIPS 140-3 validated PQC key establishment deadline (US federal, FAR flow-down) | Every federal-touching TLS endpoint needs validated ML-KEM by here, and TLS 1.3 is its prerequisite. Contractors inherit via flow-down | High confidence |
| 2031-10-14 | Windows Server 2022 extended support ends |  | High confidence |
| 2031-12-31 | EO 14412: PQC digital signature deadline | Certificate chains and signing infrastructure follow key establishment by one year | High confidence |
| 2032-01-13 | Windows 10 IoT Enterprise LTSC 2021 ends | A platform incapable of TLS 1.3 remains vendor-supported past both federal PQC deadlines. The clearest case: lifecycle-based planning misses it, capability-based planning catches it | High confidence |
| 2032-05-31 | RHEL 9 maintenance ends |  | High confidence |
| ~2033 | CNSA 2.0 exclusivity targets (phased by category through the early 2030s) | National Security Systems complete the transition; commercial procurement gravity follows | High confidence |
| 2035-05-31 | RHEL 10 maintenance ends | The first ML-KEM-native RHEL completes its lifecycle | High confidence |
| 2036-04 | Ubuntu 26.04 ESM ends | The first PQC-default Ubuntu LTS completes its extended run | High confidence |
