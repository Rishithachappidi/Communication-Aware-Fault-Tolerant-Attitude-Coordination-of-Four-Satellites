import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]));from supervisor import Evidence,REQUIRED,authorize,monitor
class HorizonAndUnits(unittest.TestCase):
 def e(self):return Evidence((1.,1.),{k:'declared' for k in REQUIRED},valid_until=100)
 def test_late_window_refused(self):
  r=authorize([2.]*144,.02,2.88,2.,1.,self.e(),now=11.34)
  self.assertEqual(r['permission'],'refuse');self.assertIn('probe exceeds remaining mission horizon',r['reasons'])
 def test_window_ending_at_horizon(self):self.assertEqual(authorize([2.]*144,.02,2.88,2.,1.,self.e(),now=11.12)['permission'],'conditional-probe')
 def test_invalid_horizon_fails_closed(self):
  e=self.e();e.horizon_samples='700';self.assertEqual(authorize([2.]*144,.02,2.88,2.,1.,e)['permission'],'refuse')
 def test_rate_units_refused(self):
  e=self.e();e.rate_unit='rad';self.assertEqual(authorize([2.]*144,.02,2.88,2.,1.,e)['permission'],'refuse')
 def test_nonfinite_bound_stops_monitor(self):self.assertEqual(monitor(2.,float('nan'),.01)['event'],'invalid-bound')
if __name__=='__main__':unittest.main()
