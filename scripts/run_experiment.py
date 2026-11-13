"""Конвейер «данные -> результат -> страница» (P3).

Читает data/measurements.csv, считает линейную регрессию по группам,
пишет график и таблицы в docs/generated/. Результат кэшируется по
SHA-256 входных данных и самого скрипта: если хеш не изменился, расчёт пропускается.
"""
import hashlib, json, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "measurements.csv"
OUT = ROOT / "docs" / "generated"
CACHE = ROOT / ".cache" / "experiment.json"
OUTPUTS = ["fit.png", "metrics.csv", "metrics.md", "figure.md"]


def input_hash() -> str:
    h = hashlib.sha256()
    for p in (DATA, Path(__file__)):
        h.update(p.read_bytes())
    return h.hexdigest()


def main() -> int:
    t0 = time.perf_counter()
    key = input_hash()
    OUT.mkdir(parents=True, exist_ok=True)
    if CACHE.exists() and json.loads(CACHE.read_text())["key"] == key \
            and all((OUT / n).exists() for n in OUTPUTS):
        print(f"[experiment] CACHE HIT {key[:12]} — расчёт пропущен "
              f"({time.perf_counter() - t0:.3f} s)")
        return 0

    print(f"[experiment] CACHE MISS {key[:12]} — выполняю расчёт")
    import numpy as np, pandas as pd
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    df = pd.read_csv(DATA)
    fig, ax = plt.subplots(figsize=(7, 4), dpi=110)
    rows = []
    for (g, d), c in zip(df.groupby("group"), ("#1f77b4", "#d95f02")):
        slope, icpt = np.polyfit(d.x, d.y, 1)
        pred = slope * d.x + icpt
        ss_res = float(((d.y - pred) ** 2).sum())
        ss_tot = float(((d.y - d.y.mean()) ** 2).sum())
        rows.append({"Группа": g, "N": len(d), "Наклон": round(slope, 4),
                     "Сдвиг": round(icpt, 4), "R²": round(1 - ss_res / ss_tot, 4),
                     "RMSE": round((ss_res / len(d)) ** 0.5, 4)})
        ax.scatter(d.x, d.y, s=10, color=c, alpha=.6, label=f"группа {g}")
        ax.plot(d.x, pred, color=c, lw=2)
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.grid(alpha=.3); ax.legend()
    fig.tight_layout(); fig.savefig(OUT / "fit.png"); plt.close(fig)
    # Адрес картинки меняется вместе с данными (?v=<хеш>), иначе браузер
    # показывает старый fit.png из кэша, хотя таблица уже новая.
    (OUT / "figure.md").write_text(
        f"![Регрессия по группам](generated/fit.png?v={key[:12]})\n", encoding="utf-8")

    m = pd.DataFrame(rows)
    m.to_csv(OUT / "metrics.csv", index=False)
    (OUT / "metrics.md").write_text(m.to_markdown(index=False) if _has_tabulate()
                                    else _md(m), encoding="utf-8")
    CACHE.parent.mkdir(exist_ok=True)
    CACHE.write_text(json.dumps({"key": key}))
    print(f"[experiment] готово за {time.perf_counter() - t0:.2f} s")
    return 0


def _has_tabulate() -> bool:
    try:
        import tabulate  # noqa: F401
        return True
    except ImportError:
        return False


def _md(df) -> str:
    head = "| " + " | ".join(df.columns) + " |\n"
    sep = "|" + "|".join("---" for _ in df.columns) + "|\n"
    body = "".join("| " + " | ".join(map(str, r)) + " |\n" for r in df.values)
    return head + sep + body


if __name__ == "__main__":
    sys.exit(main())
