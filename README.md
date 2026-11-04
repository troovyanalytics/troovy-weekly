# Troovy Data Weekly

The data team's weekly page: big achievements, wins, adhoc work, upcoming work, and the
work split by area. Every push to `main` rebuilds it and publishes it on GitHub Pages.

## Each week

1. Add `data/weeks/<monday>.json` (copy last week's file and change it).
2. Check it locally: `python3 build_static.py`, then open `site/index.html`.
3. Commit and push to `main`. The page is live 1-2 minutes later.

You can also edit a week file straight on github.com. Saving it there is a push too.

## Week file

```json
{
  "start": "2026-11-02",
  "end": "2026-11-08",
  "headline": "One line for the week",
  "stats": [{"value": "42.5%", "label": "real COGS of net sales"}],
  "items": [
    {"section": "big", "area": "analytics", "date": "2026-11-02",
     "title": "Short title", "detail": "One or two lines on why it matters."}
  ],
  "upcoming": [
    {"area": "software", "when": "Fri 6 Nov", "status": "in progress",
     "title": "Short title", "detail": "One line."}
  ]
}
```

| Field | Allowed values |
|---|---|
| `section` | `big` (big achievement), `win`, `adhoc` (a request that came in during the week) |
| `area` | `engineering` (pipelines, syncs, data models), `devops` (AWS, Fargate, alerts, cost), `analytics` (dashboards, P&L, forecasts), `software` (apps and tools) |
| `status` (upcoming only) | `planned`, `in progress`, `blocked`, `waiting`, `done` |

The file name must be the Monday (`start`), and `end` the Sunday after it. The build stops
with a clear message if any of this is wrong, so a typo never reaches the live page.

The work split counts this week's `items` per area. Upcoming work is not counted.
