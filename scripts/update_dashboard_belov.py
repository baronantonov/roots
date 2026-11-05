import re

def update_file(filepath):
    print(f"Updating {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add P-0030, P-0031, P-0032 to PERSONS array
    p30_obj = """  {
    id: "P-0030",
    gen: 4,
    genRoman: "IV ПОКОЛЕНИЕ",
    genTitle: "Старший брат прабабушки (репрессированная ветвь)",
    genEra: "1887 – после 1936 гг.",
    role: "Двоюродный прадед (брат Агриппины)",
    name: "Белов Фёдор Александрович",
    dates: "1887 – после 1936",
    place: "с. Галактионово (Жукотино) → дер. Дахново Новгородской обл.",
    status: "corroborated",
    statusClass: "st-corr",
    badgeClass: "badge-corr",
    namesAsWritten: "Белов Федор Александрович 1887 г.р.",
    jurisdiction: "село Никольское (Жукотино), Чистопольский уезд Казанской губ. / ТАССР",
    occupation: "Крестьянин с. Галактионово, грамотный, политзаключённый (ст. 58-10)",
    relatives: "Отец: Белов Александр (P-0014); Сестра: Евдокимова (Белова) Агриппина Александровна (P-0008); Сыновья: Иван 1911 (P-0032), Павел 1914 (P-0031)",
    rationale: "Родной старший брат прабабушки Агриппины Александровны Беловой (P-0008). Совпадение отчества Александрович, с. Галактионово (Жукотино) и поколения ровесников (1887 и 1889 гг.). Дважды репрессирован (1919 и 1935 гг., осужден Главсудом ТАССР к 3 годам лишения свободы по ст. 58-10). Реабилитирован 20.01.1997 [A-0036].",
    artifacts: ["A-0036", "A-0038"],
    story: "Родился в 1887 году в старинном селе Жукотино на реке Прость, старший брат прабабушки Агриппины. Был грамотным крестьянином. В революционные годы 31.01.1919 арестовывался, но через неделю дело прекратили. 17.09.1935 арестован Чистопольским РО НКВД по ст. 58-10 УК РСФСР ('антисоветская агитация') и осужден Главным судом ТАССР к 3 годам лагерей. Позднее жил в дер. Дахново Боровичского района Новгородской области. Полностью реабилитирован 20.01.1997."
  },
  {
    id: "P-0031",
    gen: 3,
    genRoman: "III ПОКОЛЕНИЕ",
    genTitle: "Двоюродные братья деда Шуры (фронтовики ВОВ)",
    genEra: "1914–1979 гг.",
    role: "Двоюродный брат деда (фронтовик)",
    name: "Белов Павел Фёдорович",
    dates: "1914–1979",
    place: "с. Галактионово Чистопольского р-на → г. Волжск, Марий Эл",
    status: "corroborated",
    statusClass: "st-corr",
    badgeClass: "badge-corr",
    namesAsWritten: "Белов Павел Федорович 1914 г.р.",
    jurisdiction: "с. Никольское (Жукотино), Чистопольский уезд / г. Волжск Марийской АССР",
    occupation: "Сержант 349-го артполка 119-й сд, фронтовик ВОВ, кавалер орденов и медалей",
    relatives: "Отец: Белов Фёдор Александрович (P-0030); Брат: Белов Иван Фёдорович (P-0032); Тётя: Евдокимова (Белова) Агриппина Александровна (P-0008); Двоюродный брат: Евдокимов Александр Николаевич (P-0004)",
    rationale: "Племянник прабабушки Агриппины Беловой, сын Фёдора Александровича Белова. Родился в с. Галактионово. Призван 05.03.1942 Волжским РВК. Награжден медалями «За боевые заслуги», «За отвагу», «За победу над Германией». Скончался в г. Волжске в 1979 г. [A-0037].",
    artifacts: ["A-0037", "A-0038"],
    story: "Родился в 1914 году в селе Галактионово в крестьянской семье Фёдора Белова. Призван на фронт 5 марта 1942 года. Прошел сквозь огонь тяжелейших боев артиллеристом 349-го артиллерийского полка 119-й стрелковой дивизии, лично поражал вражеские огневые точки, за мужество и отвагу был удостоен медалей «За отвагу» и «За боевые заслуги». После Победы жил и трудился в городе Волжске (Марий Эл), где скончался в 1979 году."
  },
  {
    id: "P-0032",
    gen: 3,
    genRoman: "III ПОКОЛЕНИЕ",
    genTitle: "Двоюродные братья деда Шуры",
    genEra: "1911 – после 1942 гг.",
    role: "Двоюродный брат деда (с. Галактионово)",
    name: "Белов Иван Фёдорович",
    dates: "р. 1911",
    place: "с. Галактионово Чистопольского района ТАССР",
    status: "corroborated",
    statusClass: "st-corr",
    badgeClass: "badge-corr",
    namesAsWritten: "Белов Иван Федорович 1911 г.р.",
    jurisdiction: "село Никольское (Жукотино), Чистопольский уезд Казанской губ.",
    occupation: "Крестьянин села Галактионово",
    relatives: "Отец: Белов Фёдор Александрович (P-0030); Брат: Белов Павел Фёдорович (P-0031); Тётя: Евдокимова (Белова) Агриппина Александровна (P-0008); Двоюродный брат: Евдокимов Александр Николаевич (P-0004)",
    rationale: "Старший сын Фёдора Александровича Белова, племянник Агриппины Беловой, уроженец с. Галактионово. Мобилизован в марте 1942 г. [A-0036].",
    artifacts: ["A-0036", "A-0038"],
    story: "Родился в 1911 году в селе Галактионово (Жукотино). Старший сын Фёдора Александровича Белова. Рос вместе с младшим братом Павлом и многочисленными двоюродными братьями Евдокимовыми (включая Сергея, Михаила и Шуру). В марте 1942 года был мобилизован на защиту Родины."
  }"""

    if '"P-0030"' not in content:
        # Insert before P-0029 ends or at end of PERSONS array
        # Find closing of PERSONS array
        m_persons = re.search(r'(const PERSONS\s*=\s*\[.*?)(  \{\s*id:\s*\"P-0029\".*?\n  \}\n)(\];)', content, re.DOTALL)
        if m_persons:
            new_persons_block = m_persons.group(1) + m_persons.group(2) + ",\n" + p30_obj + "\n" + m_persons.group(3)
            content = content[:m_persons.start()] + new_persons_block + content[m_persons.end():]
            print("Added P-0030, P-0031, P-0032 to PERSONS array.")
        else:
            print("Could not match PERSONS array insertion point!")

    # 2. Add C-0039, C-0040, C-0041 to CLAIMS array
    c39_obj = """  { id: "C-0039", text: "Старший брат прабабушки Агриппины Беловой — Белов Фёдор Александрович (P-0030, 1887 г.р., с. Галактионово), крестьянин, дважды репрессирован (1919, 1935 гг.), отбывал 3 года заключения, реабилитирован в 1997 г.", status: "corroborated", statusRu: "В архивах ✓", badge: "badge-corr", arts: "A-0004; A-0007; A-0036", groups: "IG-MEMORIAL-RT; IG-SELIKHOVA-TREE" },
  { id: "C-0040", text: "Двоюродный брат деда Шуры — Белов Павел Фёдорович (P-0031, 1914–1979, с. Галактионово → г. Волжск), гвардии сержант, артиллерист 349-го артполка 119-й сд, кавалер медалей «За отвагу» и «За боевые заслуги»", status: "corroborated", statusRu: "В архивах ✓", badge: "badge-corr", arts: "A-0036; A-0037", groups: "IG-MEMORIAL-RT; IG-CAMO-WW2" },
  { id: "C-0041", text: "Происхождение чистопольского рода Беловых из крепостных крестьян помещиков Аристовых села Никольское (Жукотино, «Савин Городок») Закамской засечной черты XVII века, прихожан Николаевской церкви (НА РТ ф. 3 оп. 2 д. 390; FamilySearch микрофильм 2344399)", status: "corroborated", statusRu: "В архивах ✓", badge: "badge-corr", arts: "A-0004; A-0036; A-0038", groups: "IG-NART-KAZAN; IG-MEMORIAL-RT" }"""

    if '"C-0039"' not in content:
        m_claims = re.search(r'(const CLAIMS\s*=\s*\[.*?)(  \{\s*id:\s*\"C-0038\".*?\n)(\];)', content, re.DOTALL)
        if m_claims:
            new_claims_block = m_claims.group(1) + m_claims.group(2).rstrip() + ",\n" + c39_obj + "\n" + m_claims.group(3)
            content = content[:m_claims.start()] + new_claims_block + content[m_claims.end():]
            print("Added C-0039..C-0041 to CLAIMS array.")

    # 3. Update CANVAS_COORDS with P-0030, P-0031, P-0032 and shifted Ukrainian branch
    old_coords_pat = r'const CANVAS_COORDS\s*=\s*\{.*?\n\};'
    m_coords = re.search(old_coords_pat, content, re.DOTALL)
    if m_coords:
        new_coords = """const CANVAS_COORDS = {
  // Gen 7 (~1800)
  "P-0026": { x: 40,   y: 70,  side: "pat" }, // Барон (родоначальник Бароновых)
  "P-0015": { x: 1660, y: 70,  side: "mat" }, // Евдоким (родоначальник Евдокимовых)

  // Gen 6 (1820-1861)
  "P-0025": { x: 40,   y: 280, side: "pat" }, // Баронов (сын Барона)
  "P-0010": { x: 1660, y: 280, side: "mat" }, // Михаил Евдокимович

  // Gen 5 (1860-1880)
  "P-0024": { x: 40,   y: 490, side: "pat" }, // Баронов [отец Василия]
  "P-0020": { x: 680,  y: 490, side: "pat" }, // Иван Шепеленко
  "P-0009": { x: 1660, y: 490, side: "mat" }, // Никандр Евдокимов
  "P-0014": { x: 2300, y: 490, side: "mat" }, // Александр Белов
  "P-0029": { x: 3340, y: 490, side: "mat" }, // Тимофей Бринюк (сдвинут)

  // Gen 4 (1888-1915)
  "P-0017": { x: 40,   y: 730, side: "pat" }, // Василий Баронов
  "P-0023": { x: 360,  y: 730, side: "pat" }, // Баронова [мать Валентина]
  "P-0018": { x: 680,  y: 730, side: "pat" }, // Клавдия Шепеленко
  "P-0019": { x: 1000, y: 730, side: "pat" }, // дед Степан
  "P-0012": { x: 1340, y: 730, side: "mat" }, // Ефим Евдокимов
  "P-0013": { x: 1660, y: 730, side: "mat" }, // Вера Евдокимова
  "P-0007": { x: 1980, y: 730, side: "mat" }, // Николай Евдокимов
  "P-0008": { x: 2300, y: 730, side: "mat" }, // Агриппина Белова
  "P-0030": { x: 2620, y: 730, side: "mat" }, // Фёдор Александрович Белов (брат Агриппины)
  "P-0027": { x: 3020, y: 730, side: "mat" }, // Афанасий Коваленко (сдвинут)
  "P-0028": { x: 3340, y: 730, side: "mat" }, // Серафима Бринюк (сдвинута)

  // Gen 3 (1926-1935)
  "P-0005": { x: 200,  y: 990, side: "pat" }, // Валентин Баронов
  "P-0016": { x: 680,  y: 990, side: "pat" }, // Нина Шепеленко
  "P-0004": { x: 2140, y: 990, side: "mat" }, // Александр Евдокимов
  "P-0031": { x: 2500, y: 990, side: "mat" }, // Павел Фёдорович Белов (ветеран ВОВ)
  "P-0032": { x: 2780, y: 990, side: "mat" }, // Иван Фёдорович Белов
  "P-0006": { x: 3180, y: 990, side: "mat" }, // Наталья Коваленко (сдвинута)

  // Gen 2 (1953-1961)
  "P-0003": { x: 440,  y: 1250, side: "pat" }, // Вадим Баронов
  "P-0002": { x: 2150, y: 1250, side: "mat" }, // Нина Евдокимова
  "P-0011": { x: 2630, y: 1250, side: "mat" }, // Виктор Евдокимов

  // Gen 1 (1988-2004)
  "P-0021": { x: 280,  y: 1500, side: "pat" }, // Дарья Баронова
  "P-0022": { x: 600,  y: 1500, side: "pat" }, // Анастасия Баронова
  "P-0001": { x: 1295, y: 1500, side: "self" }  // Антон Евдокимов
};"""
        content = content[:m_coords.start()] + new_coords + content[m_coords.end():]
        print("Updated CANVAS_COORDS.")

    # 4. Update CANVAS_FILIAL with Belov links
    old_filial_pat = r'const CANVAS_FILIAL\s*=\s*\[.*?\n\];'
    m_filial = re.search(old_filial_pat, content, re.DOTALL)
    if m_filial:
        new_filial = """const CANVAS_FILIAL = [
  // Paternal lineage
  { from: "P-0026", to: "P-0025", side: "pat" },
  { from: "P-0025", to: "P-0024", side: "pat" },
  { from: "P-0024", to: "P-0017", side: "pat" },
  { from: "P-0020", to: "P-0018", side: "pat" },
  { from: "P-0018", to: "P-0016", side: "pat" },
  { from: "P-0003", to: "P-0021", side: "pat" },
  { from: "P-0003", to: "P-0022", side: "pat" },

  // Maternal lineage
  { from: "P-0015", to: "P-0010", side: "mat" },
  { from: "P-0010", to: "P-0009", side: "mat" },
  { from: "P-0009", to: "P-0012", side: "mat" },
  { from: "P-0009", to: "P-0013", side: "mat" },
  { from: "P-0009", to: "P-0007", side: "mat" },
  { from: "P-0014", to: "P-0008", side: "mat" },
  { from: "P-0014", to: "P-0030", side: "mat" }, // Александр Белов -> Фёдор Белов
  { from: "P-0030", to: "P-0031", side: "mat" }, // Фёдор Белов -> Павел Белов
  { from: "P-0030", to: "P-0032", side: "mat" }, // Фёдор Белов -> Иван Белов
  { from: "P-0029", to: "P-0028", side: "mat" }
];"""
        content = content[:m_filial.start()] + new_filial + content[m_filial.end():]
        print("Updated CANVAS_FILIAL.")

    # 5. Update MAP_LOCATIONS to include Volzhsk and update Galaktionovo/Chistopol
    if '"volzhsk"' not in content:
        # Update galaktionovo
        content = content.replace(
            'persons: ["P-0015", "P-0010", "P-0009", "P-0007", "P-0008", "P-0012", "P-0004"]',
            'persons: ["P-0015", "P-0010", "P-0009", "P-0014", "P-0007", "P-0008", "P-0012", "P-0004", "P-0030", "P-0031", "P-0032"]'
        )
        content = content.replace(
            'persons: ["P-0013", "P-0014", "P-0007"]',
            'persons: ["P-0013", "P-0014", "P-0007", "P-0030"]'
        )

        volzhsk_loc = """,
  {
    id: "volzhsk",
    name: "город Волжск (Марийская АССР / Республика Марий Эл)",
    shortName: "г. Волжск",
    lat: 55.8647,
    lng: 48.3586,
    zoom: 12,
    icon: "🎖️",
    region: "Марийская АССР / Республика Марий Эл",
    branch: "evdokimov",
    branchLabel: "Ветвь Беловых (Марий Эл)",
    roleText: "Место призыва на фронт и послевоенной жизни ветерана Павла Фёдоровича Белова",
    description: "Сюда из села Галактионово переехал племянник прабабушки Агриппины Беловой — Павел Фёдорович Белов (P-0031). Отсюда 05.03.1942 Волжским РВК он был призван на фронт Великой Отечественной войны, прошел путь сержанта 349-го артиллерийского полка 119-й сд, был награжден медалями «За отвагу» и «За боевые заслуги», после Победы жил и трудился в Волжске до своей кончины в 1979 году.",
    persons: ["P-0031"]
  }"""
        # Insert before closing MAP_LOCATIONS
        m_map = re.search(r'(const MAP_LOCATIONS\s*=\s*\[.*?)(  \{\s*id:\s*\"surkhandarya\".*?\n  \}\n)(\];)', content, re.DOTALL)
        if m_map:
            new_map_block = m_map.group(1) + m_map.group(2).rstrip() + volzhsk_loc + "\n" + m_map.group(3)
            content = content[:m_map.start()] + new_map_block + content[m_map.end():]
            print("Added Volzhsk location to MAP_LOCATIONS.")

    # 6. Update badge counters from 29 relatives across 13 locations to 32 relatives across 14 locations
    content = content.replace("29 подтверждённых предков", "32 подтверждённых предка")
    content = content.replace("29 родственников", "32 родственника")
    content = content.replace("29 персон", "32 персоны")
    content = content.replace("13 географических локаций", "14 географических локаций")
    content = content.replace("13 локаций", "14 локаций")
    content = content.replace("13 очагов", "14 очагов")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved {filepath} successfully.")

update_file("dashboard.html")
update_file("index.html")
print("All dashboard files updated!")
