"""Build the weekly page: data/weeks/*.json + template.html -> site/index.html.

Usage: python3 build_static.py [--week YYYY-MM-DD]
  --week  week (Monday) to open by default; the latest week if left out.

The output is one self-contained HTML file (all weeks embedded). GitHub Pages serves it,
and the same file can be shared on WhatsApp. The build fails on a bad week file, so a typo
never reaches the live page.
"""
import argparse
import datetime as dt
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
SECTIONS = {"big", "win", "adhoc"}
AREAS = {"engineering", "devops", "analytics", "software"}
STATUSES = {"planned", "in progress", "blocked", "waiting", "done"}
SKELETON = (
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
    "</head><body>"
)


def check_week(path, week):
    errors = []
    where = path.name
    try:
        start = dt.date.fromisoformat(week["start"])
        end = dt.date.fromisoformat(week["end"])
    except (KeyError, ValueError) as e:
        return [f"{where}: start/end missing or not YYYY-MM-DD ({e})"]
    if path.stem != week["start"]:
        errors.append(f"{where}: file name must be the week's start date {week['start']}.json")
    if start.weekday() != 0 or end != start + dt.timedelta(days=6):
        errors.append(f"{where}: start must be a Monday and end the Sunday after it")
    for i, it in enumerate(week.get("items", [])):
        tag = f"{where} items[{i}] {it.get('title', '?')!r}"
        if it.get("section") not in SECTIONS:
            errors.append(f"{tag}: section must be one of {sorted(SECTIONS)}")
        if it.get("area") not in AREAS:
            errors.append(f"{tag}: area must be one of {sorted(AREAS)}")
        if not it.get("title"):
            errors.append(f"{tag}: title is empty")
    for i, it in enumerate(week.get("upcoming", [])):
        tag = f"{where} upcoming[{i}] {it.get('title', '?')!r}"
        if it.get("area") not in AREAS:
            errors.append(f"{tag}: area must be one of {sorted(AREAS)}")
        if it.get("status") and it["status"] not in STATUSES:
            errors.append(f"{tag}: status must be one of {sorted(STATUSES)}")
        if not it.get("title"):
            errors.append(f"{tag}: title is empty")
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", help="week (Monday) to open by default")
    args = ap.parse_args()

    weeks, errors = [], []
    for f in sorted((HERE / "data" / "weeks").glob("*.json")):
        try:
            week = json.loads(f.read_text())
        except json.JSONDecodeError as e:
            errors.append(f"{f.name}: not valid JSON ({e})")
            continue
        errors += check_week(f, week)
        weeks.append({"id": f.stem, "data": week})
    if errors:
        sys.exit("Build stopped, fix these first:\n  " + "\n  ".join(errors))
    if not weeks:
        sys.exit("no week files in data/weeks")

    selected = args.week or max(w["id"] for w in weeks)
    if not any(w["id"] == selected for w in weeks):
        sys.exit(f"week {selected} not found in data/weeks")

    built = dt.datetime.now(dt.timezone(dt.timedelta(hours=5, minutes=30))).strftime("%-d %b %Y, %H:%M IST")
    payload = json.dumps(weeks, ensure_ascii=False).replace("</", "<\\/")
    tag = (f'<script id="weeks-data" type="application/json" data-selected="{selected}" '
           f'data-built="{built}">{payload}</script>\n')
    page = (HERE / "template.html").read_text()
    marker = "<script>\n(function () {"
    if marker not in page:
        sys.exit("template.html: main script marker not found")
    page = page.replace(marker, tag + marker, 1)

    out = HERE / "site" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(SKELETON + page + "</body></html>\n")
    print(f"{out}  ({len(weeks)} weeks, default {selected})")


main()
