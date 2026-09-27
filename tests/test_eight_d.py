"""Unit tests for the 8D workflow helpers (stdlib unittest)."""

import unittest

from capa_tracker.eight_d import STEPS, overall_progress, validate_step


class TestEightD(unittest.TestCase):
    def test_step_count(self):
        self.assertEqual(len(STEPS), 9)
        self.assertEqual(STEPS[0][0], "D0")
        self.assertEqual(STEPS[-1][0], "D8")

    def test_validate_step_missing_fields(self):
        missing = validate_step("D2", {"what": "x"})
        self.assertIn("where", missing)
        self.assertIn("when", missing)
        self.assertIn("extent", missing)

    def test_validate_step_complete(self):
        content = {"what": "a", "where": "b", "when": "c", "extent": "d"}
        self.assertEqual(validate_step("D2", content), [])

    def test_validate_step_unknown(self):
        with self.assertRaises(ValueError):
            validate_step("D9", {})

    def test_overall_progress(self):
        state = {"D0": True, "D1": True}
        self.assertAlmostEqual(overall_progress(state), 200 / 9, places=1)
        full = {code: True for code, _, _ in STEPS}
        self.assertEqual(overall_progress(full), 100.0)
        self.assertEqual(overall_progress({}), 0.0)


if __name__ == "__main__":
    unittest.main()
