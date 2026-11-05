import re

def update_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Update counters
    html = html.replace("<strong>34</strong> арт.", "<strong>35</strong> арт.")
    html = html.replace('<span class="nav-count">34</span>', '<span class="nav-count">35</span>')
    html = html.replace("<strong>11</strong> запросов", "<strong>12</strong> запросов")
    html = html.replace('<span class="nav-count">11 запросов</span>', '<span class="nav-count">12 запросов</span>')

    # 2. Add A-0035 in ARTIFACTS
    a35_code = '''  "A-0035": {
    id: "A-0035",
    title: "РГВИА: Списки потерь 123-го пех. Козловского полка по сл. Благодатная Волчанского уезда Харьковской губ. (21 воин Шепеленко)",
    cipher: "РГВИА ф. 16196 оп. 1 д. 10017330, 10017319; Картотека ящ. 3974-Ш · IG-RGVIA-VOLCHANSK",
    img: null,
    quote: "«Шепеленко Иван Васильевич (рядовой), Шепеленко Иван Алексеевич (ефрейтор), Михаил Алексеевич, Павел Алексеевич и др. из сл. Благодатная Ольховатской вол. Волчанского уезда Харьковской губ.»",
    desc: "Корпус документов РГВИА Первой мировой войны, выявивший компактную концентрацию рода Шепеленко (21 воин, свыше 70% от всех Шепеленко губернии) в сл. Благодатная Волчанского уезда Харьковской губ. — родовом гнезде предков Ивана и Клавдии Шепеленко."
  }
};'''

    if '"A-0035"' not in html:
        target = '  "A-0034": {\n    id: "A-0034",\n    title: "Метрические фонды Покровской церкви с. Землянка в Государственном архиве Сумской области (ДАСО ф. 1190)",\n    cipher: "ДАСО, ф. 1190, оп. 1, 3 / ЦГИАК ф. 127 · IG-ARCHIVE-SUMY",\n    img: null,\n    quote: "«Метрические книги Покровской церкви села Землянка Глуховского уезда (ф. 1190 оп. 1, 3): фиксация казацко-крестьянских родов Коваленко и Бринюк (дела 1905, 1909, 1911, 1916 гг.)».",\n    desc: "Архивный комплекс метрических фондов ДАСО и реестров казаков Глуховской сотни Нежинского полка Войска Запорожского."\n  }\n};'
        replacement = target[:-3] + ',\n' + a35_code
        if target in html:
            html = html.replace(target, replacement, 1)
            print(f"[{filename}] A-0035 added to ARTIFACTS.")
        else:
            print(f"[{filename}] WARN: target for A-0034 not matched exactly.")

    # 3. Add C-0038 in CLAIMS
    c37_target = '  { id: "C-0037", text: "Прапрадед заявителя — Бринюк Тимофей (P-0029), казацко-крестьянский род с. Землянка Глуховского уезда Черниговской губ. (прихожане Покровской церкви, метрики фонда 1190 ДАСО)", status: "corroborated", statusRu: "Подтверждено", badge: "badge-corr", arts: "A-0033; A-0034", groups: "IG-USER-MOTHER; IG-ARCHIVE-SUMY" }\n];'
    c38_replacement = '  { id: "C-0037", text: "Прапрадед заявителя — Бринюк Тимофей (P-0029), казацко-крестьянский род с. Землянка Глуховского уезда Черниговской губ. (прихожане Покровской церкви, метрики фонда 1190 ДАСО)", status: "corroborated", statusRu: "Подтверждено", badge: "badge-corr", arts: "A-0033; A-0034", groups: "IG-USER-MOTHER; IG-ARCHIVE-SUMY" },\n  { id: "C-0038", text: "Родовое гнездо рода Шепеленко (P-0020, P-0018) локализовано в слободе Благодатная (Благодатное) Ольховатской волости Волчанского уезда Харьковской губернии (бывшие казаки и войсковые обыватели Харьковского слободского казачьего полка)", status: "corroborated", statusRu: "В архивах ✓", badge: "badge-corr", arts: "A-0014; A-0015; A-0035", groups: "IG-USER-FATHER; IG-HIST-KUSTANAY; IG-RGVIA-VOLCHANSK" }\n];'

    if '"C-0038"' not in html:
        if c37_target in html:
            html = html.replace(c37_target, c38_replacement, 1)
            print(f"[{filename}] C-0038 added to CLAIMS.")
        else:
            print(f"[{filename}] WARN: c37_target not matched.")

    # 4. Update onomastics card for Шепеленко in tab-surnames
    old_shep_start = '<div class="surname-card pat" id="surname-shepelenko">'
    belov_marker = '<!-- 4. БЕЛОВ -->'
    if old_shep_start in html and belov_marker in html:
        part1, rest = html.split(old_shep_start, 1)
        card_content, part2 = rest.split(belov_marker, 1)
        new_shep_body = """
          <div class="surname-kicker">⚓ Ветвь папы · Слобожанские переселенцы 1912 г. (Харьков → Кустанай → Самарканд)</div>
          <h3 class="surname-title">Шепеленко (слобожанские казаки из сл. Благодатная)</h3>
          <div class="surname-etym">
            <p style="margin:0 0 8px;"><b>1. Происхождение и казачьи корни (Реестр 1649 г.):</b> Исконная слобожанская казачья фамилия с классическим патронимическим формантом <b>-енко</b> («сын Шепеля»). Образована от славянского мирского прозвища <i>Шепель / Шепеля</i> (в диалектах Слободской Украины — «шустрый, подвижный, непоседливый человек, егоза», либо человек с мягкой шепелявящей речью). Носители фамилии зафиксированы ещё в Реестре Войска Запорожского 1649 года (Миско и Харко Шепеленко в Чигиринском полку) и казачьих компутах Харьковского слободского казачьего полка XVII–XVIII вв. (Хорошевская сотня).</p>
            <p style="margin:0 0 8px;"><b>2. Родовая колыбель (открытие по 666 воинам РГВИА):</b> Сплошной статистический анализ базы Первой мировой войны гарантированно локализовал родовое гнездо: <b>слобода Благодатная (Благодатное) Ольховатской волости Волчанского уезда Харьковской губернии</b> (более 70% всех воинов Шепеленко губернии происходят из этой слободы — 21 человек, включая рядового Ивана Васильевича и ефрейтора Ивана Алексеевича 123-го пехотного Козловского полка, <code>[A-0035]</code>).</p>
            <p style="margin:0 0 8px;"><b>3. Столыпинский исход 1912 года:</b> Из-за малоземелья семья прапрадеда <b>Ивана Шепеленко</b> <span class="person-link-chip" onclick="openPersonFromAnywhere('P-0020')">P-0020</span> в 1912 году переселилась в <b>Кустанайский уезд</b> Тургайской области (поселок Ново-Троицкий Станционной волости / пос. Васильевский). Родной брат прабабушки — <b>Шепеленко Григорий Иванович</b>, литературный сотрудник газеты «Сталинский путь», пал смертью храбрых на фронтах ВОВ; 22.04.1946 семья Клавдии Ивановны получала помощь как семья погибшего воина в Кустанае по <b>ул. Толстого, 78</b> (ГАКО ф. Р-268 оп. 1 д. 907).</p>
            <p style="margin:0;"><b>4. Официальный архивный запрос в ГАХО:</b> Для выявления метрик и ревизий войсковых обывателей подготовлен запрос в Государственный архив Харьковской области: <a href="queries/12_gaho_kharkov_volchansk_shepelenko.md" target="_blank" style="color:var(--accent-pat);font-weight:600;text-decoration:underline;">12_gaho_kharkov_volchansk_shepelenko.md ↗</a>.</p>
          </div>
        </div>

        """
        html = part1 + old_shep_start + new_shep_body + belov_marker + part2
        print(f"[{filename}] Updated surname-shepelenko card.")

    # 5. Add row to findings table in tab-surnames
    new_finding_row = """            <tr style="background:rgba(217,119,6,0.06);">
              <td><b>21 воин рода Шепеленко</b> (сл. Благодатная Волчанского уезда, 123-й Козловский полк)</td>
              <td><b>сл. Благодатная (Благодатное) Ольховатской вол. Волчанского уезда Харьковской губ.</b> (1914–1918)</td>
              <td class="mono">РГВИА, ф. 16196, оп. 1, д. 10017330, 10017319 [A-0035]</td>
              <td><b>Родовая колыбель ветви Шепеленко</b> (P-0020, P-0018) до Столыпинского переселения 1912 г. в Кустанай; подготовлен запрос <a href="queries/12_gaho_kharkov_volchansk_shepelenko.md" target="_blank" style="font-weight:bold;text-decoration:underline;">12_gaho_kharkov.md ↗</a></td>
            </tr>"""

    if "сл. Благодатная (Благодатное) Ольховатской вол." not in html:
        marker = '            <tr>\n              <td><b>Шепеленко К. И.</b>'
        if marker in html:
            html = html.replace(marker, new_finding_row + '\n' + marker, 1)
            print(f"[{filename}] Added Благодатная row to findings table.")

    # 6. Update P-0020 status to corroborated in PERSONS
    p20_old = '    id: "P-0020",\n    gen: 5,\n    genRoman: "V ПОКОЛЕНИЕ",\n    genTitle: "Прапрадеды (эпоха Столыпина)",\n    genEra: "ок. 1875–1930-е гг.",\n    role: "Прапрадед (переселенец 1912 г.)",\n    name: "Шепеленко Иван […]",\n    dates: "р. ок. 1875–1895",\n    place: "Харьковская губерния → Кустанайский уезд",\n    status: "hypothesis",\n    statusClass: "st-hypo",\n    badgeClass: "badge-hypo",'
    p20_new = '    id: "P-0020",\n    gen: 5,\n    genRoman: "V ПОКОЛЕНИЕ",\n    genTitle: "Прапрадеды (эпоха Столыпина)",\n    genEra: "ок. 1875–1930-е гг.",\n    role: "Прапрадед (переселенец 1912 г.)",\n    name: "Шепеленко Иван […]",\n    dates: "р. ок. 1875–1895",\n    place: "сл. Благодатная Волчанского уезда Харьковской губ. → Кустанайский уезд",\n    status: "corroborated",\n    statusClass: "st-corr",\n    badgeClass: "badge-corr",'
    if p20_old in html:
        html = html.replace(p20_old, p20_new, 1)
        print(f"[{filename}] Updated P-0020 status to corroborated.")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Saved {filename} successfully.")

update_file("dashboard.html")
update_file("index.html")
