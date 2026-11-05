#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
integrate_besm6_memoirs.py:
Integrate Nina Shepelenko's work on supercomputer BESM-6 calculating
ballistic missile trajectories and Vadim playing with punched cards.
"""

import json
import re

NINA_SHEPELENKO_STORY = """Жизнь Нины Александровны — это подлинная географическая и научно-техническая эпопея великой страны. Родилась в суровых степях Кустаная в семье потомков украинских переселенцев. В военном 1946 году, будучи десятилетней девочкой, держала мать за руку в очередях за гособеспечением по улице Толстого, 78: семья потеряла на фронте дядю-журналиста Григория. Спасаясь от послевоенной разрухи и голода, семья переехала в древний Самарканд. Юность Нины прошла среди солнца, глиняных дувалов, хлопковых полей и лазурных мозаик Шахи-Зинды.

Судьба совершила невероятный поворот, когда на её жизненном пути появился молодой офицер Валентин Баронов: с солнечного Востока она приехала на берега туманной Балтики, в Стрельну. Стала сердцем гарнизонного дома на улице Лодыгина, привнеся в строгий офицерский уклад южную теплоту, щедрость и непревзойдённый кулинарный талант.

Но была в её жизни и другая, совершенно секретная грань: в духе эпохи противостояния холодной войны Нина Александровна работала в закрытом ленинградском оборонном научно-исследовательском институте. На гигантских электронно-вычислительных машинах БЭСМ-6 она вела сложнейшие расчёты траекторий баллистических ракет стратегического назначения. Сверхсекретные задачи и результаты не подлежали разглашению даже дома, но отработанные перфокарты с дырочками попадали домой и служили забавными и любимыми игрушками для маленького сына Вадика."""

VADIM_STORY = """Родился и вырос в Стрельне на улице Лодыгина, в семье кадрового офицера-автомобилиста и сотрудницы секретного оборонного НИИ. Первые яркие детские воспоминания относятся к 1965 году, когда четырёхлетним мальчишкой ходил с родителями в гости в старинный стрельнинский деревянный дом — чудом уцелевший на передовой войны, со скрипучими деревянными лестницами и дубовыми перилами, отполированными до зеркального блеска сотнями рук.

Детство было пронизано романтикой и острым духом эпохи холодной войны: пока отец на мотоцикле «Урал» с коляской мчал семью на Финский залив или прилетал с учений с тяжёлым пистолетом Макарова на поясе, мама приносила с секретной работы на суперкомпьютере БЭСМ-6 перфокарты с дырочками, которые служили Вадику самыми необычными и весёлыми игрушками. По вечерам отец с засекреченным физиком-ядерщиком Калмановым яростно болели за футбол перед стареньким жёлтым «Волховом».

Вадим Валентинович стал главным хранителем священных реликвий военной династии: именно он сберёг под диваном подлинный офицерский тревожный чемоданчик отца майора Баронова с сохранившейся описью имущества, а также ветхий географический атлас с маршрутами тысяч километров военных командировок (Монголия, Китай, Иран, Польша, просторы СССР). Отец троих детей: Антона, Дарьи и Анастасии."""

NEW_ART_32 = """  "A-0032": {
    id: "A-0032",
    title: "Воспоминания Вадима Баронова о матери Н. А. Шепеленко: секретный НИИ, расчёт траекторий на БЭСМ-6, перфокарты",
    cipher: "case-intake.yaml · IG-USER-FATHER",
    img: null,
    quote: "«Моя мать работала в сверхсекретном НИИ на больших вычислительных машинах БЭСМ-6: проводился расчёт траекторий баллистических ракет, нацеленных на США. Домой попадали перфокарты с дырочками — были моими любимыми игрушками».",
    desc: "Свидетельство сына Вадима (1961 г.р.) о секретной математической и вычислительной работе матери Нины Александровны Шепеленко в эпоху холодной войны."
  }"""

NEW_CLAIM_34 = """  { id: "C-0034", text: "Профессиональная деятельность бабушки Н. А. Шепеленко (P-0016): работа в секретном оборонном НИИ Ленинграда на суперкомпьютере БЭСМ-6 по расчёту траекторий баллистических ракет", status: "corroborated", statusRu: "Подтверждено", badge: "badge-corr", arts: "A-0012; A-0031; A-0032", groups: "IG-USER-01; IG-USER-FATHER" }"""

def main():
    path = "/home/brnv/projects/ROOTS/dashboard.html"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Update counts
    html = html.replace("<strong>31</strong> арт.", "<strong>32</strong> арт.")
    html = html.replace('<span class="nav-count">33</span>', '<span class="nav-count">34</span>')
    html = html.replace("Genealogical Proof Standard — 33 факта", "Genealogical Proof Standard — 34 факта")

    # 2. Add A-0032 to ARTIFACTS
    art_target = 'desc: "Прямая запись воспоминаний сына Вадима (1961 г.р.) о детстве в Стрельне 1960-х гг. и подлинных вещественных реликвиях отца — офицерском тревожном чемодане и путевом атласе."\n  }\n};'
    art_replacement = 'desc: "Прямая запись воспоминаний сына Вадима (1961 г.р.) о детстве в Стрельне 1960-х гг. и подлинных вещественных реликвиях отца — офицерском тревожном чемодане и путевом атласе."\n  },\n' + NEW_ART_32 + '\n};'
    if art_target in html:
        html = html.replace(art_target, art_replacement, 1)
        print("Added A-0032 to ARTIFACTS!")
    else:
        print("ERROR: could not find art_target in dashboard.html!")
        return

    # 3. Add C-0034 to CLAIMS
    claims_target = 'groups: "IG-BESTUZHEV-SOLTSY; IG-TSGIA-SPB-SOLTSY" }\n];'
    claims_replacement = 'groups: "IG-BESTUZHEV-SOLTSY; IG-TSGIA-SPB-SOLTSY" },\n' + NEW_CLAIM_34 + '\n];'
    if claims_target in html:
        html = html.replace(claims_target, claims_replacement, 1)
        print("Added C-0034 to CLAIMS!")
    else:
        print("ERROR: could not find claims_target in dashboard.html!")
        return

    # 4. Update P-0016 in PERSONS
    pat16 = re.compile(r'(id:\s*\"P-0016\"[\s\S]*?artifacts:\s*\[[\s\S]*?\])[\s\S]*?(story:\s*\"[\s\S]*?\")(\s*\})')
    m16 = pat16.search(html)
    if m16:
        p16_head = m16.group(1)
        if '"A-0032"' not in p16_head:
            p16_head = p16_head.replace('artifacts: [', 'artifacts: ["A-0032", ')
        # Also update occupation
        p16_head = p16_head.replace('occupation: "Бухгалтер / служащая', 'occupation: "Специалист закрытого оборонного НИИ (ЭВМ БЭСМ-6), служащая')
        new_p16 = p16_head + f',\n    story: {json.dumps(NINA_SHEPELENKO_STORY, ensure_ascii=False)}' + m16.group(3)
        html = html[:m16.start()] + new_p16 + html[m16.end():]
        print("Updated P-0016 story, artifacts & occupation!")
    else:
        print("ERROR: could not match P-0016!")
        return

    # 5. Update P-0003 in PERSONS
    pat3 = re.compile(r'(id:\s*\"P-0003\"[\s\S]*?artifacts:\s*\[[\s\S]*?\])[\s\S]*?(story:\s*\"[\s\S]*?\")(\s*\})')
    m3 = pat3.search(html)
    if m3:
        p3_head = m3.group(1)
        if '"A-0032"' not in p3_head:
            p3_head = p3_head.replace('artifacts: [', 'artifacts: ["A-0032", ')
        new_p3 = p3_head + f',\n    story: {json.dumps(VADIM_STORY, ensure_ascii=False)}' + m3.group(3)
        html = html[:m3.start()] + new_p3 + html[m3.end():]
        print("Updated P-0003 story & artifacts!")
    else:
        print("ERROR: could not match P-0003!")
        return

    # 6. Update Timeline in tab-geo with BESM-6 note
    old_tl_item = "перед телевизором «Волхов» с засекреченным физиком ядерной программы СССР <b>Калмановым</b> (<code>[A-0031]</code>)."
    new_tl_item = """перед телевизором «Волхов» с засекреченным физиком ядерной программы СССР <b>Калмановым</b> (<code>[A-0031]</code>); в это же время мать <b>Нина Александровна Шепеленко</b> <span class="person-link-chip" onclick="openPersonFromAnywhere('P-0016')">P-0016</span> работает в закрытом оборонном НИИ Ленинграда на суперкомпьютере <b>БЭСМ-6</b> по расчёту траекторий баллистических ракет, принося домой перфокарты для детских игр Вадика (<code>[A-0032]</code>)."""
    if old_tl_item in html and "БЭСМ-6" not in html:
        html = html.replace(old_tl_item, new_tl_item, 1)
        print("Added BESM-6 details to timeline!")

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Dashboard updated with BESM-6 memories successfully!")

if __name__ == "__main__":
    main()
