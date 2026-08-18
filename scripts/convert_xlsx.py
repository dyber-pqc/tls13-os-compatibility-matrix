#!/usr/bin/env python3
"""One-time converter: TLS13_OS_Compatibility_Matrix xlsx -> data/*.yaml

Kept in the repo for provenance. The YAML files under data/ are the source of
truth from here on; this script documents how they were seeded from the
original community-draft spreadsheet.

Usage: python scripts/convert_xlsx.py path/to/matrix.xlsx
"""
import sys
from pathlib import Path

import openpyxl
import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# sheet title -> (output file, kind, column keys in sheet order)
SHEETS = {
    "Milestone Timeline": ("timeline.yaml", "timeline",
        ["date", "event", "why_it_matters", "status"]),
    "Linux": ("linux.yaml", "os",
        ["platform", "native_tls13", "min_release", "stack", "enabled_by_default",
         "path_to_capability", "support_ends", "extended_support", "pqc_notes",
         "caveats", "sources", "status"]),
    "Windows": ("windows.yaml", "os", None),  # same as Linux; filled below
    "macOS and BSD": ("macos-bsd.yaml", "os", None),
    "Mobile": ("mobile.yaml", "os", None),
    "Network Appliances": ("network-appliances.yaml", "appliance",
        ["platform", "tls13_status", "min_version", "applies_to",
         "enabled_by_default", "caveats", "sources", "status"]),
    "Virtualization and Cloud": ("virtualization-cloud.yaml", "appliance", None),
    "Enterprise Unix and Mainframe": ("enterprise-unix-mainframe.yaml", "os", None),
    "Container Images": ("container-images.yaml", "container",
        ["image", "capable_tags", "not_capable", "stack", "notes", "status"]),
    "Embedded and IoT Stacks": ("embedded-iot.yaml", "embedded",
        ["component", "tls13_status", "first_version", "pqc_status", "notes", "status"]),
    "Libraries and Runtimes": ("libraries-runtimes.yaml", "library",
        ["component", "first_release", "enabled_by_default", "support_status",
         "pqc_notes", "notes", "status"]),
    "Applications and Middleware": ("applications-middleware.yaml", "application",
        ["component", "first_support", "governing_stack", "where_to_enable",
         "notes", "status"]),
    "Verification Methods": ("verification-methods.yaml", "verification",
        ["check", "method", "interpretation", "status"]),
    "Decision Framework": ("decision-framework.yaml", "decision",
        ["tier", "definition", "action", "cost"]),
    "PQC Forward View": ("pqc-forward-view.yaml", "pqc",
        ["topic", "detail", "status"]),
    "Sources": ("sources.yaml", "source",
        ["source", "covers", "location"]),
}

# kinds that share a column layout inherit it from the first sheet of that kind
KIND_COLUMNS = {}


def clean(v):
    if v is None:
        return ""
    return str(v).strip()


def convert_sheet(ws, kind, columns):
    rows, notes = [], []
    in_notes = False
    for i, raw in enumerate(ws.iter_rows(values_only=True)):
        vals = [clean(v) for v in raw]
        if i == 0:  # header row
            continue
        if not any(vals):
            continue
        if vals[0] == "Notes" and not any(vals[1:]):
            in_notes = True
            continue
        if in_notes:
            notes.append(vals[0])
            continue
        row = {}
        for key, val in zip(columns, vals):
            if val:
                row[key] = val
        if row:
            rows.append(row)
    return rows, notes


def main(xlsx_path):
    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    DATA.mkdir(exist_ok=True)
    for title, (outfile, kind, columns) in SHEETS.items():
        if columns is None:
            columns = KIND_COLUMNS[kind]
        else:
            KIND_COLUMNS.setdefault(kind, columns)
        ws = wb[title]
        rows, notes = convert_sheet(ws, kind, columns)
        doc = {"category": title, "kind": kind, "rows": rows}
        if notes:
            doc["notes"] = notes
        out = DATA / outfile
        with out.open("w", encoding="utf-8", newline="\n") as f:
            yaml.dump(doc, f, sort_keys=False, allow_unicode=True,
                      width=100000, default_flow_style=False)
        print(f"{out.name}: {len(rows)} rows, {len(notes)} notes")


if __name__ == "__main__":
    main(sys.argv[1])
