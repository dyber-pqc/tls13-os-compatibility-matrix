# Applications and Middleware

> Generated from [`data/applications-middleware.yaml`](../data/applications-middleware.yaml) — edit the YAML, not this file. Regenerate with `python scripts/build.py`.

| Component | First TLS 1.3 support | Governing stack | Where to enable / verify | Notes | Status |
|---|---|---|---|---|---|
| nginx | 1.13.0 with OpenSSL 1.1.1 | Linked OpenSSL | ssl_protocols (TLSv1.3 in the default since 1.23.4, per nginx docs) | Most common reason a capable host serves only 1.2: an old ssl_protocols line | High confidence |
| Apache httpd | 2.4.37 (2018-10-23) with OpenSSL 1.1.1; enabled by default | Linked OpenSSL | SSLProtocol directive | Corrected from 2.4.36 during verification | High confidence |
| HAProxy | 1.8.1 with OpenSSL 1.1.1 | Linked OpenSSL | ssl-min-ver / ssl-max-ver on bind lines | Also check crt-list and default-server for backend-side settings | High confidence |
| Envoy | Long supported (BoringSSL) | BoringSSL | TlsParameters min/max protocol version | Service mesh data planes are usually not the gap | High confidence |
| Caddy / Traefik | From early releases (Go stack) | Go crypto/tls | Defaults are modern; overrides in config | Go 1.24+ builds bring ML-KEM hybrids by default | High confidence |
| IIS / HTTP.sys | Windows Server 2022 | Schannel | OS version gate first; then Schannel settings | See Windows tab; no configuration rescues Server 2019 | High confidence |
| Apache Tomcat | JSSE path: per running JDK. OpenSSL path: tomcat-native against 1.1.1+ | JDK or tomcat-native | Connector sslEnabledProtocols; verify which engine the connector uses | Two engines, two answers, same server.xml | High confidence |
| JVM middleware (Kafka, Elasticsearch, Jenkins, etc.) | Per running JDK (11+, or 8u261/8u272 backports) | JDK JSSE | JVM version audit; ssl.protocol settings | One JDK upgrade moves the whole category; one frozen JDK 8u151 holds it back | High confidence |
| Postfix / Dovecot (mail) | With linked OpenSSL 1.1.1+ | Linked OpenSSL | smtpd_tls_protocols, ssl_min_protocol | SMTP TLS is opportunistic: capability without enforcement is the norm. MTA-STS and DANE govern enforcement; test with STARTTLS-aware tools | High confidence |
| OpenLDAP | With linked OpenSSL 1.1.1+ | Linked OpenSSL | olcTLSProtocolMin |  | High confidence |
| Active Directory LDAPS | Domain controllers on Server 2022+ | Schannel (DC operating system) | DC OS version audit | A directory served by Server 2019 DCs caps LDAPS at TLS 1.2 for every client and app in the forest until the DCs move. One of the highest-leverage upgrades in the whole matrix | High confidence |
| Microsoft Exchange | Exchange 2019 CU15 / SE on Server 2022 or 2025; enabled by default; SMTP excluded until a future update | Schannel plus Exchange support statement | Exchange version and OS version together | Per-protocol split inside one product: HTTPS yes, SMTP not yet, and disabling any protocol except 1.3 is unsupported. Exchange 2016 and 2019 left support 2025-10 | High confidence |
| PostgreSQL | With linked OpenSSL 1.1.1+ | Linked OpenSSL | ssl_min_protocol_version (PG 12+) | Inherits the distro OpenSSL line | High confidence |
| MySQL | 8.0.16 with OpenSSL 1.1.1 | Bundled or linked OpenSSL | tls_version system variable | 5.7 caps at TLS 1.2 | High confidence |
| MariaDB | 10.4 era against OpenSSL 1.1.1; bundled-library builds vary (confirm) | Build dependent | tls_version; check which TLS library the build uses |  | *Needs verification* |
| Microsoft SQL Server | SQL Server 2022 with TDS 8.0 on a TLS 1.3 capable Windows; 2019 and earlier never | Schannel | SQL and OS versions together; strict encryption mode | Keep TLS 1.2 enabled on the host: satellite services still require it at startup | High confidence |
| Oracle Database | 23ai (TLS 1.3 by default); 19c from RU 19.32 via the opt-in next-generation provider | Oracle wallet stack; the next-generation provider is OpenSSL based | sqlnet parameters; provider selection | 19c with the default provider caps at 1.2; the RU 19.32 next-generation provider adds TLS 1.3, FIPS 140-3 and ML-KEM | High confidence |
| MongoDB / Redis | Platform stack (MongoDB) and linked OpenSSL (Redis 6+) | Platform or linked OpenSSL | net.tls settings; tls-protocols | Both inherit the host line rather than bundling | High confidence |
| IBM Db2 | 11.5 era via GSKit (corroborated; exact fix pack still to pin) | IBM GSKit | SSL_VERSIONS in dbm cfg | Db2 for z/OS follows z/OS System SSL instead; two different answers under one product name | *Needs verification* |
| SAP NetWeaver / CommonCryptoLib | Recent CommonCryptoLib 8.5.x with matching kernel (confirm against SAP Notes) | SAP CommonCryptoLib | Profile parameters (ssl/ciphersuites) | SAP publishes support in SAP Notes behind a login; a contributor with access should pin the numbers | *Needs verification* |
| SharePoint and on-prem Microsoft stack | Rides the Windows Server and .NET versions | Schannel | OS version audit first | Farms hosted on Server 2019 cap at TLS 1.2 regardless of the SharePoint version on top | High confidence |
| VDI control planes (Citrix, Omnissa Horizon) | Mixed per component (confirm) | Windows services plus appliance components | Per component inventory | Gateways, connection servers and agents adopt TLS separately; the NetScaler Gateway to VDA path documents TLS 1.3 with VDA 2503 and later | *Needs verification* |
| Network HSM and KMS appliances | Confirm per vendor firmware | Vendor stacks | Client libraries and management UI, separately | The devices anchoring key custody deserve the same per-plane scrutiny as firewalls | *Needs verification* |

## Notes

- The recurring pattern: capability comes from the stack underneath (OS tab or linked library), while an explicit protocol line in the application config decides whether it is used. Estate scanning must therefore record per-listener results; a capable host proves nothing about its services.
