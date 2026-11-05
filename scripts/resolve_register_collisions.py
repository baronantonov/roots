import csv

def main():
    # 1. Clean person-register.csv
    # P-0001 to P-0032 (Belovs) + add P-0033 (Avdey), P-0034 (Gritsko), P-0035 (Klim)
    persons = []
    seen_pids = set()
    with open("person-register.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields_p = reader.fieldnames
        for r in reader:
            pid = r["person_id"]
            if pid in ("P-0030", "P-0031", "P-0032"):
                if pid not in seen_pids:
                    # First time: Belovs
                    seen_pids.add(pid)
                    persons.append(r)
                else:
                    # Second time: Brinyuks -> renumber
                    if "Авдей" in r["preferred_label"]:
                        r["person_id"] = "P-0033"
                        r["relatives_as_reported"] = r["relatives_as_reported"].replace("P-0030", "P-0033")
                        r["source_artifact_ids"] = "A-0039"
                        persons.append(r)
                    elif "Грицко" in r["preferred_label"]:
                        r["person_id"] = "P-0034"
                        r["relatives_as_reported"] = "Соратник: Клим Бренюка (P-0035); потомки: род Бринюк"
                        r["source_artifact_ids"] = "A-0040"
                        persons.append(r)
                    elif "Клим" in r["preferred_label"]:
                        r["person_id"] = "P-0035"
                        r["relatives_as_reported"] = "Соратник: Грицко Бринюк (P-0034); потомки: род Бринюк"
                        r["source_artifact_ids"] = "A-0040"
                        persons.append(r)
            else:
                if pid == "P-0029":
                    # Update father reference to P-0033
                    r["relatives_as_reported"] = r["relatives_as_reported"].replace("P-0030", "P-0033")
                    r["source_artifact_ids"] = "A-0033;A-0034;A-0039"
                persons.append(r)
                seen_pids.add(pid)

    with open("person-register.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields_p)
        writer.writeheader()
        writer.writerows(persons)
    print("person-register.csv: resolved to", len(persons), "persons (P-0001..P-0035).")

    # 2. Clean artifact-register.csv
    # Ensure unique A-0001..A-0040
    artifacts = []
    seen_aids = set()
    with open("artifact-register.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields_a = reader.fieldnames
        for r in reader:
            aid = r["artifact_id"]
            if aid in ("A-0036", "A-0037"):
                if aid not in seen_aids:
                    # First time: Belovs (A-0036 = OpenList/Memorial, A-0037 = Pamyat Naroda/CAMO)
                    artifacts.append(r)
                    seen_aids.add(aid)
                else:
                    # Second time: Brinyuk hospital card & Cossack registers
                    title = r.get("source_title", "")
                    if "Воронежского" in title or "Бринюка" in title:
                        r["artifact_id"] = "A-0039"
                        r["related_claim_ids"] = "C-0042;C-0043"
                        r["person_ids"] = "P-0028;P-0029;P-0033"
                        artifacts.append(r)
                        seen_aids.add("A-0039")
                    elif "Компуты" in title or "Глуховской сотни" in title:
                        r["artifact_id"] = "A-0040"
                        r["related_claim_ids"] = "C-0044"
                        r["person_ids"] = "P-0034;P-0035"
                        artifacts.append(r)
                        seen_aids.add("A-0040")
            else:
                artifacts.append(r)
                seen_aids.add(aid)

    with open("artifact-register.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields_a)
        writer.writeheader()
        writer.writerows(artifacts)
    print("artifact-register.csv: resolved to", len(artifacts), "artifacts (A-0001..A-0040).")

    # 3. Clean claims-register.csv
    claims = []
    seen_cids = set()
    with open("claims-register.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields_c = reader.fieldnames
        for r in reader:
            cid = r["claim_id"]
            if cid in ("C-0039", "C-0040", "C-0041"):
                if cid not in seen_cids:
                    # First time: Belovs
                    claims.append(r)
                    seen_cids.add(cid)
                else:
                    # Second time: Brinyuks
                    claim_text = r.get("claim_text", "")
                    if "Воинский подвиг" in claim_text or "Воронежского" in claim_text:
                        r["claim_id"] = "C-0042"
                        r["artifact_ids"] = "A-0033;A-0039"
                        claims.append(r)
                        seen_cids.add("C-0042")
                    elif "Авдей" in claim_text:
                        r["claim_id"] = "C-0043"
                        r["subject_person_ids"] = "P-0029;P-0033"
                        r["artifact_ids"] = "A-0034;A-0039"
                        claims.append(r)
                        seen_cids.add("C-0043")
                    elif "Коренное казацкое" in claim_text:
                        r["claim_id"] = "C-0044"
                        r["subject_person_ids"] = "P-0029;P-0033;P-0034;P-0035"
                        r["artifact_ids"] = "A-0034;A-0040"
                        claims.append(r)
                        seen_cids.add("C-0044")
            else:
                claims.append(r)
                seen_cids.add(cid)

    with open("claims-register.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields_c)
        writer.writeheader()
        writer.writerows(claims)
    print("claims-register.csv: resolved to", len(claims), "claims (C-0001..C-0044).")

    # 4. Clean relationship-register.csv
    relationships = []
    seen_rids = set()
    with open("relationship-register.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields_r = reader.fieldnames
        for r in reader:
            rid = r["relationship_id"]
            if rid in ("R-0029", "R-0030"):
                if rid not in seen_rids:
                    # First time: Belovs
                    relationships.append(r)
                    seen_rids.add(rid)
                else:
                    # Second time: Brinyuks
                    pa = r.get("person_a_id", "")
                    pb = r.get("person_b_id", "")
                    if pa in ("P-0030", "P-0033") or pb == "P-0029":
                        r["relationship_id"] = "R-0033"
                        r["person_a_id"] = "P-0033"
                        r["person_b_id"] = "P-0029"
                        r["claim_ids"] = "C-0042;C-0043"
                        r["supporting_artifact_ids"] = "A-0039"
                        r["independence_groups"] = "IG-RGVIA-GWAR"
                        relationships.append(r)
                        seen_rids.add("R-0033")
                    elif pa in ("P-0031", "P-0034"):
                        r["relationship_id"] = "R-0034"
                        r["person_a_id"] = "P-0034"
                        r["person_b_id"] = "P-0033"
                        r["claim_ids"] = "C-0044"
                        r["supporting_artifact_ids"] = "A-0040"
                        r["independence_groups"] = "IG-ARCHIVE-COSSACK"
                        relationships.append(r)
                        seen_rids.add("R-0034")
            else:
                relationships.append(r)
                seen_rids.add(rid)

    with open("relationship-register.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields_r)
        writer.writeheader()
        writer.writerows(relationships)
    print("relationship-register.csv: resolved to", len(relationships), "relationships (R-0001..R-0034).")

if __name__ == "__main__":
    main()
