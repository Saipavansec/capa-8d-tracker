# CAPA / 8D Tracker

A lightweight Corrective and Preventive Action (CAPA) tracker implementing the
**8D problem-solving workflow** (D0–D8), with 5-Why root cause capture,
containment / corrective / preventive actions, and a Streamlit KPI dashboard.

## Features

- SQLite-backed CAPA register (severity, owner, due dates, status)
- 8D step workflow with per-step completion validation
- 5-Why root cause records linked to each CAPA
- Action tracking (containment, corrective, preventive)
- Streamlit dashboard: open/overdue counts, 8D progress, Pareto of root-cause
  categories, aging

## Quick start

```bash
pip install -r requirements.txt
python examples/seed.py        # create capa.db with sample data
streamlit run app.py
```

## 8D steps

D0 Plan · D1 Team · D2 Problem description · D3 Interim containment ·
D4 Root cause · D5 Corrective actions · D6 Implement & validate ·
D7 Prevent recurrence · D8 Closure

## Tests

```bash
python -m unittest discover -s tests -v
```
