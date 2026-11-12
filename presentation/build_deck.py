# -*- coding: utf-8 -*-
"""Сборка итоговой презентации: 29 слайдов в один PDF."""
from reportlab.pdfgen import canvas
from theme import W, H, footer
import slides_part1 as p1
import slides_part2 as p2
import slides_part3 as p3
import slides_part4 as p4

OUT = "Складской_учет_PRO_презентация.pdf"

slides = [
    (p1.s01_title, None, "Титул"),
    (p1.s02_problem, 2, "Проблема"),
    (p1.s03_goal, 3, "Цель и задачи"),
    (p1.s04_analogs, 4, "Аналоги"),
    (p1.s05_conclusions, 5, "Выводы по аналогам"),
    (p2.s06_roles, 6, "Роли"),
    (p2.s07_map, 7, "Функциональная карта"),
    (p2.s08_arch, 8, "Архитектура"),
    (p2.s09_er, 9, "Модель данных"),
    (p2.s10_er_approved, 10, "Схема базы (утверждённая)"),
    (p2.s11_semantic, 11, "Схема понятий"),
    (p2.s12_flow, 12, "Блок-схема"),
    (p2.s13_scenario_income, 13, "Сценарий: приход"),
    (p2.s14_scenario_access, 14, "Сценарий: доступ"),
    (p3.s15_divider, 15, "Как работает приложение"),
    (p3.s16_dashboard, 16, "Главная"),
    (p3.s17_products, 17, "Товары"),
    (p3.s18_operations, 18, "Приход и расход"),
    (p3.s19_history, 19, "История операций"),
    (p3.s20_reports, 20, "Отчёты"),
    (p3.s21_bot, 21, "Помощник: дерево"),
    (p3.s22_dialog, 22, "Помощник: диалог"),
    (p3.s23_support, 23, "Техподдержка"),
    (p3.s24_admin, 24, "Администрирование"),
    (p4.s26_problems, 25, "Проблемы и решения"),
    (p4.s27_stages, 26, "Этапы разработки"),
    (p4.s28_results, 27, "Итоги"),
    (p4.s29_thanks, 28, "Финал"),
]

c = canvas.Canvas(OUT, pagesize=(W, H))
c.setTitle("Складской учёт PRO — итоговый проект")
c.setAuthor("Складской учёт PRO")
c.setSubject("Презентация итогового проекта: WPF-приложение складского учёта")

for i, (fn, num, title) in enumerate(slides, 1):
    key = f"slide{i}"
    c.bookmarkPage(key)
    c.addOutlineEntry(f"{i}. {title}", key, level=0)
    if num is None:
        fn(c)
    else:
        fn(c, num)
        footer(c, num, dark=(num in (15, 28)))
    c.showPage()

c.save()
print("ok", len(slides), "slides ->", OUT)
