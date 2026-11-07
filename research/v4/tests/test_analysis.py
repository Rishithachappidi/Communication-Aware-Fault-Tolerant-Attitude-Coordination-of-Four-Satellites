import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from analyze_v4 import correct_premise_flags


class PremiseTests(unittest.TestCase):
    def record(self, start, end, scenario="pointing"):
        return dict(condition="beam", condition_value="0.9", scenario=scenario,
                    seed="4001", method="UAD", certificate_premises="1", start_s=str(start), finish_s=str(end))

    def test_mid_probe_fault_invalidates_constancy(self):
        rows, fixes = correct_premise_flags([self.record(1.06, 3.94)])
        self.assertEqual(rows[0]["certificate_premises"], "0")
        self.assertEqual(rows[0]["certificate_premises_recorded"], "1")
        self.assertEqual(len(fixes), 1)

    def test_post_fault_window_is_unchanged(self):
        rows, fixes = correct_premise_flags([self.record(2.04, 4.92)])
        self.assertEqual(rows[0]["certificate_premises"], "1")
        self.assertFalse(fixes)

    def test_window_ending_before_fault_is_unchanged(self):
        rows, fixes = correct_premise_flags([self.record(1.06, 2.0)])
        self.assertEqual(rows[0]["certificate_premises"], "1")
        self.assertFalse(fixes)

    def test_gain_only_case_does_not_invent_offset_jump(self):
        rows, fixes = correct_premise_flags([self.record(1.06, 3.94, "attenuation_only")])
        self.assertEqual(rows[0]["certificate_premises"], "1")
        self.assertFalse(fixes)


if __name__ == "__main__":
    unittest.main()
