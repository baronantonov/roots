#!/usr/bin/env python3
"""
Финальная полировка всех реестров ROOTS и отчёта:
- artifact-register.csv: правильные колонки (13: provenance_level, 14: directness, 15: originality, 16: independence_group)
- claims-register.csv: соответствие заявленных групп и артефактов
- relationship-register.csv: соответствие групп
- final-report.md: обновление строки C-0015 и добавление C-0052..C-0055 в таблицу отчёта
"""

import csv
import os

BASE_DIR = "/home/brnv/projects/ROOTS"

def fix_all():
    # 1. ARTIFACTS
    art_path = os.path.join(BASE_DIR, "artifact-register.csv")
    with open(art_path, "r", encoding="utf-8") as f:
        art_rows = list(csv.reader(f))
    
    art_header = art_rows[0]
    art_data = art_rows[1:]

    for r in art_data:
        aid = r[0]
        if aid == "A-0047":
            r[13] = "archival-primary"
            r[14] = "direct"
            r[15] = "image-of-original"
            r[16] = "IG-RGVIA-BARONOV-POW"
            r[6] = "РГВИА, Картотека потерь (пленные), шкаф 3, ящик 5681-А, документ № 30199905 (кадры 1303, 1304)"
            r[20] = "C-0015;C-0052"
        elif aid == "A-0048":
            r[13] = "archival-primary"
            r[14] = "direct"
            r[15] = "image-of-original"
            r[16] = "IG-RGVIA-KOVALENKO-1915"
            r[6] = "РГВИА, Фонд 16196, оп. 1, дело 337, лист 99; Картотека потерь ящик 1473-К, док № 22127826"
            r[20] = "C-0053"
        elif aid == "A-0049":
            r[13] = "archival-primary"
            r[14] = "direct"
            r[15] = "image-of-original"
            r[16] = "IG-RGVIA-SHEPELENKO-1916"
            r[6] = "РГВИА, Фонд 16196, оп. 1, дело 743, лист 100; Картотека потерь ящик 3891-Ш, док № 20322563"
            r[20] = "C-0054"
        elif aid == "A-0050":
            r[13] = "archival-primary"
            r[14] = "direct"
            r[15] = "image-of-original"
            r[16] = "IG-RGVIA-EVDOKIMOV-POW"
            r[6] = "РГВИА, Картотека потерь (пленные), ящик 6047-А, кадры 3001-3002 (doc ID 30649737)"
            r[20] = "C-0010;C-0055"

    with open(art_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(art_header)
        w.writerows(art_data)
    print("artifact-register.csv saved")

    # 2. CLAIMS
    claims_path = os.path.join(BASE_DIR, "claims-register.csv")
    with open(claims_path, "r", encoding="utf-8") as f:
        claim_rows = list(csv.reader(f))
    
    claim_header = claim_rows[0]
    claim_data = claim_rows[1:]

    for r in claim_data:
        cid = r[0]
        if cid == "C-0015":
            r[4] = "A-0012;A-0017;A-0018;A-0047"
            r[5] = "IG-USER-01;IG-HIST-KIRISHI-RGIA;IG-RGVIA-BARONOV-POW"
            r[7] = "strongly-corroborated"
            r[8] = "high"
        elif cid == "C-0052":
            r[4] = "A-0012;A-0017;A-0047"
            r[5] = "IG-USER-01;IG-RGVIA-BARONOV-POW"
            r[7] = "strongly-corroborated"
            r[8] = "high"
        elif cid == "C-0053":
            r[4] = "A-0048"
            r[5] = "IG-RGVIA-KOVALENKO-1915"
            r[7] = "single-source"
            r[8] = "high"
        elif cid == "C-0054":
            r[4] = "A-0049"
            r[5] = "IG-RGVIA-SHEPELENKO-1916"
            r[7] = "single-source"
            r[8] = "high"
        elif cid == "C-0055":
            r[4] = "A-0008;A-0010;A-0050"
            r[5] = "IG-RGVIA-LOSS-127PP;IG-RGVIA-POW-CARD;IG-RGVIA-EVDOKIMOV-POW"
            r[7] = "strongly-corroborated"
            r[8] = "high"

    with open(claims_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(claim_header)
        w.writerows(claim_data)
    print("claims-register.csv saved")

    # 3. RELATIONSHIPS
    rel_path = os.path.join(BASE_DIR, "relationship-register.csv")
    with open(rel_path, "r", encoding="utf-8") as f:
        rel_rows = list(csv.reader(f))
    
    rel_header = rel_rows[0]
    rel_data = rel_rows[1:]

    for r in rel_data:
        rid = r[0]
        if rid == "R-0042":
            r[6] = "A-0048"
            r[8] = "IG-RGVIA-KOVALENKO-1915"
            r[9] = "single-source"
            r[10] = "high"
        elif rid == "R-0043":
            r[6] = "A-0048"
            r[8] = "IG-RGVIA-KOVALENKO-1915"
            r[9] = "hypothesis"
            r[10] = "medium"
        elif rid == "R-0044":
            r[6] = "A-0048"
            r[8] = "IG-RGVIA-KOVALENKO-1915"
            r[9] = "hypothesis"
            r[10] = "medium"
        elif rid == "R-0045":
            r[6] = "A-0049"
            r[8] = "IG-RGVIA-SHEPELENKO-1916"
            r[9] = "single-source"
            r[10] = "medium"

    with open(rel_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(rel_header)
        w.writerows(rel_data)
    print("relationship-register.csv saved")

    # 4. FINAL-REPORT.MD
    rep_path = os.path.join(BASE_DIR, "final-report.md")
    with open(rep_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if line.startswith("| `C-0015` |"):
            new_lines.append("| `C-0015` | Прадед по отцу — Баронов Василий (`P-0017`, 1886 г.р.); уроженец Петроградской губернии (Новоладожский уезд / Кириши), рядовой 54-го Минского полка, взят в плен 01.05.1915, содержался в лагере Терезиенштадт (Австро-Венгрия), волховский лоцман | `strongly-corroborated` | `[A-0012; A-0017; A-0018; A-0047]` | нет | 100% подтверждение семейного предания и имени деда первичной карточкой военнопленного РГВИА (ящик 5681-А) |\n")
        else:
            new_lines.append(line)
            if line.startswith("| `C-0051` |"):
                # Добавляем C-0052..C-0055
                new_lines.append("| `C-0052` | Прямое документальное подтверждение личности, возраста и боевого пути прадеда Василия Баронова (`P-0017`, 1886 г.р., Петроградская губ., рядовой 54-го Минского полка, взят в плен 01.05.1915 при Горлицком прорыве, содержался в лагере Терезиенштадт) | `strongly-corroborated` | `[A-0012; A-0017; A-0047]` | нет | Подтверждено первичной архивной карточкой военнопленного РГВИА (ящик 5681-А док 30199905) и семейным свидетельством сына Валентина и внука Вадима Баронова |\n")
                new_lines.append("| `C-0053` | Боевой путь и ранение комбатанта Первой мировой войны Коваленко (Ковальченко) Филиппа Андреевича (`P-0040`) из с. Землянка (173-й Каменецкий полк, ранен 22.07.1915 у Паникев-Малая) и патронимическая ветвь Андрея Коваленко (`P-0041`) | `single-source` | `[A-0048]` | нет | Первичные документы РГВИА (ящик 1473-К и ф. 16196 оп. 1 д. 337 л. 99) по селу Землянка (код 329318) |\n")
                new_lines.append("| `C-0054` | Фронтовик-переселенец Кустанайского уезда Шепеленко Сергей Никитич (`P-0042`, 20-й стрелковый полк, ранен дважды в 1916 г.), подтверждающий укоренение рода Шепеленко в Кустанайском уезде (Алексеевская вол.) | `single-source` | `[A-0049]` | нет | Списки потерь 20-го стрелкового полка РГВИА (ф. 16196 оп. 1 д. 743 л. 100) и картотека потерь (ящик 3891-Ш) |\n")
                new_lines.append("| `C-0055` | Первичная документация военного плена Николая Никандровича Евдокимова (`P-0007`) в лагере Дейч-Габель и фиксация исторического статуса села Савин-Городок (Жукотино) в фондах РГВИА | `strongly-corroborated` | `[A-0008; A-0010; A-0050]` | нет | Первичная двусторонняя карточка военнопленного ящика 6047-А РГВИА и донесения Старо-Иванаевской волости (код 399331) |\n")

    with open(rep_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("final-report.md saved")

if __name__ == "__main__":
    fix_all()
