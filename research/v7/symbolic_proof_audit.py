"""Exact algebra checks for a written proof; not a full formal proof assistant."""
from pathlib import Path
import json
import sympy as s
OUT=Path(__file__).resolve().parent/'results';c1,c2,u1,u2,d1,d2,v1,v2=s.symbols('c1 c2 u1 u2 d1 d2 v1 v2',real=True);R,r,A,B=s.symbols('R r A B',nonnegative=True)
c=s.Matrix([c1,c2]);u=s.Matrix([u1,u2]);d=s.Matrix([d1,d2]);v=s.Matrix([v1,v2]);e=c+u;x=d+v
loss=2*e.dot(x)+x.dot(x);D=2*c.dot(d)+2*R*A+d.dot(d)+2*(B+R)*r+r*r
slack=2*(R*A-u.dot(d))+2*(r*B-(c+d).dot(v))+2*(R*r-u.dot(v))+(r*r-v.dot(v))
assert s.expand(D-loss-slack)==0
# The familiar Cauchy inequality used in each nonnegative bracket is certified
# algebraically by the 2D Gram determinant identity, plus sign/square-root order.
a1,a2,b1,b2=s.symbols('a1 a2 b1 b2',real=True)
assert s.expand((a1*a1+a2*a2)*(b1*b1+b2*b2)-(a1*b1+a2*b2)**2-(a1*b2-a2*b1)**2)==0
Ap=s.symbols('Ap',positive=True);uc=R*d/Ap;vc=r*d/Ap
sharp=2*uc.dot(d+vc)+(d+vc).dot(d+vc)
sharp_num=s.factor((sharp-(2*R*(Ap+r)+(Ap+r)**2))*Ap**2)
# Reducing the exact relation d'd=Ap² proves attainment when d is nonzero.
rem=s.rem(sharp_num,s.Poly(d1*d1+d2*d2-Ap*Ap,d1),d1);assert s.simplify(rem)==0
u0=s.Matrix([R,0]);v0=s.Matrix([r,0]);assert s.expand(2*u0.dot(v0)+v0.dot(v0)-(2*R*r+r*r))==0
um=s.Rational(1,10**6);alpha,Dum=s.symbols('alpha Dum',positive=True);assert s.simplify((Dum*um**2)/(alpha*um)**2-Dum/alpha**2)==0
report={'status':'passed','exact_identities':['general-bound nonnegative slack decomposition','two-dimensional Cauchy Gram determinant','centered-bound attainment for nonzero increment','zero-increment centered attainment including zero radii','exact radian/microradian exponent conversion'],'assumptions_used_in_written_proof':['A=norm(dbar), B=norm(c+dbar)','norm(u)<=R, norm(v)<=r, R,r>=0','Cauchy inequality and order of nonnegative square roots','fixed offset/divergence, positive power, lower gain slope and lower starting power for optical conversion'],'scope':'Machine-checked exact algebra identities plus a line-by-line mathematical argument. Not an external human verification, not a complete Lean/Coq theorem, not rounded floating-point certification.'}
(OUT/'symbolic_proof.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
