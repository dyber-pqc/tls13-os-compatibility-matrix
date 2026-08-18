#!/usr/bin/env python3
"""Build generated outputs from data/*.yaml:

  docs/<category>.md   - browsable markdown tables (one per category)
  site/data.json       - everything, for the interactive site
  site/badge-*.json    - shields.io endpoint badges served via GitHub Pages

Usage:
  python scripts/build.py           # write outputs
  python scripts/build.py --check   # exit 1 if outputs are stale (CI)
"""
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DOCS = ROOT / "docs"
SITE = ROOT / "site"

# presentation order and pretty headers per kind
HEADERS = {
    "os": [("platform", "Platform / release"), ("native_tls13", "Native TLS 1.3"),
           ("min_release", "Minimum release"), ("stack", "System TLS stack"),
           ("enabled_by_default", "On by default"), ("path_to_capability", "Path to capability"),
           ("support_ends", "Standard support ends"), ("extended_support", "Extended / paid support"),
           ("pqc_notes", "PQC notes"), ("caveats", "Caveats & open questions"),
           ("sources", "Primary sources"), ("status", "Status")],
    "appliance": [("platform", "Platform"), ("tls13_status", "TLS 1.3"),
                  ("min_version", "Minimum version"), ("applies_to", "Applies to (plane / feature)"),
                  ("enabled_by_default", "On by default"), ("caveats", "Caveats & open questions"),
                  ("sources", "Primary sources"), ("status", "Status")],
    "container": [("image", "Image family"), ("capable_tags", "Capable tags"),
                  ("not_capable", "Not capable"), ("stack", "System TLS stack"),
                  ("notes", "Notes"), ("status", "Status")],
    "embedded": [("component", "Component"), ("tls13_status", "TLS 1.3"),
                 ("first_version", "First version"), ("pqc_status", "PQC status"),
                 ("notes", "Notes"), ("status", "Status")],
    "library": [("component", "Component"), ("first_release", "First release with TLS 1.3"),
                ("enabled_by_default", "On by default"), ("support_status", "Support status"),
                ("pqc_notes", "PQC notes"), ("notes", "Notes"), ("status", "Status")],
    "application": [("component", "Component"), ("first_support", "First TLS 1.3 support"),
                    ("governing_stack", "Governing stack"), ("where_to_enable", "Where to enable / verify"),
                    ("notes", "Notes"), ("status", "Status")],
    "timeline": [("date", "Date"), ("event", "Event"),
                 ("why_it_matters", "Why it matters"), ("status", "Status")],
    "verification": [("check", "Check"), ("method", "Command / method"),
                     ("interpretation", "Interpretation & caveats"), ("status", "Status")],
    "decision": [("tier", "Tier"), ("definition", "Definition"),
                 ("action", "Typical action"), ("cost", "Cost class")],
    "pqc": [("topic", "Topic"), ("detail", "Detail"), ("status", "Status")],
    "source": [("source", "Source"), ("covers", "What it covers"), ("location", "Location")],
}

STATUS_LABELS = {
    "Verified": "**Verified**",
    "High confidence": "High confidence",
    "Needs verification": "*Needs verification*",
}

# category display order for the site and docs index
ORDER = [
    "timeline", "decision-framework", "linux", "windows", "macos-bsd", "mobile",
    "network-appliances", "virtualization-cloud", "enterprise-unix-mainframe",
    "container-images", "embedded-iot", "libraries-runtimes",
    "applications-middleware", "verification-methods", "pqc-forward-view",
    "sources",
]


def esc(v):
    return v.replace("|", "\\|").replace("\n", " ")


def md_table(doc):
    cols = HEADERS[doc["kind"]]
    keys = [k for k, _ in cols]
    lines = ["| " + " | ".join(h for _, h in cols) + " |",
             "|" + "---|" * len(cols)]
    for row in doc["rows"]:
        cells = []
        for k in keys:
            v = row.get(k, "")
            if k == "status" and v in STATUS_LABELS:
                v = STATUS_LABELS[v]
            cells.append(esc(v))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def build_doc_page(name, doc):
    parts = [f"# {doc['category']}", ""]
    parts.append("> Generated from [`data/" + name + ".yaml`](../data/" + name +
                 ".yaml) — edit the YAML, not this file. Regenerate with "
                 "`python scripts/build.py`.")
    parts.append("")
    parts.append(md_table(doc))
    if doc.get("notes"):
        parts += ["", "## Notes", ""]
        parts += [f"- {n}" for n in doc["notes"]]
    parts.append("")
    return "\n".join(parts)


def status_counts(docs):
    counts = {"Verified": 0, "High confidence": 0, "Needs verification": 0}
    for doc in docs.values():
        for row in doc["rows"]:
            s = row.get("status")
            if s in counts:
                counts[s] += 1
    return counts


def badge(label, message, color):
    return {"schemaVersion": 1, "label": label, "message": message, "color": color}


def outputs(docs):
    """Return {path: text} for everything this build generates."""
    out = {}
    index_lines = ["# Matrix documentation", "",
                   "Generated views of the data. One page per category:", ""]
    for name in ORDER:
        doc = docs[name]
        out[DOCS / f"{name}.md"] = build_doc_page(name, doc)
        index_lines.append(f"- [{doc['category']}]({name}.md) — {len(doc['rows'])} rows")
    index_lines.append("")
    out[DOCS / "README.md"] = "\n".join(index_lines)

    counts = status_counts(docs)
    total = sum(counts.values())
    payload = {
        "generated_from": "data/*.yaml",
        "status_counts": counts,
        "total_status_rows": total,
        "categories": [
            {"id": name, **docs[name]} for name in ORDER
        ],
    }
    out[SITE / "data.json"] = json.dumps(payload, ensure_ascii=False, indent=1)

    pct = round(100 * counts["Verified"] / total) if total else 0
    out[SITE / "badge-rows.json"] = json.dumps(
        badge("matrix rows", str(total), "blue"))
    out[SITE / "badge-verified.json"] = json.dumps(
        badge("verified", f"{counts['Verified']}/{total} ({pct}%)",
              "brightgreen" if pct >= 50 else "orange"))
    out[SITE / "badge-open.json"] = json.dumps(
        badge("needs verification", str(counts["Needs verification"]),
              "red" if counts["Needs verification"] else "brightgreen"))
    return out


def main():
    check = "--check" in sys.argv
    docs = {}
    for path in sorted(DATA.glob("*.yaml")):
        docs[path.stem] = yaml.safe_load(path.read_text(encoding="utf-8"))
    missing = [n for n in ORDER if n not in docs]
    if missing:
        print(f"ERROR: data files missing for: {missing}")
        return 1
    extra = [n for n in docs if n not in ORDER]
    if extra:
        print(f"ERROR: data files not in ORDER list (add them in build.py): {extra}")
        return 1

    stale = []
    for path, text in outputs(docs).items():
        if check:
            current = path.read_text(encoding="utf-8") if path.exists() else None
            if current != text:
                stale.append(path.relative_to(ROOT))
        else:
            path.parent.mkdir(exist_ok=True)
            path.write_text(text, encoding="utf-8", newline="\n")
            print(f"wrote {path.relative_to(ROOT)}")
    if check:
        if stale:
            print("Generated files are stale. Run: python scripts/build.py")
            for p in stale:
                print(f"  stale: {p}")
            return 1
        print("Generated files are up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
