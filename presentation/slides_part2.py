# -*- coding: utf-8 -*-
"""Слайды 6–14: роли, функции, архитектура, три схемы, сценарии."""
import os
from reportlab.lib.colors import HexColor, Color
from theme import *

ASSETS = os.path.join(HERE, "assets")


# ---------------- 6. роли ----------------

def s06_roles(c, num):
    page_bg(c)
    top = header(c, "01 / Анализ и постановка", "Три роли — три набора прав",
                 "Одна база, но разный интерфейс: роль определяется при входе и влияет на меню, команды и ответы помощника.")

    roles = [
        ("А", "Администратор", "Полный доступ", NAVY,
         ["Пользователи и роли", "Настройки и категории", "Товары: добавление и удаление",
          "Приход, расход, инвентаризация", "Отчёты и история", "Все обращения поддержки"], []),
        ("М", "Менеджер", "Учёт + аналитика", BLUE,
         ["Товары и документы", "Приход, расход, инвентаризация", "История операций",
          "Отчёты по остаткам и движению", "Экспорт в CSV"], ["Пользователи", "Настройки"]),
        ("С", "Сотрудник склада", "Складские операции", GREEN,
         ["Товары: просмотр", "Приход и расход", "Инвентаризация",
          "История операций", "Помощник и поддержка"], ["Отчёты", "Пользователи и настройки"]),
    ]
    w, h = 278, 300
    for i, (letter, name, badge, color, allowed, denied) in enumerate(roles):
        x = M + i * (w + 15)
        y = 120
        card(c, x, y, w, h, accent=color)
        c.setFillColor(color)
        c.circle(x + 34, y + h - 38, 17, fill=1, stroke=0)
        text(c, x + 34, y + h - 44, letter, FONT_B, 14, WHITE, "c")
        text(c, x + 60, y + h - 34, name, FONT_B, 13.2, TEXT)
        text(c, x + 60, y + h - 50, badge, FONT, 8.6, color)
        yy = y + h - 78
        for a in allowed:
            check(c, x + 18, yy - 3, 8, GREEN, 1.5)
            text(c, x + 34, yy - 9, a, FONT, 9.0, TEXT)
            yy -= 25
        for d in denied:
            cross(c, x + 18, yy - 4, 6, RED, 1.3)
            text(c, x + 34, yy - 9, d, FONT, 9.0, MUTED_2)
            yy -= 25

    rounded(c, M, 58, W - M * 2, 46, r=6, fill=NAVY, stroke=None)
    text(c, M + 18, 82, "Принцип:", FONT_B, 9.4, ORANGE)
    text(c, M + 76, 82, "права проверяются не только в меню, но и в командах, и в ответах чат-бота.",
         FONT, 10, WHITE)


# ---------------- 7. функциональная карта ----------------

def s07_map(c, num):
    page_bg(c)
    top = header(c, "01 / Анализ и постановка", "Функциональная карта приложения",
                 "Четыре блока закрывают весь путь: от справочника товара до обращения в поддержку.")

    cols = [
        ("01", "УЧЁТ", BLUE, "6 разделов",
         [("Главная", "сводка и топ-5 остатков"), ("Товары", "справочник и поиск"),
          ("Приход", "поступление на склад"), ("Расход", "отгрузка с проверкой"),
          ("Инвентаризация", "факт вместо учёта"), ("История", "документы и удаление")],
         "Остаток совпадает с фактом"),
        ("02", "АНАЛИТИКА", ORANGE, "2 отчёта + CSV",
         [("Остатки на дату", "товар, склад, сумма"), ("Движение", "приход/расход за период"),
          ("Экспорт CSV", "открывается в Excel"), ("Фильтр по датам", "начало и конец")],
         "Цифры для решения"),
        ("03", "ПОМОЩЬ", GREEN, "бот + тикеты",
         [("Складской помощник", "126 узлов, 11 тем"), ("8 готовых ответов", "частые вопросы"),
          ("Техподдержка", "форма и контакты"), ("Статусы", "Новое / В работе / Закрыто")],
         "Вопрос не уходит в пустоту"),
        ("04", "АДМИНИСТРИРОВАНИЕ", NAVY, "3 роли",
         [("Пользователи", "создание и удаление"), ("Роли", "три набора прав"),
          ("Категории", "справочник товаров"), ("Реквизиты", "название и адрес склада")],
         "Доступ по роли"),
    ]
    w, h = 204, 312
    for i, (n, title, color, count, items, result) in enumerate(cols):
        x = M + i * (w + 12)
        y = 110
        card(c, x, y, w, h, fill=WHITE, stroke=BORDER)
        rounded(c, x, y + h - 58, w, 58, r=8, fill=color, stroke=None)
        c.rect(x, y + h - 58, w, 8, fill=1, stroke=0)
        text(c, x + 14, y + h - 26, n, FONT_B, 8, WHITE)
        text(c, x + 14, y + h - 44, title, FONT_B, 9.6, WHITE)
        text(c, x + w - 14, y + h - 26, count, FONT, 7.2, WHITE, "r")
        yy = y + h - 82
        for t, d in items:
            c.setFillColor(color)
            c.rect(x + 14, yy + 3, 4, 4, fill=1, stroke=0)
            text(c, x + 24, yy, t, FONT, 8.6, TEXT)
            text(c, x + 24, yy - 12, d, FONT, 7.1, MUTED)
            yy -= 28
        rounded(c, x + 12, y + 14, w - 24, 46, r=5, fill=HexColor("#F6F8FB"), stroke=None)
        text(c, x + 22, y + 42, "РЕЗУЛЬТАТ", FONT_B, 6.2, color)
        para(c, x + 22, y + 34, w - 44, result, 7.8, 10, TEXT)

    text(c, M, 76, "11 разделов + окно входа   •   3 роли   •   9 таблиц   •   единая база данных",
         FONT_B, 9.4, MUTED)


# ---------------- 8. архитектура ----------------

def layer(c, x, y, w, h, title, sub, color, items=None):
    rounded(c, x, y, w, h, r=6, fill=WHITE, stroke=BORDER)
    c.setFillColor(color)
    c.rect(x, y, 4, h, fill=1, stroke=0)
    text(c, x + 16, y + h - 18, title, FONT_B, 11, TEXT)
    if sub:
        text(c, x + 16, y + h - 31, sub, FONT, 8.3, MUTED)
    if items:
        ix = x + 16
        iy = y + 14
        for it in items:
            ww = sw(it, FONT, 7.4) + 12
            if ix + ww > x + w - 10:
                ix = x + 16
                iy -= 18
            rounded(c, ix, iy - 6, ww, 15, r=3, fill=LIGHT, stroke=HexColor("#E3E9F2"))
            text(c, ix + 6, iy - 1.5, it, FONT, 7.4, TEXT)
            ix += ww + 5


def s08_arch(c, num):
    page_bg(c)
    top = header(c, "02 / Проектирование", "Архитектура: WPF + MVVM + SQL Server",
                 "Слои разделены: интерфейс не пишет SQL, бот не обращается к базе, подключение — в одном месте.")

    x, w = M, 620
    layer(c, x, 350, w, 56, "Views  •  WPF / XAML", "12 XAML-экранов: DataGrid, формы, навигация, стили", BLUE_L)
    arrow(c, x + w / 2, 346, x + w / 2, 324, BLUE, 1.2)
    text(c, x + w / 2 + 10, 329, "Binding  •  Commands", FONT, 7.2, MUTED)

    layer(c, x, 266, w, 54, "ViewModels  •  MVVM", "11 моделей представления, RelayCommand, ViewModelBase", BLUE)
    arrow(c, x + w / 2, 262, x + w / 2, 240, BLUE, 1.2)
    text(c, x + w / 2 + 10, 245, "вызовы сервисов", FONT, 7.2, MUTED)

    layer(c, x, 158, w, 78, "Services  •  бизнес-логика",
          "авторизация, сессия, безопасность, бот, поддержка, доступ к данным", ORANGE,
          ["AuthService", "Session", "SecurityHelper", "BotEngine", "BotKnowledge", "SupportInfo", "DatabaseHelper"])
    arrow(c, x + w / 2, 154, x + w / 2, 132, BLUE, 1.2)
    text(c, x + w / 2 + 10, 137, "Microsoft.Data.SqlClient", FONT, 7.2, MUTED)

    layer(c, x, 72, w, 56, "SQL Server  •  LocalDB", "9 таблиц, 8 индексов, внешние ключи и CHECK-ограничения", NAVY)

    # правая колонка
    px, pw = 690, 222
    rounded(c, px, 342, pw, 116, r=7, fill=WHITE, stroke=BORDER)
    text(c, px + 14, 438, "СТЕК", FONT_B, 7.6, ORANGE)
    stack = [".NET 8", "WPF", "MVVM", "ADO.NET", "SQL Server LocalDB"]
    yy = 418
    for s in stack:
        text(c, px + 14, yy, "•", FONT_B, 9, ORANGE)
        text(c, px + 26, yy, s, FONT, 9.2, TEXT)
        yy -= 19

    rounded(c, px, 150, pw, 176, r=7, fill=NAVY, stroke=None)
    text(c, px + 14, 302, "ПРИНЦИПЫ", FONT_B, 7.6, ORANGE)
    items = [
        ("Один вход в БД", "DatabaseHelper"),
        ("Бот без SQL", "знания — в коде"),
        ("Тонкий UI", "логика — в VM и сервисах"),
        ("Права в сессии", "Session.CurrentUser"),
    ]
    yy = 280
    for t, d in items:
        text(c, px + 14, yy, t, FONT_B, 8.8, WHITE)
        text(c, px + 14, yy - 12, d, FONT, 7.4, HexColor("#AFC0D6"))
        yy -= 36


# ---------------- 9. ER упрощённая ----------------

def entity(c, x, y, w, h, name, fields, color=BLUE):
    rounded(c, x, y, w, h, r=4, fill=WHITE, stroke=HexColor("#CBD6E5"))
    c.setFillColor(color)
    c.rect(x, y + h - 17, w, 17, fill=1, stroke=0)
    text(c, x + 8, y + h - 12, name, FONT_B, 8.4, WHITE)
    yy = y + h - 29
    for f in fields:
        text(c, x + 8, yy, f, FONT, 7.0, MUTED)
        yy -= 9.2


def rel(c, pts, label="1:N", lx=None, ly=None):
    for i in range(len(pts) - 1):
        line(c, pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], HexColor("#9DB0C7"), 0.9)
    if lx is not None:
        tw = sw(label, FONT_B, 6.4) + 4
        c.setFillColor(HexColor("#FAFBFD"))
        c.rect(lx - 2, ly - 2, tw, 8, fill=1, stroke=0)
        text(c, lx, ly, label, FONT_B, 6.4, BLUE)


def s09_er(c, num):
    page_bg(c)
    top = header(c, "02 / Проектирование", "Модель данных: 9 таблиц на весь контур",
                 "Справочники, документы и позиции. Остаток не редактируется вручную: он следствие операций.")

    entity(c, 48, 368, 186, 34, "Roles", ["Id  •  Name  •  UQ_Name"], NAVY)
    entity(c, 48, 286, 186, 66, "Users", ["Id  •  Login  •  Password", "SHA-256  •  FullName", "RoleId (FK)"], BLUE)
    entity(c, 48, 196, 186, 64, "SupportTickets", ["Id  •  UserId (FK)  •  Subject", "Description  •  Contact", "Status  •  CreatedAt"], ORANGE)
    entity(c, 48, 110, 186, 48, "SystemSettings", ["Id = 1 (CHECK)", "WarehouseName  •  Address"], MUTED)

    entity(c, 330, 368, 200, 34, "Categories", ["Id  •  Name"], BLUE)
    entity(c, 330, 286, 200, 66, "Products", ["Id  •  Name  •  CategoryId (FK)", "Description  •  Price  •  Unit", "Quantity ≥ 0 (CHECK)"], BLUE)
    entity(c, 330, 196, 200, 64, "DocumentItems", ["Id  •  DocumentId (FK)", "ProductId (FK)", "Quantity > 0  •  Price ≥ 0"], ORANGE)
    entity(c, 330, 110, 200, 64, "Documents", ["Id  •  DocType (Income/Outcome)", "DocDate  •  ContractorId (FK)", "UserId (FK)  •  TotalAmount"], NAVY)

    entity(c, 610, 286, 186, 50, "Contractors", ["Id  •  Name  •  Phone  •  Address"], NAVY)

    # связи
    rel(c, [(141, 368), (141, 352)], "1:N", 148, 356)
    rel(c, [(141, 286), (141, 260)], "1:N", 148, 268)
    rel(c, [(234, 319), (300, 319), (300, 142), (330, 142)], "1:N", 304, 150)
    rel(c, [(430, 368), (430, 352)], "1:N", 437, 356)
    rel(c, [(430, 286), (430, 260)], "1:N", 437, 268)
    rel(c, [(430, 196), (430, 174)], "1:N", 437, 178)
    rel(c, [(610, 311), (566, 311), (566, 142), (530, 142)], "1:N", 569, 150)

    # пояснение
    rounded(c, 610, 110, 302, 64, r=6, fill=BLUE_PALE, stroke=None)
    text(c, 624, 158, "ОСТАТОК", FONT_B, 6.8, BLUE)
    para(c, 624, 148, 274,
         "Хранится в Products. Меняется только транзакцией документа или сохранением инвентаризации.",
         8.2, 11, TEXT)

    # ограничения
    rounded(c, M, 50, W - M * 2, 38, r=6, fill=WHITE, stroke=BORDER)
    text(c, M + 14, 69, "ЦЕЛОСТНОСТЬ", FONT_B, 7.2, ORANGE)
    text(c, M + 110, 69, "CHECK Quantity ≥ 0   •   FK 547: понятная ошибка   •   ON DELETE CASCADE для позиций   •   транзакции",
         FONT, 8.9, TEXT)


# ---------------- 10. утверждённая схема БД ----------------

def s10_er_approved(c, num):
    page_bg(c)
    top = header(c, "02 / Проектирование", "Схема данных приложения",
                 "Логическая модель: справочники, пользователи и роли, операции, документы, отчёты и модуль помощи.")
    image(c, os.path.join(ASSETS, "er_full.jpg"), 40, 82, 880, 330, border=True, pad=4)
    text(c, 48, 66, "9 сущностей  •  3 роли  •  приход и расход  •  позиции документа  •  отчёты и модули",
         FONT, 7.8, MUTED)


# ---------------- 11. семантическая модель ----------------

def s11_semantic(c, num):
    page_bg(c, dark=True)
    c.setFillColor(HexColor("#0E1120"))
    c.rect(0, 0, W, H, fill=1, stroke=0)

    text(c, M, 502, "02 / ПРОЕКТИРОВАНИЕ", FONT_B, 8.2, ORANGE)
    c.setFillColor(ORANGE)
    c.rect(M, 491, 24, 2, fill=1, stroke=0)
    text(c, M, 462, "Семантическая модель", FONT_B, 25, WHITE)
    para(c, M, 443, 350,
         "Единый словарь объектов, действий и участников. На нём держатся база, интерфейс и ответы помощника.",
         9.8, 13, HexColor("#AFC0D6"))

    image(c, os.path.join(ASSETS, "graph_full.jpg"), 408, 42, 528, 468, border=False, pad=0, bg=NAVY)

    yy = 396
    text(c, M, yy, "КАК ЧИТАЕМ ГРАФ", FONT_B, 7.6, ORANGE)
    items = [
        ("Объекты", "товар, категория, документ, остаток, отчёт"),
        ("Действия", "изменяет, формирует, проводит, входит в"),
        ("Участники", "роли, чат-бот, техподдержка, пользователь"),
    ]
    yy -= 24
    for t, d in items:
        text(c, M, yy, t, FONT_B, 9.8, WHITE)
        para(c, M, yy - 13, 340, d, 8.4, 11.5, HexColor("#AFC0D6"))
        yy -= 48

    stats = [("126", "узлов дерева"), ("41", "вопрос"), ("85", "действий"), ("11", "тем")]
    sx, sy = M, 168
    for i, (n, lab) in enumerate(stats):
        bx = sx + (i % 2) * 168
        by = sy - (i // 2) * 58
        rounded(c, bx, by, 154, 50, r=5, fill=HexColor("#1A2C42"), stroke=HexColor("#2B425E"))
        text(c, bx + 12, by + 23, n, FONT_B, 19, ORANGE)
        text(c, bx + 54, by + 22, lab, FONT, 7.8, HexColor("#AFC0D6"))

    line(c, M, 100, 360, 100, HexColor("#2B425E"), 0.7)
    para(c, M, 90, 350,
         "Один словарь — одинаковые названия в базе, интерфейсе и ответах бота.",
         8.4, 11, HexColor("#8FA6C0"))
    text(c, M, 44, "Чат-бот работает по этой же модели данных",
         FONT, 7.4, HexColor("#7F95B0"))


# ---------------- 12. схема работы пользователя ----------------

def s12_flow(c, num):
    page_bg(c)
    top = header(c, "02 / Проектирование", "Схема работы пользователя",
                 "Полный маршрут: от вопроса «что нужно сделать?» до результата, отчёта или обращения в поддержку.")
    image(c, os.path.join(ASSETS, "flow_full.jpg"), 40, 58, 610, 366, border=True, pad=3)

    x, w = 676, 236
    text(c, x, top - 2, "СЕМЬ ВЕТОК", FONT_B, 7.6, ORANGE)
    branches = [
        ("Приход", "документ увеличивает остаток", GREEN),
        ("Расход", "проверка остатка перед записью", RED),
        ("Товары", "каталог, приход, инвентаризация", BLUE),
        ("История", "удаление и обратный пересчёт", ORANGE),
        ("Вход и доступ", "роль, меню, пользователи", NAVY),
        ("Отчёты", "период, отчёт, CSV", BLUE),
        ("Техподдержка", "подсказка, обращение, номер", ORANGE),
    ]
    yy = top - 30
    for name, desc, color in branches:
        c.setFillColor(color)
        c.rect(x, yy - 4, 3, 28, fill=1, stroke=0)
        text(c, x + 10, yy + 10, name, FONT_B, 9.4, TEXT)
        text(c, x + 10, yy - 2, desc, FONT, 7.4, MUTED)
        yy -= 39


# ---------------- 13–14. детали сценариев ----------------

def scenario_slide(c, num, kicker, title, subtitle, image_name, panel_title, rules, footer_note=None):
    page_bg(c)
    top = header(c, kicker, title, subtitle)
    image(c, os.path.join(ASSETS, image_name), 40, 62, 588, 374, border=True, pad=3)
    text(c, 48, 52, "фрагмент схемы", FONT, 6.6, MUTED_2)
    x, w = 650, 262
    text(c, x, top - 8, panel_title, FONT_B, 7.6, ORANGE)
    yy = top - 30
    for i, (t, d) in enumerate(rules, 1):
        numbered(c, x, yy + 2, i, d=16, color=BLUE, size=7.4)
        text(c, x + 24, yy, t, FONT_B, 9.6, TEXT)
        ph = para(c, x + 24, yy - 5, w - 24, d, 8.2, 11.4, MUTED)
        yy -= ph + 26
    if footer_note:
        rounded(c, x, 62, w, 54, r=6, fill=BLUE_PALE, stroke=None)
        para(c, x + 12, 104, w - 24, footer_note, 8.2, 11.2, BLUE)


def s13_scenario_income(c, num):
    scenario_slide(
        c, num, "02 / Проектирование", "Сценарий: приход, расход и товары",
        "Слева — ветки прихода и расхода, справа — каталог. Остаток меняется только через документ.",
        "flow_income_fade.jpg", "ТРИ ПРАВИЛА",
        [("Документ — основание", "Приход и расход сохраняются вместе с позициями и остатком: одна транзакция."),
         ("Расход проверяет остаток", "Если просят больше, чем есть, программа покажет доступное количество и не сохранит документ."),
         ("Товар без документа", "Новый товар создаётся с остатком 0; на учёт его ставит приход, факт — инвентаризация.")],
        "Остаток нельзя «поправить руками» в карточке товара — это защищает историю от незаметных изменений.")


def s14_scenario_access(c, num):
    scenario_slide(
        c, num, "02 / Проектирование", "Сценарий: отчёты и поддержка",
        "Правая ветка: отчёт по периоду и обращение, которое не теряется. Роль определяет доступ.",
        "flow_reports2_fade.jpg", "ТРИ ПРАВИЛА",
        [("Отчёт по роли", "Менеджер и администратор выбирают отчёт; кладовщик получает понятный отказ и подсказку."),
         ("Период и данные", "Остатки — на дату, движение — за интервал; результат можно выгрузить в CSV."),
         ("Обращение с номером", "Бот передаёт вопрос, форма фиксирует тему и описание, статус меняет администратор.")],
        "Если подсказки недостаточно — обращение, контакты и контроль статуса: «Новое», «В работе», «Закрыто».")
