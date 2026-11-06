#!/usr/bin/env python3
"""
Синхронизация таблицы утверждений в final-report.md из claims-register.csv.
"""

import csv
import os
import re

BASE_DIR = "/home/brnv/projects/ROOTS"

def sync_report():
    claims_path = os.path.join(BASE_DIR, "claims-register.csv")
    report_path = os.path.join(BASE_DIR, "final-report.md")

    with open(claims_path, "r", encoding="utf-8") as f:
        claims = list(csv.DictReader(f))

    with open(report_path, "r", encoding="utf-8") as f:
        rep_text = f.read()

    # Формируем новую таблицу утверждений
    table_lines = [
        "| Claim ID | Утверждение | Статус | Поддержка | Противоречия | Обоснование |",
        "|---|---|---|---|---|---|"
    ]

    for c in claims:
        cid = c["claim_id"]
        text = c["claim_text"].replace("\n", " ").replace("|", "/")
        status = c["status"]
        arts = c["artifact_ids"].replace(";", "; ")
        arts_fmt = f"`[{arts}]`" if arts else "нет"
        contra = c["contradicting_artifact_ids"] if c.get("contradicting_artifact_ids") else "нет"
        rationale = c["rationale"].replace("\n", " ").replace("|", "/")
        table_lines.append(f"| `{cid}` | {text} | `{status}` | {arts_fmt} | {contra} | {rationale} |")

    new_table_str = "\n".join(table_lines)

    # Заменяем старую таблицу в разделе 8
    pattern = r"(\| Claim ID \| Утверждение \|.*?\n)(?=\n---\n\n## 9\. Существенные противоречия)"
    if re.search(pattern, rep_text, re.DOTALL):
        rep_text = re.sub(pattern, new_table_str + "\n", rep_text, flags=re.DOTALL)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(rep_text)
        print(f"Replaced claims table in final-report.md with {len(claims)} claims.")
    else:
        print("Table pattern not found in final-report.md")

if __name__ == "__main__":
    sync_report()
