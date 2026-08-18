# Embedded and IoT Stacks

> Generated from [`data/embedded-iot.yaml`](../data/embedded-iot.yaml) — edit the YAML, not this file. Regenerate with `python scripts/build.py`.

| Component | TLS 1.3 | First version | PQC status | Notes | Status |
|---|---|---|---|---|---|
| Mbed TLS | Yes on 3.x; No on 2.28 LTS | Fully stabilized and default-enabled from 3.6.0 LTS (2024-03; supported to at least 2027-03) | Not mainline as of seeding; confirm roadmap (PSA driver path) | 2.28 LTS, still common in shipped firmware, has no TLS 1.3 at all and left support at the end of 2024. The most consequential embedded dividing line | High confidence |
| wolfSSL | Yes | 3.15.0 (2018, draft 28, via the enable-tls13 build option) | ML-KEM, ML-DSA and SLH-DSA supported; wolfCrypt holds FIPS 140-3 certificates 4718 (to 2029-07) and 5041 (to 2030-07); a further FIPS 140-3 certificate incorporating PQC was announced 2026-02 with CMVP submission in process | Commercial and GPL dual license; common in constrained and FIPS-required embedded designs | High confidence |
| BearSSL | No | n/a (TLS 1.2 max, corroborated as of 2026) | None | Deliberately minimal; designs on BearSSL need a stack change for TLS 1.3. Confirm at bearssl.org | *Needs verification* |
| LibreSSL / libtls | Yes | Client from 3.1; server default from 3.2.0; first stable both-sides default is 3.2.2 (OpenBSD 6.8) | Confirm roadmap | Default stack on OpenBSD; some embedded and BSD-derived products | High confidence |
| BoringSSL | Yes | 2018 era (no public versioned releases) | Pioneer: ML-KEM hybrids proven at Google scale | Not intended for third-party consumption but ubiquitous via Chrome, Android, gRPC, Envoy, vSphere | High confidence |
| AWS s2n-tls | Yes | Long supported (exact first release still to pin) | ML-KEM hybrids via AWS-LC, deployed to AWS KMS, ACM and Secrets Manager endpoints | Powers AWS service HTTPS endpoints | *Needs verification* |
| rustls | Yes | From inception | X25519MLKEM768 preferred by default with the aws-lc-rs provider; ML-KEM moved into the rustls crate itself at 0.23.22 | Growing share in proxies and cloud-native infrastructure | High confidence |
| OpenWrt | Build dependent | 19.07+ with OpenSSL builds; default TLS provider has varied by release (mbedTLS 2.28 default in 23.05 lacked TLS 1.3; confirm 24.x state) | Follows chosen provider | Perfect illustration that embedded capability is a build-time component choice, not an OS version fact | *Needs verification* |
| Yocto / Buildroot images | Recipe dependent | Whatever openssl or mbedtls recipe the image pins | Recipe dependent | Long-lived firmware ships frozen stacks; this is the deepest tail of the whole migration. Audit the recipe lock, per product, per firmware version | High confidence |
| Zephyr / ESP-IDF / FreeRTOS ecosystems | Depends on the pinned Mbed TLS generation | ESP-IDF documents full TLS 1.3 from Mbed TLS 3.6.0; Zephyr and FreeRTOS track whatever they pin | Follows the pinned stack | Same rule as OpenWrt and Yocto: the build manifest decides, not the platform name | *Needs verification* |
| OT, ICS and industrial gateways | Mostly absent or frozen | Per product firmware | None in the field | OPC UA security policies are distinct from TLS. Where TLS appears (web HMIs, MQTT northbound, historian links) it is a frozen embedded stack; expect the part of the estate still terminating TLS 1.2 in 2035 | *Needs verification* |

## Notes

- Embedded is where the TLS 1.2 long tail will live in 2035. The unit of analysis is the firmware build manifest, not the device model. Contributors from the embedded space: rows per RTOS ecosystem (Zephyr, FreeRTOS plus coreTLS choices, ESP-IDF) are a welcome extension.
