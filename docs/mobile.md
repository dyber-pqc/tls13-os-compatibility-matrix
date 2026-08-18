# Mobile

> Generated from [`data/mobile.yaml`](../data/mobile.yaml) — edit the YAML, not this file. Regenerate with `python scripts/build.py`.

| Platform / release | Native TLS 1.3 | Minimum release | System TLS stack | On by default | Path to capability | Standard support ends | Extended / paid support | PQC notes | Caveats & open questions | Primary sources | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| iOS / iPadOS 12.2 and later | Yes | 12.2 | Network.framework / Secure Transport | Yes | OS update; hardware older than the iOS 12 line needs replacement | Latest major fully supported; limited security back-support for prior majors (informal) | n/a | iOS 26 (fall 2025) adds the hybrid PQ group at the TLS layer in Network.framework plus quantum-secure CryptoKit APIs (corroborated; confirm shipped scope) | App Transport Security governs app connections; MDM can pin minimum TLS | Apple | High confidence |
| iOS 12.1 and earlier | No (final RFC) | 12.2 | Secure Transport | No | Device replacement (hardware capped below iOS 12.2) | Unsupported | n/a | None | Survives in kiosk, scanner and payment fleets | Apple | High confidence |
| Android 10 (API 29) and later | Yes (platform default) | Android 10 | Conscrypt (BoringSSL based) | Yes | OS update where OEM provides one; otherwise device replacement | OEM dependent (3 to 7 years by vendor and tier) | n/a | From Android 10, Conscrypt is an updatable Mainline module via Google Play system updates, decoupling TLS capability from OEM firmware (corroborated; device-class coverage still to confirm) | Fleet reality is set by the oldest OEM-abandoned devices, not the platform line | Android platform docs | *Needs verification* |
| Android 9 and earlier | No (platform stack) | Android 10 | Conscrypt (older) | No | Apps can self-provision TLS 1.3 via Google Play services security provider or bundled Conscrypt; the platform itself stays below the line | Unsupported by Google; OEM patches vary | n/a | None | App-level workaround does not help system components or unmanaged apps | Android developer docs | High confidence |

## Notes

- Mobile matters to infrastructure planning as the client population: once server estates enforce TLS 1.3 minimums (a prerequisite for PQC-only policies later), abandoned Android fleets and frozen iOS kiosk devices are what breaks.
