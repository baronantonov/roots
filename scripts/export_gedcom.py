#!/usr/bin/env python3
"""
Экспорт полного древа ROOTS в стандарт GEDCOM 5.5.1 UTF-8.
"""

import csv
import json
import re
import os

BASE_DIR = "/home/brnv/projects/ROOTS"

def export_gedcom():
    person_path = os.path.join(BASE_DIR, "person-register.csv")
    dash_path = os.path.join(BASE_DIR, "dashboard.html")

    with open(person_path, "r", encoding="utf-8") as f:
        persons = list(csv.DictReader(f))

    with open(dash_path, "r", encoding="utf-8") as f:
        html = f.read()

    lines = [
        "0 HEAD",
        "1 SOUR ROOTS-RESEARCH",
        "2 VERS 1.35.0",
        "1 GEDC",
        "2 VERS 5.5.1",
        "2 FORM LINEAGE-LINKED",
        "1 CHAR UTF-8"
    ]

    for p in persons:
        pid = p["person_id"]
        canonical_name = p.get("preferred_label", "")
        parts = canonical_name.split()
        if len(parts) >= 2:
            surname = parts[0]
            first_name = " ".join(parts[1:])
            name_str = f"{first_name} /{surname}/"
        else:
            name_str = f"{canonical_name} //"

        lines.append(f"0 @{pid}@ INDI")
        lines.append(f"1 NAME {name_str}")

        b_date = p.get("birth_estimate", "")
        b_place = p.get("places", "")
        if b_date or b_place:
            lines.append("1 BIRT")
            if b_date:
                lines.append(f"2 DATE {b_date}")
            if b_place:
                lines.append(f"2 PLAC {b_place}")

        d_date = p.get("death_estimate", "")
        if d_date:
            lines.append("1 DEAT")
            lines.append(f"2 DATE {d_date}")

        occ = p.get("occupation_or_status", "")
        if occ:
            lines.append(f"1 OCCU {occ[:90]}")

        notes = p.get("notes", "")
        if notes:
            lines.append(f"1 NOTE {notes[:180]}")

    # Извлекаем браки
    m_match = re.search(r'const CANVAS_MARRIAGES = (\[.*?\]);', html, re.DOTALL)
    if m_match:
        # Упрощенный парсинг JSON-like объектов
        raw_m = m_match.group(1)
        items = re.findall(r'\{\s*id:\s*"([^"]+)",\s*p1:\s*"([^"]+)",\s*p2:\s*"([^"]+)",\s*date:\s*"([^"]+)",\s*children:\s*\[(.*?)\]', raw_m)
        fam_idx = 1
        for mid, p1, p2, mdate, c_str in items:
            fid = f"F{fam_idx:04d}"
            fam_idx += 1
            lines.append(f"0 @{fid}@ FAM")
            lines.append(f"1 HUSB @{p1}@")
            lines.append(f"1 WIFE @{p2}@")
            if mdate:
                lines.append("1 MARR")
                lines.append(f"2 DATE {mdate}")
            c_ids = re.findall(r'"(P-\d+)"', c_str)
            for cid in c_ids:
                lines.append(f"1 CHIL @{cid}@")

    lines.append("0 TRLR")

    ged_path = os.path.join(BASE_DIR, "roots.ged")
    with open(ged_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Exported {len(persons)} persons to roots.ged (GEDCOM 5.5.1 UTF-8)")

if __name__ == "__main__":
    export_gedcom()
