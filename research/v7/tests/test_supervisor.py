import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from supervisor import *
class SupervisorTest(unittest.TestCase):
 def evidence(self):return Evidence((1.,1.),{k:'synthetic-fixture-only' for k in REQUIRED},valid_until=10.)
 def call(self,e,**kw):return authorize([2.]*10,.02,.2,2.,1.,e,**kw)
 def test_missing_evidence_refused(self):self.assertEqual(self.call(None)['permission'],'refuse')
 def test_expired_window_refused(self):
  e=self.evidence();e.valid_until=.1;self.assertEqual(self.call(e)['permission'],'refuse')
 def test_no_parameter_interpolation(self):
  e=self.evidence();e.actuator_pair=(1.1,1.25);self.assertEqual(self.call(e)['permission'],'refuse')
 def test_unverified_contract_refused(self):
  e=self.evidence();e.references.pop('constant_offset_window');self.assertEqual(self.call(e)['permission'],'refuse')
 def test_units_required(self):
  e=self.evidence();e.angular_unit='urad';self.assertEqual(self.call(e)['permission'],'refuse')
 def test_simulation_not_deployment(self):self.assertEqual(self.call(self.evidence(),deployment='physical')['permission'],'refuse')
 def test_uncertain_power_does_not_unlock_acquisition(self):
  r=authorize([.9]*10,.02,.2,.99,1.,self.evidence());self.assertEqual(r['permission'],'refuse');self.assertEqual(r['mode'],'service-or-uncertain')
 def test_no_recovery_credit(self):
  r=self.call(self.evidence());self.assertEqual(r['permission'],'conditional-probe');self.assertFalse(r['recovery_authorized'])
 def test_breach_marks_uncertified(self):self.assertEqual(monitor(.9,1.)['event'],'bound-breach')
 def test_no_false_breach_from_uncertain_measurement(self):self.assertEqual(monitor(.99,1.,eta=.05)['event'],'no-observed-breach')
 def test_invalid_budget_cannot_fail_open(self):self.assertEqual(self.call(self.evidence(),service_budget=float('nan'))['permission'],'refuse')
 def test_invalid_expiry_refused(self):
  e=self.evidence();e.valid_until=float('nan');self.assertEqual(self.call(e)['permission'],'refuse')
 def test_envelope_must_cover_whole_probe(self):
  e=self.evidence();e.horizon_samples=1;self.assertEqual(self.call(e)['permission'],'refuse')
 def test_censored_or_invalid_interval_refused(self):
  e=self.evidence();e.relative_power_sigma=1.;self.assertEqual(self.call(e)['permission'],'refuse')
if __name__=='__main__':unittest.main()
