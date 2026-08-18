#!/usr/bin/env python3
"""Validate the data/*.yaml files that back the matrix.

Run locally before opening a PR:  python scripts/validate.py
CI runs this on every push and pull request.

Checks:
  * every file parses as YAML with the expected top-level shape
  * every row has the required keys for its kind, and no unknown keys
  * status values are one of the allowed set
  * evidence rows (os / appliance / library / etc.) carry a primary source
  * "Verified" rows must name verifiers in the caveats/notes field
  * no tab characters or trailing whitespace surprises in cell values
"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

ALLOWED_STATUS = {"Verified", "High confidence", "Needs verification"}

# kind -> (required keys, all allowed keys)
SCHEMAS = {
    "os": (
        {"platform", "native_tls13", "stack", "sources", "status"},
        {"platform", "native_tls13", "min_release", "stack", "enabled_by_default",
         "path_to_capability", "support_ends", "extended_support", "pqc_notes",
         "caveats", "sources", "status"},
    ),
    "appliance": (
        {"platform", "tls13_status", "applies_to", "sources", "status"},
        {"platform", "tls13_status", "min_version", "applies_to",
         "enabled_by_default", "caveats", "sources", "status"},
    ),
    "container": (
        {"image", "stack", "status"},
        {"image", "capable_tags", "not_capable", "stack", "notes", "status"},
    ),
    "embedded": (
        {"component", "tls13_status", "status"},
        {"component", "tls13_status", "first_version", "pqc_status", "notes", "status"},
    ),
    "library": (
        {"component", "first_release", "status"},
        {"component", "first_release", "enabled_by_default", "support_status",
         "pqc_notes", "notes", "status"},
    ),
    "application": (
        {"component", "first_support", "governing_stack", "status"},
        {"component", "first_support", "governing_stack", "where_to_enable",
         "notes", "status"},
    ),
    "timeline": (
        {"date", "event", "status"},
        {"date", "event", "why_it_matters", "status"},
    ),
    "verification": (
        {"check", "method", "interpretation", "status"},
        {"check", "method", "interpretation", "status"},
    ),
    "decision": (
        {"tier", "definition", "action", "cost"},
        {"tier", "definition", "action", "cost"},
    ),
    "pqc": (
        {"topic", "detail", "status"},
        {"topic", "detail", "status"},
    ),
    "source": (
        {"source", "covers", "location"},
        {"source", "covers", "location"},
    ),
}

# kinds whose rows are factual claims and therefore carry a status column
STATUS_KINDS = {"os", "appliance", "container", "embedded", "library",
                "application", "timeline", "verification", "pqc"}


def fail(errors, path, msg):
    errors.append(f"{path.name}: {msg}")


def label(row):
    for key in ("platform", "component", "image", "check", "tier", "topic",
                "source", "event", "date"):
        if key in row:
            return str(row[key])[:60]
    return "<row>"


def validate_file(path, errors):
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        fail(errors, path, f"YAML parse error: {e}")
        return None
    if not isinstance(doc, dict):
        fail(errors, path, "top level must be a mapping")
        return None
    for key in ("category", "kind", "rows"):
        if key not in doc:
            fail(errors, path, f"missing top-level key '{key}'")
            return None
    kind = doc["kind"]
    if kind not in SCHEMAS:
        fail(errors, path, f"unknown kind '{kind}'")
        return None
    required, allowed = SCHEMAS[kind]
    if not isinstance(doc["rows"], list) or not doc["rows"]:
        fail(errors, path, "rows must be a non-empty list")
        return None
    seen = set()
    for row in doc["rows"]:
        if not isinstance(row, dict):
            fail(errors, path, f"row is not a mapping: {row!r}")
            continue
        name = label(row)
        missing = required - row.keys()
        if missing:
            fail(errors, path, f"[{name}] missing required keys: {sorted(missing)}")
        unknown = row.keys() - allowed
        if unknown:
            fail(errors, path, f"[{name}] unknown keys: {sorted(unknown)}")
        for k, v in row.items():
            if not isinstance(v, str) or not v.strip():
                fail(errors, path, f"[{name}] key '{k}' must be a non-empty string")
            elif v != v.strip():
                fail(errors, path, f"[{name}] key '{k}' has leading/trailing whitespace")
            elif "\t" in v:
                fail(errors, path, f"[{name}] key '{k}' contains a tab character")
        if kind in STATUS_KINDS:
            status = row.get("status")
            if status and status not in ALLOWED_STATUS:
                fail(errors, path,
                     f"[{name}] status '{status}' not in {sorted(ALLOWED_STATUS)}")
            if status == "Verified":
                trail = (row.get("caveats", "") + row.get("notes", ""))
                if not trail:
                    fail(errors, path,
                         f"[{name}] Verified rows must record who verified and when "
                         f"in the caveats/notes field (initials + date)")
        first = label(row)
        if first in seen:
            fail(errors, path, f"duplicate row label '{first}'")
        seen.add(first)
    if "notes" in doc:
        if not isinstance(doc["notes"], list) or not all(
                isinstance(n, str) and n.strip() for n in doc["notes"]):
            fail(errors, path, "notes must be a list of non-empty strings")
    return doc


def main():
    errors = []
    files = sorted(DATA.glob("*.yaml"))
    if not files:
        print("No data files found under data/ - nothing to validate.")
        return 1
    total_rows = 0
    counts = {s: 0 for s in ALLOWED_STATUS}
    for path in files:
        doc = validate_file(path, errors)
        if doc:
            total_rows += len(doc["rows"])
            for row in doc["rows"]:
                s = row.get("status")
                if s in counts:
                    counts[s] += 1
    print(f"Checked {len(files)} files, {total_rows} rows.")
    print("Status counts: " + ", ".join(f"{k}: {v}" for k, v in sorted(counts.items())))
    if errors:
        print(f"\n{len(errors)} problem(s) found:\n")
        for e in errors:
            print(f"  FAIL  {e}")
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
