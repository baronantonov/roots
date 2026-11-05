#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extend_baronov_branch.py:
Extends the Baronov lineage in dashboard.html to 7 generations:
P-0026 (Gen 7), P-0025 (Gen 6), P-0024 (Gen 5), P-0023 (Gen 4),
adds claims C-0030..C-0033, updates canvas coordinates, marriages,
filial links, and UI counts.
"""

import re
import json

P_0026_OBJ = """  {
    id: "P-0026",
    gen: 7,
    genRoman: "VII ПОКОЛЕНИЕ",
    genTitle: "Родоначальник прозвания Бароновых",
    genEra: "ок. 1785–1810 гг.",
    role: "Прапрапрапрадед (эпоним рода)",
    name: "Барон […] [родоначальник]",
    dates: "р. ок. 1785–1810 · ум. до 1858",
    place: "село Сольцы на Волхове, Новоладожский уезд",
    status: "hypothesis",
    statusClass: "st-hypo",
    badgeClass: "badge-hypo",
    namesAsWritten: "Барон (уличное прозвание / прозвищное именование домохозяина)",
    jurisdiction: "Солецкий погост, Новоладожский уезд Санкт-Петербургской губернии",
    occupation: "Крепостной крестьянин сельца Сольцы А. Ф. Бестужева, волховский артельщик / кормщик",
    relatives: "Сын: Баронов […] (P-0025); Внук: Баронов […] (P-0024); Правнук: Баронов Василий (P-0017)",
    rationale: "Патриарх и эпоним рода Бароновых села Сольцы (приход церкви Рождества Богородицы 1717 г.). По этимологии северо-западных говоров прозвище «Барон» присваивалось авторитетным, статным артельным старшинам на Волховских порогах. Проверяется по 8-й ревизии 1834 г. (ЦГИА СПб ф. 1646).",
    artifacts: ["A-0025", "A-0027"],
    story: "Седьмое поколение предков по отцу, живший в эпоху Отечественной войны 1812 года. Крепостной крестьянин старинного села Сольцы при имении Бестужевых. Обладал ярким, независимым нравом и могучим телосложением; водил купеческие караваны и барки через бурные Волховские пороги. За свой гордый характер, стать и непререкаемый авторитет в крестьянском мире заслужил уважительное прозвище «Барон», которое спустя полвека легло в основу официальной фамилии его потомков."
  },"""

P_0025_OBJ = """  {
    id: "P-0025",
    gen: 6,
    genRoman: "VI ПОКОЛЕНИЕ",
    genTitle: "Крестьянская реформа 1861 г. на Волхове",
    genEra: "ок. 1820–1840 гг.",
    role: "Прапрапрадед (реформа 1861 г.)",
    name: "Баронов […] [дед Василия]",
    dates: "р. ок. 1820–1835 · ум. после 1861",
    place: "село Сольцы, Новоладожский уезд Санкт-Петербургской губ.",
    status: "hypothesis",
    statusClass: "st-hypo",
    badgeClass: "badge-hypo",
    namesAsWritten: "Крестьянин-домохозяин имения Сольцы Бестужевых / Теглевых (10-я ревизия 1858 г.)",
    jurisdiction: "Солецкое сельское общество, Солецкая волость, Новоладожский уезд",
    occupation: "Помещичий крестьянин Бестужевых, с 1861 г. — временнообязанный крестьянин-собственник надела",
    relatives: "Отец: Барон […] (P-0026); Сын: Баронов […] (P-0024); Внук: Баронов Василий (P-0017)",
    rationale: "Крестьянин Солецкого имения Бестужевых, получивший личную свободу и выкупной земельный надел по уставной грамоте 1861 г. (РГИА ф. 577 оп. 35). Проверяется по 10-й ревизии 1858 г. и ревизским сказкам Новоладожского уезда в ЦГИА СПб (ф. 1646).",
    artifacts: ["A-0018", "A-0025"],
    story: "Прапрапрадед по отцовской линии. Родился крепостным крестьянином имения Сольцы, принадлежавшего дворянам Бестужевым (семье Александра Федосеевича Бестужева, где росли братья-декабристы). В феврале 1861 года встречал Манифест об отмене крепостного права в церкви Рождества Богородицы, подписал уставную грамоту и выкупил полевой надел на левом берегу Волхова (РГИА ф. 577 оп. 35). Стал родоначальником свободной ветви Бароновых."
  },"""

P_0024_OBJ = """  {
    id: "P-0024",
    gen: 5,
    genRoman: "V ПОКОЛЕНИЕ",
    genTitle: "Прапрадеды (пореформенная эпоха)",
    genEra: "ок. 1850–1865 гг.",
    role: "Прапрадед (отец Василия)",
    name: "Баронов […] [отец Василия]",
    dates: "р. ок. 1850–1865 · ум. до 1917",
    place: "село Сольцы / деревня Кириши, Новоладожский уезд",
    status: "hypothesis",
    statusClass: "st-hypo",
    badgeClass: "badge-hypo",
    namesAsWritten: "Баронов; отец Василия Баронова (по метрикам прихода с. Сольцы ок. 1880–1886 гг.)",
    jurisdiction: "Солецкая волость, Новоладожский уезд Санкт-Петербургской губернии",
    occupation: "Крестьянин села Сольцы, лесосплавщик на Волхове",
    relatives: "Отец: Баронов […] (P-0025); Сын: Баронов Василий (P-0017); Внук: Баронов Валентин Васильевич (P-0005)",
    rationale: "Отец прадеда Василия Баронова, представитель пореформенного поколения приволховских крестьян. Подлежит установлению через поиск записи о рождении сына Василия в метрических книгах церкви Рождества Богородицы с. Сольцы за 1880–1888 гг. (ЦГИА СПб ф. 19 оп. 125–127).",
    artifacts: ["A-0018", "A-0025", "A-0027"],
    story: "Прапрадед по отцовской линии. Родился на Волхове накануне великих реформ Александра II. Жил в селе Сольцы напротив деревни Кириши, занимался хлебопашеством, рыбной ловлей и сплавом плотов по своенравному порожистому Волхову. Прихожанин древней каменной церкви Рождества Богородицы (1717 г.). Воспитал сына Василия в строгих традициях северного крестьянского трудолюбия, верности своему роду и стойкости."
  },"""

P_0023_OBJ = """  {
    id: "P-0023",
    gen: 4,
    genRoman: "IV ПОКОЛЕНИЕ",
    genTitle: "Прадед, прабабушка и оккупация",
    genEra: "ок. 1890–1940-е гг.",
    role: "Прабабушка по отцу",
    name: "Баронова […] [мать Валентина]",
    dates: "р. ок. 1890–1905 · ум. 1940-е",
    place: "пос. Кириши (село Сольцы), Ленинградская обл.",
    status: "hypothesis",
    statusClass: "st-hypo",
    badgeClass: "badge-hypo",
    namesAsWritten: "Баронова; мать Валентина Васильевича (1929 г.р.)",
    jurisdiction: "пос. Кириши (село Сольцы), Андреевский район Ленобласти",
    occupation: "Крестьянка, жительница прифронтового посёлка Кириши",
    relatives: "Супруг: Баронов Василий (P-0017); Сын: Баронов Валентин Васильевич (P-0005); Внук: Баронов Вадим Валентинович (P-0003)",
    rationale: "Мать деда Валентина Васильевича, разделившая с детьми трагедию оккупации Киришского плацдарма в 1941–1943 гг. Выявляется через запрос в ЦГА СПб (ф. Р-6143) по актовой записи о рождении сына Валентина от 01.05.1929.",
    artifacts: ["A-0018", "A-0019", "A-0026"],
    story: "Прабабушка по отцовской линии, хранительница очага семьи Бароновых на берегах Волхова. Когда в сентябре 1941 года гитлеровские войска подошли к Киришам и заняли посёлок, на её плечи легла нечеловеческая задача — спасти детей от голодной смерти и артобстрелов в зоне двухлетнего позиционного ада Киришского плацдарма. В условиях тотального голода и разрухи сумела уберечь 12-летнего сына Валентина, который навсегда сохранил память о её самоотверженности и материнской заботе."
  },"""

NEW_CLAIMS_BLOCK = """  { id: "C-0030", text: "Прабабушка по отцу — Баронова […] (P-0023), супруга Василия (P-0017) и мать Валентина (P-0005), жительница Киришей, пережившая оккупацию Киришского плацдарма 1941–1943 гг.", status: "corroborated", statusRu: "Подтверждено", badge: "badge-corr", arts: "A-0018; A-0019; A-0026", groups: "IG-HIST-KIRISHI-RGIA; IG-USER-01; IG-KIRISHI-BRIDGEHEAD" },
  { id: "C-0031", text: "Прапрадед по отцу — Баронов […] (P-0024), крестьянин с. Сольцы / д. Кириши Солецкой волости Новоладожского уезда, отец Василия Баронова (P-0017)", status: "hypothesis", statusRu: "Архивный поиск", badge: "badge-hypo", arts: "A-0018; A-0025; A-0027", groups: "IG-HIST-KIRISHI-RGIA; IG-BESTUZHEV-SOLTSY; IG-TSGIA-SPB-SOLTSY" },
  { id: "C-0032", text: "Прапрапрадед — Баронов […] (P-0025), временнообязанный крестьянин имения Сольцы Бестужевых эпохи отмены крепостного права 1861 г. (РГИА ф. 577 оп. 35)", status: "hypothesis", statusRu: "Архивный поиск", badge: "badge-hypo", arts: "A-0018; A-0025", groups: "IG-HIST-KIRISHI-RGIA; IG-BESTUZHEV-SOLTSY" },
  { id: "C-0033", text: "Родоначальник прозвания Бароновых — Барон […] (P-0026), патриарх волховского рода села Сольцы прихода церкви Рождества Богородицы (1717 г.), рубеж XVIII–XIX вв.", status: "hypothesis", statusRu: "Архивный поиск", badge: "badge-hypo", arts: "A-0025; A-0027", groups: "IG-BESTUZHEV-SOLTSY; IG-TSGIA-SPB-SOLTSY" }"""

def main():
    path = "/home/brnv/projects/ROOTS/dashboard.html"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Update counts in header and tabs
    html = html.replace("<strong>22</strong> персоны", "<strong>26</strong> персон")
    html = html.replace("Все персоны (22)", "Все персоны (26)")
    html = html.replace("🔍 Найти предка...", "🔍 Найти персону в древе (26)...")
    html = html.replace("🔍 Найти персону в древе (22)...", "🔍 Найти персону в древе (26)...")
    html = html.replace('<button class="nav-tab-btn active" data-tab="tab-tree" onclick="activateTab(\'tab-tree\')">\n        <span>🌳 Древо</span>\n        <span class="nav-count">22</span>', '<button class="nav-tab-btn active" data-tab="tab-tree" onclick="activateTab(\'tab-tree\')">\n        <span>🌳 Древо</span>\n        <span class="nav-count">26</span>')
    html = html.replace("Genealogical Proof Standard — 29 фактов", "Genealogical Proof Standard — 33 факта")
    html = html.replace('<button class="nav-tab-btn" data-tab="tab-queue" onclick="activateTab(\'tab-queue\')">\n        <span>📑 Запросы GPS</span>\n        <span class="nav-count">29</span>', '<button class="nav-tab-btn" data-tab="tab-queue" onclick="activateTab(\'tab-queue\')">\n        <span>📑 Запросы GPS</span>\n        <span class="nav-count">33</span>')

    # 2. Insert P-0026 right after P-0015
    p15_pat = re.compile(r'(id:\s*\"P-0015\"[\s\S]*?story:\s*\"[\s\S]*?\"\s*\})(,)', re.MULTILINE)
    m15 = p15_pat.search(html)
    if m15 and "P-0026" not in html:
        html = html[:m15.end(1)] + ",\n" + P_0026_OBJ + html[m15.end(2):]
        print("Inserted P-0026!")
    else:
        print("Notice: P-0015 match failed or P-0026 already present")

    # 3. Insert P-0025 right after P-0010
    p10_pat = re.compile(r'(id:\s*\"P-0010\"[\s\S]*?story:\s*\"[\s\S]*?\"\s*\})(,)', re.MULTILINE)
    m10 = p10_pat.search(html)
    if m10 and "P-0025" not in html:
        html = html[:m10.end(1)] + ",\n" + P_0025_OBJ + html[m10.end(2):]
        print("Inserted P-0025!")

    # 4. Insert P-0024 right after P-0020
    p20_pat = re.compile(r'(id:\s*\"P-0020\"[\s\S]*?story:\s*\"[\s\S]*?\"\s*\})(,)', re.MULTILINE)
    m20 = p20_pat.search(html)
    if m20 and "P-0024" not in html:
        html = html[:m20.end(1)] + ",\n" + P_0024_OBJ + html[m20.end(2):]
        print("Inserted P-0024!")

    # 5. Insert P-0023 right after P-0017
    p17_pat = re.compile(r'(id:\s*\"P-0017\"[\s\S]*?story:\s*\"[\s\S]*?\"\s*\})(,)', re.MULTILINE)
    m17 = p17_pat.search(html)
    if m17 and "P-0023" not in html:
        html = html[:m17.end(1)] + ",\n" + P_0023_OBJ + html[m17.end(2):]
        print("Inserted P-0023!")

    # 6. Append claims C-0030..C-0033
    claim29_target = 'groups: "IG-USER-01; IG-PETERHOF-AUTO-52611; IG-USER-FATHER" }\n];'
    claim_replacement = 'groups: "IG-USER-01; IG-PETERHOF-AUTO-52611; IG-USER-FATHER" },\n' + NEW_CLAIMS_BLOCK + '\n];'
    if claim29_target in html:
        html = html.replace(claim29_target, claim_replacement, 1)
        print("Appended claims C-0030..C-0033!")
    else:
        print("ERROR: could not find claim29_target!")

    # 7. Update CANVAS_COORDS
    old_coords_block = """  // Gen 7 (~1800)
  "P-0015": { x: 1620, y: 70, side: "mat" },

  // Gen 6 (1820-1861)
  "P-0010": { x: 1620, y: 270, side: "mat" },

  // Gen 5 (1860-1880)
  "P-0020": { x: 560,  y: 480, side: "pat" },
  "P-0009": { x: 1500, y: 480, side: "mat" },
  "P-0014": { x: 2050, y: 480, side: "mat" },

  // Gen 4 (1888-1915)
  "P-0017": { x: 80,   y: 720, side: "pat" },"""

    new_coords_block = """  // Gen 7 (~1800)
  "P-0026": { x: -80,  y: 70, side: "pat" },
  "P-0015": { x: 1620, y: 70, side: "mat" },

  // Gen 6 (1820-1861)
  "P-0025": { x: -80,  y: 270, side: "pat" },
  "P-0010": { x: 1620, y: 270, side: "mat" },

  // Gen 5 (1860-1880)
  "P-0024": { x: -80,  y: 480, side: "pat" },
  "P-0020": { x: 560,  y: 480, side: "pat" },
  "P-0009": { x: 1500, y: 480, side: "mat" },
  "P-0014": { x: 2050, y: 480, side: "mat" },

  // Gen 4 (1888-1915)
  "P-0017": { x: -160, y: 720, side: "pat" },
  "P-0023": { x: 160,  y: 720, side: "pat" },"""

    if old_coords_block in html:
        html = html.replace(old_coords_block, new_coords_block, 1)
        print("Updated CANVAS_COORDS!")
    else:
        print("WARNING: old_coords_block not found exactly!")

    # 8. Update CANVAS_MARRIAGES
    old_marr_block = '  { id: "m-4", p1: "P-0003", p2: "P-0002", date: "ок. 1985", children: ["P-0001"], side: "center" }\n];'
    new_marr_block = '  { id: "m-4", p1: "P-0003", p2: "P-0002", date: "ок. 1985", children: ["P-0001"], side: "center" },\n  { id: "m-5", p1: "P-0017", p2: "P-0023", date: "ок. 1920", children: ["P-0005"], side: "pat" }\n];'
    if old_marr_block in html:
        html = html.replace(old_marr_block, new_marr_block, 1)
        print("Added marriage m-5 to CANVAS_MARRIAGES!")

    # 9. Update CANVAS_FILIAL
    old_filial_target = '  { from: "P-0014", to: "P-0008", side: "mat" },\n  { from: "P-0017", to: "P-0005", side: "pat" },'
    new_filial_target = """  { from: "P-0014", to: "P-0008", side: "mat" },
  { from: "P-0026", to: "P-0025", side: "pat" },
  { from: "P-0025", to: "P-0024", side: "pat" },
  { from: "P-0024", to: "P-0017", side: "pat" },"""
    if old_filial_target in html:
        html = html.replace(old_filial_target, new_filial_target, 1)
        print("Updated CANVAS_FILIAL lines!")

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Dashboard extended with Baronov branch successfully!")

if __name__ == "__main__":
    main()
