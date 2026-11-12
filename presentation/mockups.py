# -*- coding: utf-8 -*-
"""Векторные макеты интерфейса по XAML-разметке приложения."""
from reportlab.lib.colors import HexColor
from theme import *

SIDEBAR = HexColor("#253D5B")
SIDEBAR_ACTIVE = HexColor("#3E5A7E")
HEADER = HexColor("#5B9BD5")
CONTENT_BG = HexColor("#F4F7F9")
TITLEBAR = HexColor("#1A2A3F")


def cut(s, font, size, max_w):
    s = str(s)
    if sw(s, font, size) <= max_w:
        return s
    while s and sw(s + "…", font, size) > max_w:
        s = s[:-1]
    return s + "…"


def mock_button(c, x, y, w, h, label, fill=BLUE, fg=WHITE, size=5.0, r=2):
    rounded(c, x, y, w, h, r=r, fill=fill, stroke=None)
    text(c, x + w / 2, y + h / 2 - size * 0.35, label, FONT_B, size, fg, "c")


def mock_input(c, x, y, w, h, value="", placeholder="", size=5.0):
    rounded(c, x, y, w, h, r=2, fill=WHITE, stroke=HexColor("#C9D4E2"))
    if value:
        text(c, x + 4, y + h / 2 - size * 0.35, cut(value, FONT, size, w - 8), FONT, size, TEXT)
    elif placeholder:
        text(c, x + 4, y + h / 2 - size * 0.35, placeholder, FONT, size, MUTED_2)


def mock_table(c, x, top, widths, headers, rows, row_h=15, font=5.2, header_h=12,
               aligns=None, row_colors=None, header_fill=HexColor("#F1F5FA")):
    total = sum(widths)
    c.setFillColor(header_fill)
    c.rect(x, top - header_h, total, header_h, fill=1, stroke=0)
    cx = x
    for i, h in enumerate(headers):
        text(c, cx + 4, top - header_h + 4, h.upper(), FONT_B, 4.4, MUTED)
        cx += widths[i]
    y = top - header_h
    for ri, row in enumerate(rows):
        y -= row_h
        if ri % 2 == 1:
            c.setFillColor(HexColor("#FAFBFD"))
            c.rect(x, y, total, row_h, fill=1, stroke=0)
        c.setStrokeColor(HexColor("#EDF1F6"))
        c.setLineWidth(0.4)
        c.line(x, y, x + total, y)
        cx = x
        for ci, cell in enumerate(row):
            al = (aligns or ["l"] * len(row))[ci]
            col = TEXT
            if row_colors and (ri, ci) in row_colors:
                col = row_colors[(ri, ci)]
            fnt = FONT_B if ci == 0 else FONT
            val = cut(cell, fnt, font, widths[ci] - 8)
            if al == "r":
                text(c, cx + widths[ci] - 4, y + row_h / 2 - font * 0.35, val, fnt, font, col, "r")
            elif al == "c":
                text(c, cx + widths[ci] / 2, y + row_h / 2 - font * 0.35, val, fnt, font, col, "c")
            else:
                text(c, cx + 4, y + row_h / 2 - font * 0.35, val, fnt, font, col)
            cx += widths[ci]
    return y


MENU = [
    ("Главная", "dashboard"), ("Товары", "products"), ("Приход", "income"),
    ("Расход", "outcome"), ("Инвентаризация", "inventory"), ("История операций", "history"),
    (None, None), ("Отчёты", "reports"), ("Пользователи", "users"), ("Настройки", "settings"),
    (None, None), ("Помощник", "chat"), ("Техподдержка", "support"),
]


def app_window(c, x, y, w, h, active, content, role="Администратор",
               user="Иванов Иван Иванович", sidebar=True):
    # тень
    c.saveState()
    c.setFillColor(HexColor("#DCE3ED"))
    c.roundRect(x + 3, y - 3, w, h, 7, fill=1, stroke=0)
    c.restoreState()
    rounded(c, x, y, w, h, r=6, fill=WHITE, stroke=HexColor("#C9D4E2"))

    # заголовок окна
    c.setFillColor(TITLEBAR)
    c.roundRect(x, y + h - 16, w, 16, 6, fill=1, stroke=0)
    c.rect(x, y + h - 16, w, 6, fill=1, stroke=0)
    for i, col in enumerate([HexColor("#E06C60"), HexColor("#E8B45A"), HexColor("#61B87A")]):
        c.setFillColor(col)
        c.circle(x + 9 + i * 7, y + h - 8, 2.2, fill=1, stroke=0)
    text(c, x + w / 2, y + h - 10.5, "Складской учёт PRO", FONT_B, 4.8, HexColor("#AFC0D6"), "c")

    sb = 112 if sidebar else 0
    # сайдбар
    if sidebar:
        c.setFillColor(SIDEBAR)
        c.roundRect(x, y, sb, h - 16, 6, fill=1, stroke=0)
        c.rect(x + sb - 6, y, 6, h - 16, fill=1, stroke=0)
        c.setFillColor(ORANGE)
        c.circle(x + 15, y + h - 34, 3.6, fill=1, stroke=0)
        text(c, x + 23, y + h - 36, "СКЛАДСКОЙ УЧЁТ", FONT_B, 4.4, WHITE)

        iy = y + h - 54
        for label, key in MENU:
            if label is None:
                c.setStrokeColor(HexColor("#3B526B"))
                c.setLineWidth(0.5)
                c.line(x + 10, iy + 8, x + sb - 10, iy + 8)
                iy -= 7
                continue
            if key == active:
                c.setFillColor(SIDEBAR_ACTIVE)
                c.rect(x, iy - 3, sb, 15, fill=1, stroke=0)
            c.setFillColor(HexColor("#7FA0C4") if key != active else ORANGE)
            c.rect(x + 10, iy + 3.5, 2.5, 2.5, fill=1, stroke=0)
            text(c, x + 17, iy + 1, label, FONT_B if key == active else FONT, 4.7,
                 WHITE if key == active else HexColor("#C2D0E0"))
            iy -= 17
        text(c, x + 12, y + 14, "Выйти из системы", FONT, 4.4, HexColor("#FF9A9A"))

    # шапка
    c.setFillColor(HEADER)
    c.rect(x + sb, y + h - 40, w - sb, 24, fill=1, stroke=0)
    text(c, x + sb + 10, y + h - 32, "Добро пожаловать, " + user, FONT, 5.6, WHITE)
    sx = x + w - 92
    rounded(c, sx, y + h - 34, 82, 12, r=6, fill=WHITE, stroke=None)
    text(c, sx + 7, y + h - 31.5, "Поиск...", FONT, 4.4, MUTED_2)

    # контент
    cx, cy = x + sb, y + 10
    cw, ch = w - sb, h - 16 - 24 - 10
    c.setFillColor(CONTENT_BG)
    c.rect(cx, cy, cw, ch, fill=1, stroke=0)

    # футер
    c.setFillColor(WHITE)
    c.rect(x + sb, y, w - sb, 10, fill=1, stroke=0)
    c.setStrokeColor(HexColor("#E2E8F0"))
    c.line(x + sb, y + 10, x + w, y + 10)
    c.setFillColor(GREEN)
    c.circle(x + sb + 10, y + 5, 1.6, fill=1, stroke=0)
    text(c, x + sb + 15, y + 3.3, "База данных: подключена", FONT, 4.0, GREEN)
    text(c, x + w - 8, y + 3.3, role, FONT, 4.0, MUTED, "r")

    content(c, cx, cy, cw, ch)


# ---------- содержимое экранов ----------

def ui_dashboard(c, x, y, w, h):
    mock_button(c, x + 12, y + h - 26, 68, 16, "+  Приход", GREEN, WHITE, 5.2)
    mock_button(c, x + 86, y + h - 26, 68, 16, "–  Расход", RED, WHITE, 5.2)

    cards = [("Всего товаров:", "1 247", " шт.", HexColor("#2C3E50")),
             ("Поступило сегодня:", "128", "", GREEN),
             ("Реализовано сегодня:", "46", "", ORANGE)]
    cw = (w - 24 - 16) / 3
    for i, (label, val, unit, col) in enumerate(cards):
        bx = x + 12 + i * (cw + 8)
        rounded(c, bx, y + h - 98, cw, 62, r=4, fill=WHITE, stroke=HexColor("#E6EBF3"))
        text(c, bx + 10, y + h - 52, label, FONT, 5.0, MUTED)
        text(c, bx + 10, y + h - 78, val, FONT_B, 17, col)
        if unit:
            text(c, bx + 10 + sw(val, FONT_B, 17) + 3, y + h - 76, unit, FONT, 5.2, MUTED_2)

    top = y + h - 110
    rounded(c, x + 12, y + 12, w - 24, h - 122, r=4, fill=WHITE, stroke=HexColor("#E6EBF3"))
    text(c, x + 22, top - 16, "Товары на складе (Топ-5 по остаткам)", FONT_B, 6.8, TEXT)
    widths = [42, 210, 80, 52]
    rows = [
        ("1", "Ноутбук Lenovo IdeaPad", "15,00", "шт."),
        ("2", "Мышь беспроводная", "80,00", "шт."),
        ("3", "Бумага А4 (500 листов)", "200,00", "пач"),
        ("4", "Ручка шариковая синяя", "500,00", "шт."),
        ("5", "Чай чёрный (100 пакетиков)", "120,00", "уп"),
    ]
    mock_table(c, x + 22, top - 28, widths, ["Артикул", "Наименование", "Остаток", "Ед."],
               rows, row_h=22, font=5.4, aligns=["c", "l", "r", "c"])
    c.setStrokeColor(HexColor("#EDF1F6"))
    c.setLineWidth(0.5)
    c.line(x + 22, y + 34, x + w - 22, y + 34)
    text(c, x + 22, y + 20, "Всего позиций: 9", FONT, 4.8, MUTED)
    text(c, x + 110, y + 20, "Обновлено: 12.11.2026, 10:42", FONT, 4.8, MUTED_2)
    text(c, x + w - 22, y + 20, "Показать все", FONT_B, 4.8, BLUE, "r")


def ui_products(c, x, y, w, h):
    text(c, x + 12, y + h - 22, "Справочник товаров", FONT_B, 9, TEXT)
    mock_button(c, x + 150, y + h - 26, 74, 16, "+ Добавить товар", BLUE, WHITE, 5.0)

    top = y + h - 38
    rounded(c, x + 12, y + 12, w - 24, h - 50, r=4, fill=WHITE, stroke=HexColor("#E6EBF3"))
    widths = [188, 88, 62, 62, 26]
    rows = [
        ("Ноутбук Lenovo IdeaPad", "Электроника", "15", "52 990", "×"),
        ("Мышь беспроводная", "Электроника", "80", "790", "×"),
        ("Бумага А4 (500 листов)", "Канцелярия", "200", "420", "×"),
        ("Ручка шариковая синяя", "Канцелярия", "500", "18", "×"),
        ("Чай чёрный (100 пакетиков)", "Продукты", "120", "250", "×"),
        ("Кофе растворимый 190 г", "Продукты", "60", "640", "×"),
        ("Моющее средство 5 л", "Хозтовары", "40", "380", "×"),
        ("Дрель аккумуляторная", "Инструменты", "12", "6 490", "×"),
        ("Перчатки рабочие", "Хозтовары", "300", "65", "×"),
    ]
    rc = {(i, 4): RED for i in range(len(rows))}
    mock_table(c, x + 20, top, widths, ["Наименование", "Категория", "Остаток", "Цена", ""],
               rows, row_h=21, font=5.4, aligns=["l", "l", "r", "r", "c"], row_colors=rc)


def ui_operations(c, x, y, w, h):
    text(c, x + 12, y + h - 22, "Приход товара на склад", FONT_B, 9, TEXT)

    # панель выбора
    top = y + h - 34
    rounded(c, x + 12, top - 62, w - 24, 62, r=4, fill=HexColor("#F8F9FA"), stroke=HexColor("#E6EBF3"))
    text(c, x + 20, top - 14, "Контрагент:", FONT, 4.8, MUTED)
    mock_input(c, x + 20, top - 28, 150, 13, "ООО «ТехноСнаб»")
    text(c, x + 182, top - 14, "Товар:", FONT, 4.8, MUTED)
    mock_input(c, x + 182, top - 28, 180, 13, "Ноутбук Lenovo IdeaPad")
    text(c, x + 20, top - 40, "Кол-во:", FONT, 4.8, MUTED)
    mock_input(c, x + 20, top - 54, 44, 13, "15")
    text(c, x + 72, top - 40, "Цена:", FONT, 4.8, MUTED)
    mock_input(c, x + 72, top - 54, 58, 13, "52 990")
    mock_button(c, x + 140, top - 54, 82, 13, "Добавить в список", HexColor("#3498DB"), WHITE, 4.6)

    # таблица
    ttop = top - 72
    rounded(c, x + 12, y + 44, w - 24, ttop - y - 44, r=4, fill=WHITE, stroke=HexColor("#E6EBF3"))
    rows = [
        ("Ноутбук Lenovo IdeaPad", "15", "52 990", "794 850", "×"),
        ("Мышь беспроводная", "80", "790", "63 200", "×"),
        ("Бумага А4 (500 листов)", "200", "420", "84 000", "×"),
        ("Ручка шариковая синяя", "500", "18", "9 000", "×"),
        ("Чай чёрный (100 пакетиков)", "120", "250", "30 000", "×"),
    ]
    widths = [196, 52, 66, 78, 30]
    rc = {(i, 4): RED for i in range(len(rows))}
    mock_table(c, x + 20, ttop, widths, ["Товар", "Кол-во", "Цена", "Сумма", ""],
               rows, row_h=24, font=5.4, aligns=["l", "r", "r", "r", "c"], row_colors=rc)
    text(c, x + 20, y + 28, "Позиций: 5   •   Единиц: 915", FONT, 4.8, MUTED)

    text(c, x + w - 220, y + 26, "ИТОГО:", FONT_B, 7.2, TEXT)
    text(c, x + w - 160, y + 26, "981 050", FONT_B, 8.4, TEXT)
    mock_button(c, x + w - 120, y + 18, 96, 18, "ПРОВЕСТИ ДОКУМЕНТ", GREEN, WHITE, 5.0)


def ui_history(c, x, y, w, h):
    text(c, x + 12, y + h - 22, "История операций", FONT_B, 9, TEXT)
    top = y + h - 34
    rounded(c, x + 12, y + 12, w - 24, h - 46, r=4, fill=WHITE, stroke=HexColor("#E6EBF3"))
    widths = [32, 60, 84, 158, 70, 52]
    rows = [
        ("12", "Приход", "12.11 10:42", "ООО «ТехноСнаб»", "942 050", "Удалить"),
        ("11", "Расход", "11.11 16:40", "ИП Соколов А. В.", "121 300", "Удалить"),
        ("10", "Приход", "10.11 09:15", "ООО «ОфисПлюс»", "58 400", "Удалить"),
        ("9", "Расход", "09.11 16:40", "ИП Соколов А. В.", "34 210", "Удалить"),
        ("8", "Приход", "08.11 11:30", "ООО «ТехноСнаб»", "402 700", "Удалить"),
        ("7", "Расход", "07.11 15:10", "ИП Соколов А. В.", "18 400", "Удалить"),
        ("6", "Приход", "06.11 09:40", "ООО «ОфисПлюс»", "96 300", "Удалить"),
        ("5", "Расход", "05.11 17:25", "ИП Соколов А. В.", "42 100", "Удалить"),
    ]
    rc = {(i, 1): (GREEN if r[1] == "Приход" else RED) for i, r in enumerate(rows)}
    rc.update({(i, 5): RED for i in range(len(rows))})
    mock_table(c, x + 20, top, widths, ["№", "Тип", "Дата", "Контрагент", "Сумма", ""],
               rows, row_h=34, font=5.8, aligns=["c", "c", "l", "l", "r", "c"], row_colors=rc)


def ui_reports(c, x, y, w, h):
    yy = y + h - 22
    text(c, x + 12, yy + 4, "С:", FONT, 4.8, MUTED)
    mock_input(c, x + 24, yy, 60, 12, "01.10.2026")
    text(c, x + 92, yy + 4, "По:", FONT, 4.8, MUTED)
    mock_input(c, x + 108, yy, 60, 12, "12.11.2026")
    mock_button(c, x + 180, yy, 54, 12, "Остатки", BLUE, WHITE, 4.6)
    mock_button(c, x + 238, yy, 72, 12, "Движение товара", WHITE, BLUE, 4.6)
    mock_button(c, x + 314, yy, 80, 12, "Экспорт в CSV", HexColor("#F39C12"), WHITE, 4.6)

    top = y + h - 48
    rounded(c, x + 12, y + 12, w - 24, h - 60, r=4, fill=WHITE, stroke=HexColor("#E6EBF3"))
    rows = [
        ("Ноутбук Lenovo IdeaPad", "Электроника", "15", "794 850"),
        ("Мышь беспроводная", "Электроника", "80", "63 200"),
        ("Бумага А4 (500 листов)", "Канцелярия", "200", "84 000"),
        ("Ручка шариковая синяя", "Канцелярия", "500", "9 000"),
        ("Чай чёрный (100 пакетиков)", "Продукты", "120", "30 000"),
        ("Кофе растворимый 190 г", "Продукты", "60", "38 400"),
        ("Моющее средство 5 л", "Хозтовары", "40", "15 200"),
        ("Дрель аккумуляторная", "Инструменты", "12", "77 880"),
        ("Перчатки рабочие", "Хозтовары", "300", "19 500"),
    ]
    widths = [198, 106, 68, 84]
    mock_table(c, x + 20, top, widths, ["Товар", "Категория", "Кол-во", "Сумма"],
               rows, row_h=25, font=5.4, aligns=["l", "l", "r", "r"])


def ui_users(c, x, y, w, h):
    text(c, x + 12, y + h - 20, "Пользователи", FONT_B, 8.6, TEXT)
    # форма
    rounded(c, x + 12, y + 12, 178, h - 40, r=4, fill=WHITE, stroke=HexColor("#E6EBF3"))
    text(c, x + 22, y + h - 44, "НОВЫЙ ПОЛЬЗОВАТЕЛЬ", FONT_B, 5.4, MUTED)
    labels = ["Логин:", "Пароль:", "Повтор пароля:", "ФИО:", "Роль:"]
    vals = ["petrov", "••••••••", "••••••••", "Петров Пётр", "Менеджер"]
    for i, (l, v) in enumerate(zip(labels, vals)):
        yy = y + h - 62 - i * 34
        text(c, x + 22, yy, l, FONT, 4.8, MUTED)
        mock_input(c, x + 22, yy - 14, 158, 12, v)
    text(c, x + 22, y + 44, "Пароль хешируется перед сохранением", FONT, 4.2, MUTED_2)
    mock_button(c, x + 22, y + 22, 100, 14, "Создать пользователя", BLUE, WHITE, 4.6)

    # таблица
    tx = x + 202
    tw = w - 214
    rounded(c, tx, y + 12, tw, h - 40, r=4, fill=WHITE, stroke=HexColor("#E6EBF3"))
    rows = [
        ("admin", "Администратор системы", "Администратор", "—"),
        ("manager", "Петрова Анна Сергеевна", "Менеджер", "×"),
        ("sklad", "Иванов Иван Иванович", "Сотрудник склада", "×"),
        ("petrov", "Петров Пётр Петрович", "Менеджер", "×"),
        ("sidorov", "Сидоров Сергей Сергеевич", "Сотрудник склада", "×"),
        ("kozlova", "Козлова Мария Ильинична", "Менеджер", "×"),
        ("orlov", "Орлов Олег Олегович", "Сотрудник склада", "×"),
    ]
    widths = [46, 130, 78, 14]
    rc = {(i, 3): RED for i in range(1, len(rows))}
    mock_table(c, tx + 3, y + h - 48, widths, ["Логин", "ФИО", "Роль", ""],
               rows, row_h=28, font=5.2, aligns=["l", "l", "l", "c"], row_colors=rc)


def ui_support(c, x, y, w, h):
    # форма
    fx = x + 12
    fw = 190
    rounded(c, fx, y + 12, fw, h - 26, r=4, fill=HexColor("#F8F9FA"), stroke=HexColor("#E6EBF3"))
    text(c, fx + 10, y + h - 28, "НОВОЕ ОБРАЩЕНИЕ", FONT_B, 5.4, TEXT)
    text(c, fx + 10, y + h - 42, "Тема:", FONT, 4.6, MUTED)
    mock_input(c, fx + 10, y + h - 54, fw - 20, 12, "Другое")
    text(c, fx + 10, y + h - 68, "Опишите проблему:", FONT, 4.6, MUTED)
    rounded(c, fx + 10, y + h - 112, fw - 20, 40, r=2, fill=WHITE, stroke=HexColor("#C9D4E2"))
    para(c, fx + 14, y + h - 76, fw - 28,
         "Не получается найти раздел «Отчёты» в меню.", 4.6, 6.2, TEXT)
    text(c, fx + 10, y + h - 122, "Телефон или e-mail:", FONT, 4.6, MUTED)
    mock_input(c, fx + 10, y + h - 134, fw - 20, 12, "+7 (900) 000-00-00")
    mock_button(c, fx + 10, y + h - 156, fw - 20, 14, "Отправить", GREEN, WHITE, 4.8)
    text(c, fx + 10, y + h - 170, "Обращение №17 отправлено.", FONT, 4.4, BLUE)
    text(c, fx + 10, y + h - 180, "Статус: «Новое».", FONT, 4.4, BLUE)

    text(c, fx + 10, y + 126, "ЧТО УКАЗАТЬ", FONT_B, 4.8, TEXT)
    text(c, fx + 10, y + 114, "•  что делали перед ошибкой", FONT, 4.2, MUTED)
    text(c, fx + 10, y + 104, "•  текст ошибки или снимок", FONT, 4.2, MUTED)
    text(c, fx + 10, y + 94, "•  раздел, где это произошло", FONT, 4.2, MUTED)

    text(c, fx + 10, y + 60, "КОНТАКТЫ", FONT_B, 4.8, TEXT)
    text(c, fx + 10, y + 48, "+7 (000) 000-00-00", FONT, 4.4, MUTED)
    text(c, fx + 10, y + 38, "support@example.com", FONT, 4.4, MUTED)
    text(c, fx + 10, y + 28, "Пн–Пт, 9:00–18:00", FONT, 4.4, MUTED)

    # таблица обращений
    tx = fx + fw + 12
    tw = w - (tx - x) - 12
    text(c, tx, y + h - 20, "ВСЕ ОБРАЩЕНИЯ", FONT_B, 5.0, TEXT)
    rows = [
        ("17", "12.11 10:12", "Иванов И. И.", "Другое", "Новое"),
        ("16", "11.11 16:40", "Петрова А. С.", "Отчёты", "В работе"),
        ("15", "10.11 09:05", "Иванов И. И.", "Вход", "Закрыто"),
        ("14", "09.11 14:20", "Сидоров С. С.", "Документы", "Закрыто"),
        ("13", "08.11 11:10", "Петрова А. С.", "Отчёты", "Закрыто"),
        ("12", "07.11 16:35", "Иванов И. И.", "Другое", "Закрыто"),
    ]
    widths = [24, 54, 66, 48, 44]
    rc = {(0, 4): BLUE, (1, 4): ORANGE, (2, 4): GREEN}
    top = y + h - 28
    rounded(c, tx, y + 12, tw, h - 40, r=4, fill=WHITE, stroke=HexColor("#E6EBF3"))
    mock_table(c, tx + 6, top, widths, ["№", "Дата", "Автор", "Тема", "Статус"],
               rows, row_h=28, font=4.8, aligns=["c", "l", "l", "l", "c"], row_colors=rc)
