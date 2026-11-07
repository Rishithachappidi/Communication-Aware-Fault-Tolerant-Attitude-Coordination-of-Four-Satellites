import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from statistics_tools import family_percentiles
class FamilyIntervalTest(unittest.TestCase):
 def test_one_family_is_two_sided_95(self):self.assertEqual(family_percentiles(),(.025,.975))
 def test_adjusted_interval_contains_unadjusted_tails(self):
  for m in [6,9,36]:
   a,b=family_percentiles(families=m);self.assertLessEqual(a,.025);self.assertGreaterEqual(b,.975);self.assertAlmostEqual(a+b,1)
 def test_invalid_family_rejected(self):
  with self.assertRaises(ValueError):family_percentiles(families=0)
if __name__=='__main__':unittest.main()
