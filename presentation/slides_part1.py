# -*- coding: utf-8 -*-
"""Слайды 1–5: титул, проблема, цель, аналоги, выводы."""
import os
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from theme import *

ASSETS = os.path.join(HERE, "assets")


def network(c, nodes, edges, color=HexColor("#36506E"), label=HexColor("#AFC0D6"), r=26):
    for a, b in edges:
        x1, y1, _ = nodes[a]
        x2, y2, _ = nodes[b]
        c.setStrokeColor(HexColor("#2B425E"))
        c.setLineWidth(0.8)
        c.line(x1, y1, x2, y2)
    for name, (x, y, rad) in nodes.items():
        c.setFillColor(HexColor("#1A2C42"))
        c.setStrokeColor(color)
        c.setLineWidth(0.8)
        c.circle(x, y, rad, fill=1, stroke=1)
        text(c, x, y - 2.6, name, FONT, 7.2, label, "c")


def s01_title(c):
    page_bg(c, dark=True)
    # фоновые линии
    c.setStrokeColor(HexColor("#223750"))
    c.setLineWidth(0.6)
    for i in range(10):
        c.line(0, 70 + i * 52, W, 30 + i * 52)

    text(c, M, 492, "ИТОГОВЫЙ ПРОЕКТ  •  2026", FONT_B, 8.6, ORANGE)
    c.setFillColor(ORANGE)
    c.rect(M, 480, 28, 2.2, fill=1, stroke=0)

    text(c, M, 392, "Складской учёт", FONT_B, 50, WHITE)
    text(c, M, 340, "PRO", FONT_B, 50, ORANGE)
    text(c, M + sw("PRO", FONT_B, 50) + 14, 340, "— порядок вместо таблиц", FONT, 15, HexColor("#8FA6C0"))

    para(c, M, 300, 520,
         "Десктопное приложение для небольшого склада: товары, приход и расход, "
         "инвентаризация, отчёты, три роли, встроенный чат-бот и техподдержка.",
         12.6, 18, HexColor("#C6D3E2"))

    line(c, M, 238, M + 520, 238, HexColor("#2B425E"), 1)
    text(c, M, 212, "Выполнил(а):  ______________________________", FONT, 10, HexColor("#AFC0D6"))
    text(c, M, 192, "Группа:  ______________        Руководитель:  ______________________", FONT, 10, HexColor("#AFC0D6"))

    x = M
    for label in [".NET 8", "WPF", "MVVM", "SQL Server", "MSTest"]:
        x += pill(c, x, 128, label, 7.4, HexColor("#BFD0E3"), HexColor("#1C3048"),
                  HexColor("#324A66")) + 7

    text(c, M, 82, "Локальная работа  •  без подписки  •  без интернета  •  с помощником внутри",
         FONT, 9, HexColor("#7F95B0"))

    nodes = {
        "Товар": (700, 356, 30),
        "Документ": (812, 292, 31),
        "Остаток": (682, 252, 27),
        "Категория": (790, 190, 27),
        "Отчёт": (858, 398, 24),
        "Пользователь": (610, 400, 28),
        "Помощник": (704, 456, 30),
        "Техподдержка": (872, 168, 26),
        "Контрагент": (612, 210, 25),
    }
    edges = [("Товар", "Документ"), ("Товар", "Остаток"), ("Товар", "Категория"),
             ("Документ", "Остаток"), ("Документ", "Контрагент"), ("Отчёт", "Остаток"),
             ("Пользователь", "Документ"), ("Пользователь", "Помощник"),
             ("Помощник", "Техподдержка"), ("Техподдержка", "Остаток"),
             ("Отчёт", "Документ"), ("Пользователь", "Отчёт")]
    network(c, nodes, edges)
    # акцент на помощнике
    c.setStrokeColor(ORANGE)
    c.setLineWidth(1.4)
    c.circle(704, 456, 35, fill=0, stroke=1)


def s02_problem(c, num):
    page_bg(c)
    top = header(c, "01 / Анализ и постановка", "Учёт держится на таблицах и памяти",
                 "Небольшой склад живёт в Excel, переписке и опыте кладовщика. "
                 "Пока операций мало — работает; когда их становится больше — расходится с фактом.")
    cards = [
        ("01", "Остатки не сходятся", "Ручные правки, забытые операции и случайно изменённые формулы. "
                                      "Цифра в таблице перестаёт быть доказательством.", "РИСК: РАСХОЖДЕНИЕ С ФАКТОМ", RED),
        ("02", "Нет истории", "Не восстановить, кто и когда изменил остаток, какой документ был основанием "
                              "и что именно удалили.", "РИСК: НЕВОЗМОЖНО РАЗОБРАТЬСЯ", ORANGE),
        ("03", "Права — условные", "Кладовщик видит цены, настройки и пользователей. Разделение доступа "
                                    "держится на договорённости, а не на системе.", "РИСК: ЛИШНИЙ ДОСТУП", BLUE),
        ("04", "Помощь — вне программы", "Инструкция лежит отдельно, вопрос идёт «к знающему». Новый сотрудник "
                                          "учится методом проб и ошибок.", "РИСК: ДОЛГОЕ ОБУЧЕНИЕ", GREEN),
    ]
    cw, ch = 422, 140
    positions = [(M, top - ch), (M + cw + 20, top - ch), (M, top - ch * 2 - 18), (M + cw + 20, top - ch * 2 - 18)]
    for (n, title, body, risk, color), (x, y) in zip(cards, positions):
        card(c, x, y, cw, ch, accent=color)
        text(c, x + 20, y + ch - 28, n, FONT_B, 9, color)
        text(c, x + 42, y + ch - 29, title, FONT_B, 14.2, TEXT)
        para(c, x + 20, y + ch - 52, cw - 40, body, 9.6, 13.4, MUTED)
        text(c, x + 20, y + 16, risk, FONT_B, 6.8, color)

    rounded(c, M, 62, W - M * 2, 42, r=6, fill=NAVY, stroke=None)
    text(c, M + 18, 77, "Итог:", FONT_B, 10, ORANGE)
    text(c, M + 64, 77, "чем больше операций, тем дороже ошибка — и тем меньше доверия к учёту.",
         FONT, 11, WHITE)


def s03_goal(c, num):
    page_bg(c)
    top = header(c, "01 / Анализ и постановка", "Цель и задачи проекта",
                 "Сделать инструмент, который закрывает полный контур учёта и не требует отдельного внедрения.")

    # цель
    rounded(c, M, 74, 322, top - 74, r=9, fill=NAVY, stroke=None)
    c.setFillColor(ORANGE)
    c.rect(M, top - 6, 322, 6, fill=1, stroke=0)
    text(c, M + 22, top - 36, "ЦЕЛЬ", FONT_B, 8.4, ORANGE)
    para(c, M + 22, top - 54, 278,
         "Дать небольшому складу одно окно, в котором остатки, документы, роли и помощь "
         "работают вместе — без подписки и без интернета.", 14.2, 20, WHITE)
    line(c, M + 22, 214, M + 300, 214, HexColor("#36506E"), 0.8)
    text(c, M + 22, 192, "КРИТЕРИЙ УСПЕХА", FONT_B, 7.8, HexColor("#9FB3CB"))
    para(c, M + 22, 178, 278,
         "Сотрудник без обучения проводит приход или расход за 2–3 минуты, "
         "а остаток совпадает с фактом.", 9.6, 13, HexColor("#C6D3E2"))

    tasks = [
        ("01", "Разобрать аналоги", "Выделить минимально достаточный функционал для склада на 1–3 человека."),
        ("02", "Спроектировать модели", "Данные, семантика и сценарии — три схемы, принятые преподавателем."),
        ("03", "Реализовать ядро учёта", "Товары, приход, расход, инвентаризация и история операций."),
        ("04", "Добавить роли и отчёты", "Три роли, остатки и движение товара, экспорт в CSV."),
        ("05", "Встроить помощь", "Чат-бот по дереву решений и техподдержка с обращениями."),
        ("06", "Проверить и оформить", "Модульные тесты, скрипт создания БД и документация."),
    ]
    x0, y0 = 394, top - 96
    tw, th = 254, 104
    for i, (n, t, d) in enumerate(tasks):
        x = x0 + (i % 2) * (tw + 16)
        y = y0 - (i // 2) * (th + 12)
        card(c, x, y, tw, th, fill=WHITE, stroke=BORDER)
        numbered(c, x + 14, y + th - 12, n, d=18, color=BLUE_PALE, fg=BLUE, size=7.6)
        text(c, x + 40, y + th - 25, t, FONT_B, 10.6, TEXT)
        para(c, x + 14, y + th - 40, tw - 28, d, 8.8, 12, MUTED)


def table(c, x, top, widths, headers, rows, size=8.4, pad=7, header_h=26,
          row_min=24, highlight=None, align=None, header_fill=NAVY, zebra=True):
    # заголовок
    c.setFillColor(header_fill)
    c.rect(x, top - header_h, sum(widths), header_h, fill=1, stroke=0)
    cx = x
    for i, h in enumerate(headers):
        text(c, cx + pad, top - header_h + 9, h, FONT_B, size, WHITE)
        cx += widths[i]
    y = top - header_h
    for ri, row in enumerate(rows):
        # высота
        maxh = row_min
        for ci, cell in enumerate(row):
            lines = wrap_lines(str(cell), widths[ci] - pad * 2, FONT, size)
            maxh = max(maxh, len(lines) * (size * 1.28) + 10)
        y -= maxh
        fill = WHITE if ri % 2 == 0 or not zebra else HexColor("#F7F9FC")
        if highlight == ri:
            fill = NAVY
        c.setFillColor(fill)
        c.rect(x, y, sum(widths), maxh, fill=1, stroke=0)
        c.setStrokeColor(HexColor("#E7ECF3"))
        c.setLineWidth(0.5)
        c.line(x, y, x + sum(widths), y)
        cx = x
        for ci, cell in enumerate(row):
            col = WHITE if highlight == ri else TEXT
            fnt = FONT_B if (highlight == ri or ci == 0) else FONT
            lines = wrap_lines(str(cell), widths[ci] - pad * 2, fnt, size)
            ty = y + maxh - 7 - size
            for ln in lines:
                text(c, cx + pad, ty, ln, fnt, size, col)
                ty -= size * 1.28
            cx += widths[ci]
    return y


def s04_analogs(c, num):
    page_bg(c)
    top = header(c, "01 / Анализ и постановка", "Аналоги: что уже есть на рынке",
                 "Сравнили четыре класса решений по тому, что важно небольшому складу: цена, порог входа, роли и помощь.")
    widths = [156, 92, 126, 96, 142, 158, 94]
    headers = ["Продукт", "Тип", "Стоимость", "Порог входа", "Роли и учёт", "Помощь", "Интернет"]
    rows = [
        ("Excel", "файл", "0 ₽*", "низкий", "вручную, без ролей", "нет", "не нужен"),
        ("1С: Торговля и склад", "локально", "лицензия + внедрение", "высокий", "да, документы", "ИТС, справка", "не нужен"),
        ("МойСклад", "облако", "0–3 400 ₽/мес", "низкий", "да, документы", "поддержка", "обязателен"),
        ("WMS-класс (1С:WMS, Складо)", "локально / облако", "от 100 тыс. ₽", "высокий", "да, адресное хранение", "внедрение", "зависит"),
        ("Складской учёт PRO", "локально", "0 ₽**", "низкий", "3 роли, документы", "бот + тикеты", "не нужен"),
    ]
    table(c, M, top, widths, headers, rows, size=8.4, pad=7, row_min=51,
          highlight=4, header_fill=NAVY)
    text(c, M, 110, "ВЫВОД", FONT_B, 7.6, ORANGE)
    text(c, M + 52, 110,
         "Массовые продукты закрывают «большой» учёт, но требуют денег и внедрения. Excel бесплатен, но не даёт целостности.",
         FONT, 9.6, TEXT)
    para(c, M, 88, W - M * 2,
         "* при наличии офисного пакета.  ** SQL Server Express / LocalDB, без лицензионных платежей. "
         "Тарифы и условия — по открытым обзорам 2026 г.; точные цены уточняются у поставщиков. "
         "Источники: moysklad.ru, solutions.1c.ru, обзоры toolfox.ru и cleverence.ru.",
         7.4, 10.5, MUTED_2)


def s05_conclusions(c, num):
    page_bg(c)
    top = header(c, "01 / Анализ и постановка", "Выводы из аналогов: наша ниша",
                 "Аналоги задают планку, но ни один из них не закрывает задачу «маленький склад + помощь внутри».")

    # берём
    rounded(c, M, top - 238, 420, 238, r=8, fill=WHITE, stroke=BORDER)
    c.setFillColor(GREEN)
    c.rect(M, top - 6, 420, 6, fill=1, stroke=0)
    text(c, M + 18, top - 32, "БЕРЁМ", FONT_B, 8.4, GREEN)
    items = [
        ("Простота Excel", "таблицы, поиск, быстрый старт без обучения"),
        ("Дисциплина 1С", "документ — основание, остаток — следствие"),
        ("Чистота МойСклад", "минимум полей и понятные действия"),
        ("Роли и отчёты", "доступ по роли, остатки и движение товара"),
    ]
    y = top - 50
    for t, d in items:
        check(c, M + 20, y - 10, 9, GREEN)
        text(c, M + 38, y - 10, t, FONT_B, 10.4, TEXT)
        text(c, M + 38, y - 25, d, FONT, 8.8, MUTED)
        y -= 46

    # не берём
    x = M + 440
    rounded(c, x, top - 238, 424, 238, r=8, fill=WHITE, stroke=BORDER)
    c.setFillColor(RED)
    c.rect(x, top - 6, 424, 6, fill=1, stroke=0)
    text(c, x + 18, top - 32, "НЕ БЕРЁМ", FONT_B, 8.4, RED)
    items2 = [
        ("Адресное хранение и ТСД", "избыточно для склада на 1–3 человека"),
        ("Подписку и облако", "учёт не должен зависеть от интернета"),
        ("Внедрение как проект", "программа должна объяснять себя сама"),
    ]
    y = top - 50
    for t, d in items2:
        cross(c, x + 20, y - 8, 7, RED)
        text(c, x + 38, y - 10, t, FONT_B, 10.4, TEXT)
        text(c, x + 38, y - 25, d, FONT, 8.8, MUTED)
        y -= 58

    # ниша
    rounded(c, M, 58, W - M * 2, 104, r=8, fill=NAVY, stroke=None)
    c.setFillColor(ORANGE)
    c.rect(M, 58, 5, 104, fill=1, stroke=0)
    text(c, M + 22, 140, "НИША", FONT_B, 8.2, ORANGE)
    para(c, M + 22, 128, 790,
         "Локальное приложение для небольшого склада: бесплатно, без интернета, "
         "с помощником, который ведёт по шагам и открывает нужный раздел.",
         12.2, 15.5, WHITE)
    text(c, M + 22, 72, "Не «ещё одна 1С», а понятный инструмент, который не требует внедрения.",
         FONT, 9, HexColor("#AFC0D6"))
