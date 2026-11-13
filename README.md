# python-web — публикация результатов эксперимента (MkDocs Material)

[![Build & Deploy](https://github.com/SolarVonBro/python-web-ssg/actions/workflows/pages.yml/badge.svg)](https://github.com/SolarVonBro/python-web-ssg/actions/workflows/pages.yml)

```bash
python -m venv .venv && . .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
make site          # расчёт (с кэшем) + метка версии + mkdocs build --strict
make serve         # предпросмотр
```

Лицензии: код — MIT (`LICENSE`), контент — CC BY 4.0 (`LICENSE-CONTENT`).
Отчёт — раздел «Отчёт» на сайте ([`docs/report.md`](docs/report.md)); версия для печати — [`docs/assets/otchet-zadanie-1.pdf`](docs/assets/otchet-zadanie-1.pdf).
