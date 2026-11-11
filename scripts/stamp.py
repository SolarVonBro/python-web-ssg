"""Метка версии: хеш коммита, дата сборки, версия набора данных."""
import datetime, os, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "generated"
OUT.mkdir(parents=True, exist_ok=True)


def sh(*a):
    try:
        return subprocess.check_output(a, cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


commit = os.environ.get("GITHUB_SHA", "")[:7] or sh("git", "rev-parse", "--short", "HEAD") or "unknown"
dirty = " (+uncommitted)" if sh("git", "status", "--porcelain") else ""
date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
ds = (ROOT / "data" / "VERSION").read_text().strip()
(OUT / "version.md").write_text(
    f"| Коммит | Дата сборки | Версия набора данных |\n|---|---|---|\n"
    f"| `{commit}{dirty}` | {date} | `{ds}` |\n", encoding="utf-8")
print(f"[stamp] {commit}{dirty} {date} dataset={ds}")
