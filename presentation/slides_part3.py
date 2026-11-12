# -*- coding: utf-8 -*-
"""Слайды 15–24: раздел «как работает», экраны приложения, бот, поддержка, админ."""
import os
from reportlab.lib.colors import HexColor
from theme import *
from mockups import (app_window, ui_dashboard, ui_products, ui_operations,
                     ui_history, ui_reports, ui_users, ui_support,
                     mock_button, mock_input, mock_table, cut)


# ---------------- 15. разделитель ----------------

def s15_divider(c, num):
    page_bg(c, dark=True)
    # едва заметный каркас окна справа
    c.setFillColor(HexColor("#17283D"))
    c.roundRect(600, 120, 330, 300, 8, fill=1, stroke=0)
    c.setFillColor(HexColor("#1D3A58"))
    c.rect(600, 370, 330, 20, fill=1, stroke=0)
    c.setFillColor(HexColor("#15243A"))
    c.rect(600, 120, 78, 250, fill=1, stroke=0)
    c.setStrokeColor(HexColor("#263E59"))
    for i in range(6):
        c.line(690, 350 - i * 32, 910, 350 - i * 32)

    text(c, M, 430, "ЧАСТЬ 2", FONT_B, 9, ORANGE)
    text(c, M, 360, "02", FONT_B, 74, ORANGE)
    text(c, M + 110, 372, "Как работает", FONT_B, 34, WHITE)
    text(c, M + 110, 332, "приложение", FONT_B, 34, WHITE)
    para(c, M, 300, 500,
         "Один сквозной сценарий: вход, главная, документ, остаток, отчёт и помощь. "
         "Показываем экраны и логику, которая за ними стоит.", 11.5, 16, HexColor("#C6D3E2"))

    path = ["Вход", "Главная", "Документ", "Остаток", "Отчёт", "Помощник"]
    x = M
    y = 128
    for i, label in enumerate(path):
        w = sw(label, FONT_B, 8.2) + 20
        rounded(c, x, y, w, 22, r=11, fill=HexColor("#1A2C42"), stroke=HexColor("#35506F"))
        text(c, x + w / 2, y + 8, label, FONT_B, 8.2, WHITE, "c")
        x += w
        if i < len(path) - 1:
            arrow(c, x + 5, y + 11, x + 19, y + 11, ORANGE, 0.8, 4)
            x += 24


# ---------------- 16. главная ----------------

def s16_dashboard(c, num):
    page_bg(c)
    top = header(c, "03 / Реализация", "Главная: состояние склада за пять секунд",
                 "Сводка за сегодня, быстрые действия и топ-5 остатков. Не нужно открывать отчёт, чтобы понять картину.")
    app_window(c, 40, 76, 600, 372, "dashboard", ui_dashboard)

    x, w = 666, 246
    text(c, x, top - 6, "ЧТО НА ЭКРАНЕ", FONT_B, 7.6, ORANGE)
    bullets(c, x, top - 24, w, [
        "Три карточки: всего на складе, поступило и реализовано сегодня.",
        "Быстрые кнопки «Приход» и «Расход» — из сводки в документ.",
        "Топ-5 товаров по остатку: что занимает склад.",
        "Глобальный поиск в шапке — по товарам и разделам.",
    ], size=8.8, leading=12, gap=7)
    rounded(c, x, 76, w, 64, r=6, fill=BLUE_PALE, stroke=None)
    text(c, x + 12, 124, "ПОД КАПОТОМ", FONT_B, 6.4, BLUE)
    para(c, x + 12, 114, w - 24,
         "Четыре SQL-запроса при открытии: сумма остатков, приход и расход за сегодня, топ-5.",
         8.0, 10.8, TEXT)
    text(c, 48, 62, "Экран воспроизведён по XAML-разметке приложения", FONT, 6.4, MUTED_2)


# ---------------- 17. товары ----------------

def s17_products(c, num):
    page_bg(c)
    top = header(c, "03 / Реализация", "Товары: справочник и категории",
                 "Поиск по названию, остаток из документов, удаление — только администратор и только если товар не используется.")
    app_window(c, 40, 76, 600, 372, "products", ui_products)

    x, w = 666, 246
    text(c, x, top - 6, "КАК УСТРОЕНО", FONT_B, 7.6, ORANGE)
    bullets(c, x, top - 24, w, [
        "Поиск по названию: фильтр в SQL, без загрузки всего каталога.",
        "Категории — отдельный справочник; добавляет администратор.",
        "Новый товар всегда с остатком 0: на учёт ставит приход.",
        "Удаление проверяет связи: товар в документах удалить нельзя.",
    ], size=8.8, leading=12, gap=7)

    rounded(c, x, 76, w, 92, r=6, fill=RED_PALE, stroke=None)
    text(c, x + 12, 152, "ПЕРЕХВАТ SQL 547", FONT_B, 6.4, RED)
    para(c, x + 12, 142, w - 24,
         "Вместо технической ошибки базы пользователь видит: «Товар используется в документах. "
         "Сначала удалите документы».", 8.0, 10.8, TEXT)
    text(c, 48, 62, "Экран воспроизведён по XAML-разметке приложения", FONT, 6.4, MUTED_2)


# ---------------- 18. операции ----------------

def s18_operations(c, num):
    page_bg(c)
    top = header(c, "03 / Реализация", "Приход и расход: документ меняет остаток",
                 "Одна форма на две операции. Разница — направление остатка и проверка доступного количества.")
    app_window(c, 40, 76, 600, 372, "income", ui_operations)

    x, w = 666, 246
    text(c, x, top - 4, "ПРИ СОХРАНЕНИИ", FONT_B, 7.6, ORANGE)
    steps = [
        ("Проверка", "для расхода: хватает ли остатка"),
        ("Транзакция", "BEGIN TRANSACTION"),
        ("Документ", "INSERT в Documents и DocumentItems"),
        ("Остаток", "UPDATE Products: плюс или минус"),
        ("Фиксация", "COMMIT или полный ROLLBACK"),
    ]
    yy = top - 22
    for i, (t, d) in enumerate(steps, 1):
        numbered(c, x, yy + 2, i, d=15, color=BLUE, size=7)
        text(c, x + 22, yy, t, FONT_B, 8.8, TEXT)
        text(c, x + 22, yy - 11, d, FONT, 7.4, MUTED)
        yy -= 30

    rounded(c, x, 76, w, 62, r=6, fill=GREEN_PALE, stroke=None)
    text(c, x + 12, 122, "ЛИБО ОБА, ЛИБО НИЧЕГО", FONT_B, 6.4, GREEN)
    para(c, x + 12, 112, w - 24,
         "Ошибка на любом шаге откатывает и документ, и остаток. Минус на складе невозможен: CHECK Quantity ≥ 0.",
         8.0, 10.8, TEXT)
    text(c, 48, 62, "Экран воспроизведён по XAML-разметке приложения", FONT, 6.4, MUTED_2)


# ---------------- 19. инвентаризация и история ----------------

def s19_history(c, num):
    page_bg(c)
    top = header(c, "03 / Реализация", "Инвентаризация и история операций",
                 "Факт можно привести к учёту напрямую, а документ — удалить с обратным пересчётом остатков.")
    app_window(c, 40, 76, 600, 372, "history", ui_history)

    x, w = 666, 246
    rounded(c, x, top - 118, w, 112, r=6, fill=WHITE, stroke=BORDER)
    text(c, x + 12, top - 22, "ИНВЕНТАРИЗАЦИЯ", FONT_B, 7.0, BLUE)
    # мини-таблица
    c.setFillColor(HexColor("#F1F5FA"))
    c.rect(x + 12, top - 42, w - 24, 12, fill=1, stroke=0)
    text(c, x + 18, top - 38, "Товар", FONT_B, 4.4, MUTED)
    text(c, x + 140, top - 38, "Учёт", FONT_B, 4.4, MUTED)
    text(c, x + 182, top - 38, "Факт", FONT_B, 4.4, MUTED)
    rows = [("Ноутбук", "15", "14"), ("Мышь", "80", "78"), ("Бумага А4", "200", "200")]
    yy = top - 54
    for a, b, d in rows:
        text(c, x + 18, yy, a, FONT, 4.8, TEXT)
        text(c, x + 140, yy, b, FONT, 4.8, MUTED)
        text(c, x + 182, yy, d, FONT_B, 4.8, ORANGE)
        yy -= 13
    mock_button(c, x + 12, top - 108, 92, 13, "Сохранить изменения", GREEN, WHITE, 4.2)

    bullets(c, x, top - 136, w, [
        "Инвентаризация меняет остаток напрямую, без документа.",
        "Удаление документа пересчитывает остаток: приход — минус, расход — плюс.",
        "Всё в транзакции: история и остаток остаются согласованными.",
    ], size=8.4, leading=11.4, gap=6)
    rounded(c, x, 76, w, 58, r=6, fill=ORANGE_PALE, stroke=None)
    text(c, x + 12, 120, "ВАЖНО", FONT_B, 6.4, ORANGE)
    para(c, x + 12, 110, w - 24,
         "Инвентаризация не создаёт документ — если нужен след в истории, оформляйте приход или расход.",
         7.8, 10.6, TEXT)
    text(c, 48, 62, "Экран воспроизведён по XAML-разметке приложения", FONT, 6.4, MUTED_2)


# ---------------- 20. отчёты ----------------

def s20_reports(c, num):
    page_bg(c)
    top = header(c, "03 / Реализация", "Отчёты: остатки, движение и CSV",
                 "Два отчёта и выгрузка, которую бухгалтерия откроет в Excel. Доступ — у менеджера и администратора.")
    app_window(c, 40, 76, 600, 372, "reports", ui_reports)

    x, w = 666, 246
    text(c, x, top - 6, "ДВА ОТЧЁТА", FONT_B, 7.6, ORANGE)
    yy = top - 26
    for t, d in [("Остатки", "товар, категория, количество, цена и сумма — на текущую дату."),
                 ("Движение", "приход и расход за выбранный период с датами.")]:
        check(c, x, yy - 6, 7, GREEN)
        text(c, x + 16, yy, t, FONT_B, 9.2, TEXT)
        hh = para(c, x + 16, yy - 5, w - 16, d, 8.0, 10.8, MUTED)
        yy -= hh + 24
    text(c, x, 296, "CSV ДЛЯ EXCEL", FONT_B, 6.6, MUTED)
    rounded(c, x, 198, w, 84, r=5, fill=HexColor("#1A2A3F"), stroke=None)
    lines = ["Товар;Кол-во;Сумма;Тип", "Ноутбук;15;794850;Приход", "Мышь;80;63200;Приход",
             "Бумага А4;200;84000;Приход"]
    yy = 266
    for i, ln in enumerate(lines):
        text(c, x + 12, yy, ln, FONT, 6.0, HexColor("#D7E4F3") if i == 0 else HexColor("#9FD3AE"))
        yy -= 15
    text(c, x, 180, "UTF-8  •  разделитель «;»", FONT, 6.4, MUTED_2)
    rounded(c, x, 76, w, 64, r=6, fill=BLUE_PALE, stroke=None)
    text(c, x + 12, 126, "ДОСТУП", FONT_B, 6.4, BLUE)
    para(c, x + 12, 116, w - 24,
         "Пункт меню скрыт для кладовщика; бот тоже объяснит, что отчёт доступен менеджеру.",
         8.0, 10.8, TEXT)
    text(c, 48, 62, "Экран воспроизведён по XAML-разметке приложения", FONT, 6.4, MUTED_2)


# ---------------- 21. как устроен бот ----------------

def s21_bot(c, num):
    page_bg(c)
    top = header(c, "03 / Реализация", "Помощник: дерево решений, а не нейросеть",
                 "Правила, ключевые слова и роль пользователя. Работает локально, без интернета и без обращения к базе.")

    steps = [
        ("01", "Нормализация", "нижний регистр, ё = е, знаки препинания убираются"),
        ("02", "Кнопка или текст", "ответ на текущий вопрос: да, нет или название ветки"),
        ("03", "Ключевые слова", "вес совпадения; опечатки — расстояние Левенштейна ≤ 1"),
        ("04", "Ветка дерева", "вопрос, действие и кнопка «Открыть раздел»"),
    ]
    w, h, gap = 204, 82, 16
    for i, (n, t, d) in enumerate(steps):
        x = M + i * (w + gap)
        y = 330
        card(c, x, y, w, h, fill=WHITE, stroke=BORDER)
        text(c, x + 12, y + h - 16, n, FONT_B, 7.4, ORANGE)
        text(c, x + 12, y + h - 32, t, FONT_B, 9.6, TEXT)
        para(c, x + 12, y + h - 42, w - 24, d, 7.4, 9.8, MUTED)
        if i < 3:
            arrow(c, x + w + 3, y + h / 2, x + w + gap - 4, y + h / 2, BLUE, 1.0, 4)

    # мини-дерево
    tx, ty = 48, 78
    rounded(c, tx, ty, 474, 200, r=6, fill=WHITE, stroke=BORDER)
    text(c, tx + 14, ty + 184, "ДЕРЕВО ДИАЛОГА", FONT_B, 6.8, MUTED)
    root = (tx + 160, ty + 154, 154, 22)
    rounded(c, root[0], root[1], root[2], root[3], r=4, fill=NAVY, stroke=None)
    text(c, root[0] + root[2] / 2, root[1] + 7.5, "Что нужно сделать?", FONT_B, 6.6, WHITE, "c")
    children = ["Приход", "Расход", "Товары", "История", "Вход", "Помощник"]
    centers = []
    for i, ch in enumerate(children):
        cx = tx + 10 + i * 76
        centers.append(cx + 36)
        border = ORANGE if ch == "Товары" else HexColor("#D5DEEA")
        fill = ORANGE_PALE if ch == "Товары" else WHITE
        rounded(c, cx, ty + 96, 72, 20, r=10, fill=fill, stroke=border, lw=1.0 if ch == "Товары" else 0.7)
        text(c, cx + 36, ty + 102.5, ch, FONT_B if ch == "Товары" else FONT, 5.8, TEXT, "c")
    # шина
    c.setStrokeColor(HexColor("#C7D3E2"))
    c.setLineWidth(0.6)
    bus_y = ty + 130
    c.line(root[0] + root[2] / 2, root[1], root[0] + root[2] / 2, bus_y)
    c.line(centers[0], bus_y, centers[-1], bus_y)
    for cx in centers:
        c.line(cx, bus_y, cx, ty + 116)
    # пример
    text(c, tx + 14, ty + 74, "«не сходится остаток»", FONT_I, 6.4, ORANGE)
    text(c, tx + 14, ty + 58, "Товары  •  Инвентаризация  •  кнопка «Открыть раздел»", FONT_B, 6.4, ORANGE)
    line(c, tx + 14, ty + 42, tx + 456, ty + 42, HexColor("#E6EBF2"), 0.6)
    text(c, tx + 14, ty + 28, "«забыл пароль»  •  Вход и доступ  •  совет и сброс через администратора",
         FONT, 6.4, MUTED)

    # метрики
    mx, my = 546, 248
    stats = [("126", "узлов дерева"), ("41", "вопрос"), ("85", "действий"), ("11", "тем")]
    for i, (n, lab) in enumerate(stats):
        bx = mx + (i % 2) * 184
        by = my - (i // 2) * 66
        rounded(c, bx, by, 172, 56, r=5, fill=WHITE, stroke=BORDER)
        text(c, bx + 12, by + 30, n, FONT_B, 20, BLUE)
        text(c, bx + 62, by + 29, lab, FONT, 7.6, MUTED)
    text(c, mx, 152, "8 готовых ответов  •  4 сценария small talk", FONT, 7.6, MUTED)
    text(c, mx, 136, "10 кнопок навигации в разделы", FONT, 7.6, MUTED)
    rounded(c, mx, 78, 366, 38, r=5, fill=GREEN_PALE, stroke=None)
    text(c, mx + 12, 102, "БЕЗ НЕЙРОСЕТИ", FONT_B, 6.4, GREEN)
    text(c, mx + 12, 88, "Ответы предсказуемы и проверяются тестами", FONT, 7.6, TEXT)


# ---------------- 22. диалог с ботом ----------------

def bubble(c, x, top, maxw, text_, user=False, size=6.2):
    lines = wrap_lines(text_, maxw - 14, FONT, size)
    w = max(sw(ln, FONT, size) for ln in lines) + 14
    h = len(lines) * (size * 1.35) + 8
    bx = x + maxw - w if user else x
    rounded(c, bx, top - h, w, h, r=6, fill=BLUE if user else WHITE,
            stroke=None if user else HexColor("#DDE3EA"), lw=0.7)
    yy = top - 5 - size
    for ln in lines:
        text(c, bx + 7, yy, ln, FONT, size, WHITE if user else TEXT)
        yy -= size * 1.35
    return h


def chips(c, x, top, labels, maxw, size=5.8):
    cx, cy = x, top
    for lab in labels:
        w = sw(lab, FONT, size) + 12
        if cx + w > x + maxw:
            cx = x
            cy -= 17
        rounded(c, cx, cy - 13, w, 13, r=6.5, fill=WHITE, stroke=BLUE_L, lw=0.6)
        text(c, cx + 6, cy - 9, lab, FONT, size, BLUE)
        cx += w + 5
    return cy - 20


def s22_dialog(c, num):
    page_bg(c)
    top = header(c, "03 / Реализация", "Помощник в диалоге: от вопроса к разделу",
                 "Свободный текст, кнопки и переход в нужный раздел. Последний вопрос можно сразу передать в поддержку.")

    # окно чата
    x, y, w, h = 40, 50, 650, 370
    rounded(c, x + 3, y - 3, w, h, 7, fill=HexColor("#DCE3ED"), stroke=None)
    rounded(c, x, y, w, h, r=7, fill=WHITE, stroke=HexColor("#C9D4E2"))
    c.setFillColor(HexColor("#1A2A3F"))
    c.roundRect(x, y + h - 16, w, 16, 6, fill=1, stroke=0)
    c.rect(x, y + h - 16, w, 6, fill=1, stroke=0)
    text(c, x + 12, y + h - 10.5, "Складской помощник", FONT_B, 5.0, HexColor("#AFC0D6"))

    # шапка чата
    c.setFillColor(HexColor("#F4F7F9"))
    c.rect(x, y + h - 52, w, 36, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.circle(x + 26, y + h - 34, 9, fill=1, stroke=0)
    text(c, x + 26, y + h - 37, "Б", FONT_B, 8.0, WHITE, "c")
    text(c, x + 42, y + h - 29, "Складской помощник", FONT_B, 9.0, TEXT)
    text(c, x + 42, y + h - 41, "Пишите своими словами или выбирайте ответы кнопками", FONT, 6.2, MUTED)
    mock_button(c, x + w - 118, y + h - 45, 106, 16, "Написать в техподдержку", ORANGE, WHITE, 5.0)

    # сообщения
    ax, aw = x + 14, w - 28
    at = y + h - 62
    at -= bubble(c, ax, at, aw, "Здравствуйте, Иванов Иван Иванович! Я Складской помощник. Напишите, что нужно сделать, или выберите тему кнопкой.", size=7.0) + 5
    at = chips(c, ax, at, ["Приход", "Расход", "Товары и остатки", "История и отчёты", "Вход и доступ", "Техподдержка"], aw, size=6.4)
    at -= bubble(c, ax, at, aw, "не сходится остаток", user=True, size=7.0) + 6
    at -= bubble(c, ax, at, aw, "Остатки меняются через инвентаризацию.", size=7.0) + 4
    at -= bubble(c, ax, at, aw, "Открыть «Инвентаризацию»", size=7.0) + 4
    at -= bubble(c, ax, at, aw, "Ввести фактический остаток", size=7.0) + 4
    at -= bubble(c, ax, at, aw, "Нажать «Сохранить изменения»", size=7.0) + 4
    at -= bubble(c, ax, at, aw, "Сохранение прошло успешно?", size=7.0) + 4
    at = chips(c, ax, at, ["Да", "Нет"], aw, size=6.4)
    mock_button(c, ax, at - 15, 132, 14, "Открыть «Инвентаризацию»", GREEN, WHITE, 5.2)
    text(c, ax, at - 34, "Если не помогло — передайте последний вопрос в поддержку.", FONT_I, 6.2, MUTED)
    mock_button(c, ax, at - 50, 124, 13, "Написать в техподдержку", ORANGE, WHITE, 4.8)

    # ввод
    c.setStrokeColor(HexColor("#E2E8F0"))
    c.line(x + 12, y + 30, x + w - 12, y + 30)
    mock_input(c, x + 14, y + 12, 420, 16, placeholder="Сообщение...")
    mock_button(c, x + 440, y + 12, 62, 16, "Отправить", BLUE, WHITE, 5.0)
    mock_button(c, x + 508, y + 12, 50, 16, "Назад", WHITE, TEXT, 4.8)
    mock_button(c, x + 564, y + 12, 72, 16, "Начать заново", WHITE, TEXT, 4.6)

    # панель
    px, pw = 712, 200
    text(c, px, top - 8, "ЧТО ДЕЛАЕТ БОТ", FONT_B, 7.2, ORANGE)
    bullets(c, px, top - 26, pw, [
        "Понимает текст и кнопки.",
        "Помнит ветку: «Назад» и «Начать заново».",
        "Сам отвечает на вопросы о правах по роли.",
        "Предлагает открыть раздел программы.",
        "Передаёт последний вопрос в поддержку.",
    ], size=8.2, leading=11.2, gap=5)
    rounded(c, px, 210, pw, 76, r=6, fill=BLUE_PALE, stroke=None)
    text(c, px + 10, 270, "ЧЕГО НЕ ДЕЛАЕТ", FONT_B, 6.2, BLUE)
    para(c, px + 10, 260, pw - 20,
         "Не обращается к базе, не выдумывает ответы. Не понял — fallback и список тем.",
         7.8, 10.4, TEXT)


# ---------------- 23. техподдержка ----------------

def s23_support(c, num):
    page_bg(c)
    top = header(c, "03 / Реализация", "Техподдержка: обращение не теряется",
                 "Форма, номер, статус и история. Пользователь видит свои обращения, администратор — все.")
    app_window(c, 40, 76, 600, 372, "support", ui_support)

    x, w = 666, 246
    text(c, x, top - 6, "МАРШРУТ ОБРАЩЕНИЯ", FONT_B, 7.6, ORANGE)
    statuses = [("Новое", BLUE), ("В работе", ORANGE), ("Закрыто", GREEN)]
    yy = top - 30
    for i, (s, col) in enumerate(statuses):
        bx = x + i * 82
        rounded(c, bx, yy - 12, 70, 18, r=9, fill=col, stroke=None)
        text(c, bx + 35, yy - 6, s, FONT_B, 6.6, WHITE, "c")
        if i < 2:
            arrow(c, bx + 73, yy - 3, bx + 80, yy - 3, MUTED_2, 0.8, 3)

    bullets(c, x, top - 72, w, [
        "Бот передаёт последний вопрос в описание — не нужно перепечатывать.",
        "Номер обращения и статус показываются сразу после отправки.",
        "Администратор двигает статус: «Новое», «В работе», «Закрыто».",
        "Контакты поддержки всегда на экране.",
    ], size=8.4, leading=11.4, gap=6)
    rounded(c, x, 76, w, 62, r=6, fill=ORANGE_PALE, stroke=None)
    text(c, x + 12, 122, "ЕСЛИ РАБОТА ВСТАЛА", FONT_B, 6.4, ORANGE)
    para(c, x + 12, 112, w - 24,
         "В обращении есть контакты: телефон, e-mail и часы работы. Это последний шаг схемы.",
         7.8, 10.6, TEXT)
    text(c, 48, 62, "Экран воспроизведён по XAML-разметке приложения", FONT, 6.4, MUTED_2)


# ---------------- 24. администрирование ----------------

def s24_admin(c, num):
    page_bg(c)
    top = header(c, "03 / Реализация", "Администрирование и безопасность",
                 "Пользователи, роли и реквизиты склада. Пароли не хранятся в открытом виде.")
    app_window(c, 40, 76, 600, 372, "users", ui_users)

    x, w = 666, 246
    text(c, x, top - 6, "ЧТО ЗАКРЫТО", FONT_B, 7.6, ORANGE)
    items = [
        ("Пароли", "SHA-256, 64 hex-символа; открытый пароль не сохраняется"),
        ("Роли", "меню, команды и ответы бота зависят от роли"),
        ("admin", "учётную запись нельзя удалить из интерфейса"),
        ("Настройки", "пользователи, категории и реквизиты — только администратор"),
    ]
    yy = top - 26
    for t, d in items:
        check(c, x, yy - 6, 8, GREEN)
        text(c, x + 18, yy, t, FONT_B, 8.8, TEXT)
        para(c, x + 18, yy - 6, w - 18, d, 7.6, 10.2, MUTED)
        yy -= 38

    rounded(c, x, 96, w, 96, r=6, fill=ORANGE_PALE, stroke=None)
    text(c, x + 12, 178, "ЗОНЫ РОСТА", FONT_B, 6.4, ORANGE)
    bullets(c, x + 12, 168, w - 24, [
        "Соль + PBKDF2/Argon2 вместо чистого SHA-256.",
        "Восстановление пароля и журнал аудита действий.",
        "Параметризовать оставшиеся SQL-запросы.",
    ], size=7.4, leading=9.6, gap=3, bullet_color=ORANGE)
    text(c, 48, 62, "Экран воспроизведён по XAML-разметке приложения", FONT, 6.4, MUTED_2)
