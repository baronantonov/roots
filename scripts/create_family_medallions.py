#!/usr/bin/env python3
"""
Генерация архивных медальонов для папы, мамы и бабушки:
P-0002: Евдокимова Нина Александровна (мама)
P-0003: Баронов Вадим Валентинович (отец)
P-0016: Шепеленко Нина Степановна (бабушка Нина)
"""

import os
from PIL import Image, ImageDraw, ImageFont

def make_family_medallion(meta, out_dir="/home/brnv/projects/ROOTS/photos"):
    w, h = 400, 533
    bg_color = (244, 241, 236)
    circle_bg = (253, 254, 248)
    
    im = Image.new("RGB", (w, h), bg_color)
    draw = ImageDraw.Draw(im)

    # Шрифты
    font_bold = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
    font_italic = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"

    f_id = ImageFont.truetype(font_bold, 17)
    f_mono = ImageFont.truetype(font_bold, 86)
    f_name = ImageFont.truetype(font_bold, 21)
    f_dates = ImageFont.truetype(font_bold, 18)
    f_sub = ImageFont.truetype(font_italic, 15)
    f_footer = ImageFont.truetype(font_italic, 13)

    accent = meta["accent"]

    # 1. Внешняя тонкая рамка
    draw.rectangle([12, 12, w-13, h-13], outline=accent, width=1)
    # Угловые маркеры рамки
    for cx_box, cy_box in [(12, 12), (w-13, 12), (12, h-13), (w-13, h-13)]:
        draw.rectangle([cx_box-3, cy_box-3, cx_box+3, cy_box+3], outline=accent, fill=bg_color, width=1)

    # 2. Плашка с ID персоны вверху (y: 35..55)
    id_text = meta["id"]
    id_w = draw.textlength(id_text, font=f_id)
    id_box_w = id_w + 22
    id_box_h = 20
    id_x = (w - id_box_w) / 2
    id_y = 35
    draw.rectangle([id_x, id_y, id_x + id_box_w, id_y + id_box_h], fill=accent)
    draw.text((id_x + 11, id_y + 1), id_text, fill=(255, 255, 255), font=f_id)

    # 3. Центральный круг-медальон (начинается на y=58, заканчивается на y=346)
    circle_r = 144
    cx, cy = w / 2, 203
    draw.ellipse([cx - circle_r, cy - circle_r, cx + circle_r, cy + circle_r], fill=circle_bg, outline=accent, width=2)
    # Внутреннее тонкое кольцо
    draw.ellipse([cx - circle_r + 4, cy - circle_r + 4, cx + circle_r - 4, cy + circle_r - 4], outline=(225, 220, 210), width=1)

    # 4. Монограмма (крупные инициалы)
    mono = meta["initials"]
    mono_w = draw.textlength(mono, font=f_mono)
    draw.text(((w - mono_w) / 2, cy - 48), mono, fill=accent, font=f_mono)

    # 5. Имя и фамилия
    y_text = 368
    n1_w = draw.textlength(meta["line1"], font=f_name)
    draw.text(((w - n1_w) / 2, y_text), meta["line1"], fill=(35, 30, 25), font=f_name)

    y_text += 26
    n2_w = draw.textlength(meta["line2"], font=f_name)
    draw.text(((w - n2_w) / 2, y_text), meta["line2"], fill=(35, 30, 25), font=f_name)

    # 6. Даты жизни
    y_text += 34
    d_w = draw.textlength(meta["dates"], font=f_dates)
    draw.text(((w - d_w) / 2, y_text), meta["dates"], fill=accent, font=f_dates)

    # 7. Роль и место
    y_text += 28
    r_w = draw.textlength(meta["role"], font=f_sub)
    draw.text(((w - r_w) / 2, y_text), meta["role"], fill=(100, 95, 85), font=f_sub)

    # 8. Футер
    footer_text = "ГЕНЕАЛОГИЧЕСКИЙ АРХИВ РОДА · ROOTS"
    foot_w = draw.textlength(footer_text, font=f_footer)
    draw.text(((w - foot_w) / 2, h - 30), footer_text, fill=(150, 140, 130), font=f_footer)

    out_file = os.path.join(out_dir, meta["filename"])
    im.save(out_file, quality=95)
    print(f"Created: {out_file}")

ITEMS = [
    {
        "id": "P-0002",
        "initials": "НЕ",
        "line1": "Евдокимова Нина",
        "line2": "Александровна",
        "dates": "род. 1956",
        "role": "мама · Ленинград / Санкт-Петербург",
        "accent": (140, 45, 25),
        "filename": "portrait-p-0002-medallion.jpg"
    },
    {
        "id": "P-0003",
        "initials": "БВ",
        "line1": "Баронов Вадим",
        "line2": "Валентинович",
        "dates": "род. 1961",
        "role": "отец · Стрельна / Санкт-Петербург",
        "accent": (30, 78, 121),
        "filename": "portrait-p-0003-medallion.jpg"
    },
    {
        "id": "P-0016",
        "initials": "ШН",
        "line1": "Шепеленко Нина",
        "line2": "Степановна",
        "dates": "1935–2011",
        "role": "бабушка Нина · Самарканд / Ленинград",
        "accent": (42, 82, 122),
        "filename": "portrait-p-0016-medallion.jpg"
    }
]

if __name__ == "__main__":
    for item in ITEMS:
        make_family_medallion(item)
