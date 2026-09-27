"""Seed capa.db with sample CAPAs demonstrating the 8D workflow."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from capa_tracker import (add_action, add_five_why, complete_step, create_capa,
                          get_connection, init_db, set_step)

conn = init_db("capa.db")

samples = [
    ("Surface finish out of spec on housing",
     "Polishing line producing Ra > 1.6 um on 12% of housings.",
     "high", "J. Rivera", "2026-10-15", "Process"),
    ("Supplier dimensional nonconformance",
     "Incoming shaft diameter below LSL on lot S-2211.",
     "critical", "A. Chen", "2026-09-30", "Supplier"),
    ("Label mix-up on packaging line",
     "Wrong revision label applied to 40 units before detection.",
     "medium", "P. Nair", "2026-11-01", "Human factors"),
    ("Torque audit failures",
     "Fastener torque below minimum on final audit sample.",
     "high", "J. Rivera", "2026-10-20", "Process"),
    ("Calibration overdue on CMM-02",
     "CMM used 11 days past calibration due date.",
     "medium", "A. Chen", "2026-09-25", "System"),
    ("Repeat customer complaint: seal leakage",
     "Third complaint this quarter for seal leakage on pump P-400.",
     "critical", "P. Nair", "2026-10-05", "Design"),
]

for title, desc, sev, owner, due, category in samples:
    cid = create_capa(conn, title, description=desc, severity=sev,
                      owner=owner, due_date=due, root_cause_category=category)
    set_step(conn, cid, "D2", {"what": title, "where": "Line 2",
                               "when": "2026-09", "extent": "see description"})
    add_five_why(conn, cid, 1, "Why did it happen?",
                 "Initial cause under investigation.")
    add_action(conn, cid, "containment", "Quarantine suspect lots", owner=owner)
    for step in ("D0", "D1", "D2"):
        complete_step(conn, cid, step)

print(f"seeded {len(samples)} sample CAPAs into capa.db")
