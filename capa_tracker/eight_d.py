"""8D problem-solving workflow: step definitions and completion validation."""

from __future__ import annotations

# (code, title, required content fields)
STEPS = [
    ("D0", "Plan: prepare for the 8D process",
     ["objective", "team_lead"]),
    ("D1", "Team: establish a cross-functional team",
     ["members"]),
    ("D2", "Problem: describe the problem (5W2H)",
     ["what", "where", "when", "extent"]),
    ("D3", "Containment: interim containment actions",
     ["actions"]),
    ("D4", "Root cause: verified root cause (5 Why / fishbone)",
     ["root_cause", "verification"]),
    ("D5", "Corrective actions: choose permanent corrective actions",
     ["actions"]),
    ("D6", "Implement & validate corrective actions",
     ["evidence"]),
    ("D7", "Prevent recurrence: systemic preventive actions",
     ["actions"]),
    ("D8", "Closure: recognize the team and close the CAPA",
     ["summary"]),
]


def validate_step(step_code, content):
    """Return the list of missing required fields for an 8D step.

    Raises ValueError for an unknown step code.
    """
    for code, _, required in STEPS:
        if code == step_code:
            content = content or {}
            return [f for f in required if not content.get(f)]
    raise ValueError(f"unknown 8D step: {step_code}")


def overall_progress(steps_state):
    """Compute 0-100 progress from a {step_code: completed_bool} mapping."""
    done = sum(1 for code, _, _ in STEPS if steps_state.get(code))
    return round(100 * done / len(STEPS), 1)
