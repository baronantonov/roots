#!/usr/bin/env python3
"""
Генерация архивных медальонов для новых персон рода ROOTS:
P-0040: Коваленко Филипп Андреевич (173-й пех. Каменецкий полк, с. Землянка)
P-0041: Коваленко Андрей (патриарх рода Коваленко с. Землянка)
P-0042: Шепеленко Сергей Никитич (20-й стрелковый полк, Кустанайский уезд)
"""

import os
from PIL import Image, ImageDraw, ImageFont

MEDALLIONS = [
    {
        "id": "portrait-p-0040-medallion.jpg",
        "name": "ФИЛИППЪ",
        "patronym": "АНДРЕЕВИЧЪ",
        "surname": "КОВАЛЕНКО",
        "dates": "ок. 1885 – 1915..1940",
        "status": "173-й пех. Каменецкій полкъ",
        "symbol": "⚔️",
        "note": "с. Землянка • Глуховскій уѣздъ",
        "bg_tone": (245, 242, 235),
        "frame_tone": (95, 75, 55),
        "gold_tone": (180, 140, 80)
    },
    {
        "id": "portrait-p-0041-medallion.jpg",
        "name": "АНДРЕЙ",
        "patronym": "—",
        "surname": "КОВАЛЕНКО",
        "dates": "ок. 1855 – ок. 1920",
        "status": "Хлѣбопашецъ / Патріархъ рода",
        "symbol": "🌾",
        "note": "с. Землянка • Глуховскій уѣздъ",
        "bg_tone": (246, 243, 236),
        "frame_tone": (85, 70, 50),
        "gold_tone": (170, 135, 75)
    },
    {
        "id": "portrait-p-0042-medallion.jpg",
        "name": "СЕРГѢЙ",
        "patronym": "НИКИТИЧЪ",
        "surname": "ШЕПЕЛЕНКО",
        "dates": "ок. 1890 – 1916..1950",
        "status": "20-й стрѣлковый полкъ",
        "symbol": "🎖️",
        "note": "пос. Васильевскій • Кустанай",
        "bg_tone": (244, 241, 234),
        "frame_tone": (90, 75, 60),
        "gold_tone": (175, 140, 80)
    }
]

def make_medallion(meta, out_dir="photos"):
    w, h = 400, 533
    im = Image.new("RGB", (w, h), meta["bg_tone"])
    draw = ImageDraw.Draw(im)

    # Загружаем шрифты
    font_serif = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
    font_bold = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
    font_italic = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"

    f_title = ImageFont.truetype(font_bold, 24)
    f_sub = ImageFont.truetype(font_serif, 17)
    f_small = ImageFont.truetype(font_italic, 15)
    f_micro = ImageFont.truetype(font_serif, 14)
    f_sym = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)

    # 1. Внешняя винтажная рамка
    draw.rectangle([8, 8, w-9, h-9], outline=meta["gold_tone"], width=2)
    draw.rectangle([14, 14, w-15, h-15], outline=meta["frame_tone"], width=1)

    # 2. Овальный медальон
    oval_box = [30, 40, w-30, h-70]
    draw.ellipse(oval_box, outline=meta["gold_tone"], width=3)
    draw.ellipse([34, 44, w-34, h-74], outline=meta["frame_tone"], width=1)
    draw.ellipse([38, 48, w-38, h-78], outline=(220, 210, 195), width=1)

    # Угловые декоративные элементы
    for cx, cy in [(14, 14), (w-15, 14), (14, h-15), (w-15, h-15)]:
        draw.rectangle([cx-4, cy-4, cx+4, cy+4], fill=meta["gold_tone"])

    # Верхний заголовок (фамилия)
    y = 75
    text_w = draw.textlength(meta["surname"], font=f_title)
    draw.text(((w - text_w) / 2, y), meta["surname"], fill=meta["frame_tone"], font=f_title)

    # Имя и отчество
    y += 34
    full_name = f"{meta['name']} {meta['patronym']}"
    text_w = draw.textlength(full_name, font=f_sub)
    draw.text(((w - text_w) / 2, y), full_name, fill=(110, 90, 70), font=f_sub)

    # Разделительная золотая черта
    y += 32
    draw.line([(w/2 - 50, y), (w/2 + 50, y)], fill=meta["gold_tone"], width=1)
    draw.ellipse([w/2 - 3, y - 3, w/2 + 3, y + 3], fill=meta["gold_tone"])

    # Центральный сословный символ
    y += 45
    sym_w = draw.textlength(meta["symbol"], font=f_sym)
    draw.text(((w - sym_w) / 2, y), meta["symbol"], fill=meta["frame_tone"], font=f_sym)

    # Воинский / сословный статус
    y += 65
    status_w = draw.textlength(meta["status"], font=f_sub)
    draw.text(((w - status_w) / 2, y), meta["status"], fill=meta["frame_tone"], font=f_sub)

    # Локация / уезд
    y += 28
    note_w = draw.textlength(meta["note"], font=f_micro)
    draw.text(((w - note_w) / 2, y), meta["note"], fill=(120, 100, 80), font=f_micro)

    # Разделитель снизу
    y += 28
    draw.line([(w/2 - 40, y), (w/2 + 40, y)], fill=meta["gold_tone"], width=1)

    # Годы жизни / активности
    y += 20
    dates_w = draw.textlength(meta["dates"], font=f_small)
    draw.text(((w - dates_w) / 2, y), meta["dates"], fill=(130, 95, 55), font=f_small)

    # Нижняя подпись архива
    arch_label = "АРХИВЪ РОДА ROOTS • РГВІА"
    arch_w = draw.textlength(arch_label, font=f_micro)
    draw.text(((w - arch_w) / 2, h - 35), arch_label, fill=(140, 120, 100), font=f_micro)

    out_path = os.path.join(out_dir, meta["id"])
    im.save(out_path, quality=95)
    print(f"Created: {out_path} ({w}x{h})")

def main():
    os.makedirs("photos", exist_ok=True)
    for m in MEDALLIONS:
        make_medallion(m)

if __name__ == "__main__":
    main()
