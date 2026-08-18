# macOS and BSD

> Generated from [`data/macos-bsd.yaml`](../data/macos-bsd.yaml) — edit the YAML, not this file. Regenerate with `python scripts/build.py`.

| Platform / release | Native TLS 1.3 | Minimum release | System TLS stack | On by default | Path to capability | Standard support ends | Extended / paid support | PQC notes | Caveats & open questions | Primary sources | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| macOS 10.13 High Sierra and earlier | No (draft-era code only, off by default) | macOS 10.14.4 | Secure Transport | No | OS upgrade where hardware allows; otherwise device replacement | Unsupported | n/a | None |  | Apple support publications | High confidence |
| macOS 10.14 Mojave | Partial before 10.14.4 | 10.14.4 | Secure Transport / Network.framework | Yes, from 10.14.4 | Point update | Unsupported | n/a | None | 10.14.4 negotiates TLS 1.3 (aligned with Safari 12.1), but App Transport Security defaults kept TLS 1.2 as the maximum in that era, so per-app behavior varied; state the claim carefully | Apple release notes | *Needs verification* |
| macOS 11 Big Sur through current (macOS 26 Tahoe) | Yes | Capable at GA | Network.framework / Secure Transport | Yes | Already capable | Apple patches roughly the three most recent majors; no formal published lifecycle | n/a | The 26 cycle (fall 2025) added the hybrid PQ group at the TLS layer in Network.framework plus quantum-secure CryptoKit APIs (corroborated; confirm shipped scope against Apple docs). iMessage PQ3 came earlier | Absence of a published support lifecycle is itself a planning caveat | Apple | *Needs verification* |
| OpenBSD (LibreSSL) | Yes | OpenBSD 6.8 / LibreSSL 3.2.2 (client support from 3.1) | LibreSSL (libssl / libtls) | Yes | Already capable on supported releases | Two most recent 6-month releases supported | n/a | Confirm LibreSSL PQC roadmap (not yet mainline as of seeding) | libtls API differs from OpenSSL; ports linking OpenSSL behave per OpenSSL | OpenBSD release notes | High confidence |
| NetBSD | Yes on current | Confirm first release with OpenSSL 1.1.1 in base | OpenSSL in base | Yes | Major upgrade for old installs | Per release | n/a |  |  | NetBSD docs | *Needs verification* |
| FreeBSD 11.x and earlier | No | FreeBSD 12.0 | Base OpenSSL predates 1.1.1 | No | Major version upgrade | Ended | n/a | None |  | FreeBSD security pages | High confidence |
| FreeBSD 12.0 and later | Yes | 12.0 | OpenSSL 1.1.1 in base at 12.0; 3.0 in 14.x | Yes | Already capable | Per branch (12 ended 2023-12; 13.x winding down; 14.x current) | n/a | Confirm base OpenSSL version and PQC state in FreeBSD 15 |  | FreeBSD security pages | *Needs verification* |

## Notes

- Client-side reality check: evergreen browsers bundle their own stacks, so Chrome or Firefox on an old macOS still negotiates TLS 1.3. The gap this matrix targets is the OS-native stack that system services, MDM agents, and Apple frameworks depend on.
