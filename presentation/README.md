# Презентация «Складской учёт PRO»

Итоговый PDF: `Складской_учет_PRO_презентация.pdf` (28 слайдов, 16:9, 960×540 pt).

## Как пересобрать

```bash
pip install --break-system-packages reportlab pillow pymupdf
python3 build_deck.py
```

`build_deck.py` собирает все слайды и добавляет закладки по разделам.
Слайды разложены по файлам: `slides_part1.py` (1–5), `slides_part2.py` (6–14),
`slides_part3.py` (15–24), `slides_part4.py` (25–28). Экраны приложения —
векторные макеты в `mockups.py`, дизайн-система — в `theme.py`.
Схемы проекта лежат в `assets/` (`graph_full.jpg`, `er_full.jpg`,
`flow_full.jpg` и кропы для слайдов 13–14).
