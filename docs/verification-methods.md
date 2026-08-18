# Verification Methods

> Generated from [`data/verification-methods.yaml`](../data/verification-methods.yaml) — edit the YAML, not this file. Regenerate with `python scripts/build.py`.

| Check | Command / method | Interpretation & caveats | Status |
|---|---|---|---|
| Remote service check | openssl s_client -connect host:443 -tls1_3 -brief | Success prints TLSv1.3; failure means the service as configured does not offer it. Tests service plus path, not just the stack | High confidence |
| Full protocol sweep | testssl.sh -p https://host  or  nmap -p 443 --script ssl-enum-ciphers host | Enumerates all offered versions; catches capable-but-disabled services and weak floors in one pass | High confidence |
| Outbound path check | curl -Iv --tlsv1.3 https://host/ | Requires curl built on a capable backend (curl -V shows it); exercises any middleboxes between you and the target | High confidence |
| Local Linux stack | openssl version; openssl ciphers -s -tls1_3 | A non-empty suite list means the stack is capable. Then check policy gates: update-crypto-policies --show on RHEL family; MinProtocol in openssl.cnf elsewhere | High confidence |
| Local Windows | OS build gate first (Win11 / Server 2022+); then Get-TlsCipherSuite for TLS_AES_* suites; then the Schannel registry keys under Protocols for explicit disables | On older Windows the version check is definitive: not capable, no configuration rescues it | High confidence |
| Fleet package inventory | rpm -q openssl / dpkg -s openssl via configuration management, mapped against this matrix | Triage only. Version strings mislead on enterprise backports; confirm by negotiation before recording Verified | High confidence |
| Record per listener, not per host | Scan each TLS port in use (443 web, 636 LDAPS, 3389 RDP, 5432 PostgreSQL, 9093 Kafka, 25/587 SMTP, 8443 management) | A host is capable; a listener is configured. Inventories that stop at the host level systematically overstate readiness | High confidence |
| Middlebox awareness | Test from both sides of any TLS-inspecting proxy, firewall, or load balancer | Inspection and termination devices below their capable release silently cap or break TLS 1.3 for whole segments; see Network Appliances tab | High confidence |
| FIPS mode interaction | Re-run stack and service checks with FIPS mode enabled, not only disabled | Legacy FIPS modules lacked TLS 1.3; modern ones include it but validation status varies by product (see the vSphere 8.0 U3 row). Regulated estates must test the mode they actually run | High confidence |
| Mail special case | testssl.sh -t smtp host:25 (STARTTLS aware) | Opportunistic TLS means capability without enforcement is the norm; check MTA-STS and DANE posture separately | High confidence |
| PQC handshake size check | Repeat remote checks with a hybrid group forced: openssl s_client -connect host:443 -tls1_3 -groups X25519MLKEM768 | The ML-KEM key share pushes the ClientHello past one TCP segment. Middleboxes and stacks that mishandle fragmented ClientHellos break (Mbed TLS before 3.6.3 is a documented case); test every inspection path before enabling PQC fleet-wide | High confidence |

## Notes

- Suggested fleet workflow: (1) package and OS inventory mapped to this matrix for triage, (2) active negotiation scan per listener for truth, (3) config extraction for the why behind every 1.2-only result, (4) record findings per service with a date. Cryptographic inventory tooling can automate steps 1 to 3. Step 4 stays human.
