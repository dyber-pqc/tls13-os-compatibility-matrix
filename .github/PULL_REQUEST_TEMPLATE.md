## What this PR changes

<!-- e.g. "Verifies the RHEL 8 row against the Red Hat lifecycle page" / "Adds Synology DSM rows" -->

## Evidence

<!-- Primary source(s) checked — URL or doc title + section. For live checks, paste the
     command and relevant output (e.g. openssl s_client -connect host:443 -tls1_3 -brief). -->

## Checklist

- [ ] Edited `data/*.yaml` only (never `docs/` or `site/data.json` by hand)
- [ ] Ran `python scripts/validate.py` — clean
- [ ] Ran `python scripts/build.py` and committed the regenerated files
- [ ] Every changed claim cites a source a stranger can check
- [ ] If I flipped a status to `Verified`: I'm an **independent** second checker, and my
      initials + date are in the row's caveats/notes field
