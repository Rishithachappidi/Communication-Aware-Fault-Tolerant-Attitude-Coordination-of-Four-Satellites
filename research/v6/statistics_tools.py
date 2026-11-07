"""Two-sided Bonferroni percentile locations; bootstrap validity remains approximate."""
def family_percentiles(alpha=.05,families=1):
 if not (0<alpha<1) or not isinstance(families,int) or families<1:raise ValueError('Invalid alpha or family count')
 tail=alpha/(2*families)
 return tail,1-tail
