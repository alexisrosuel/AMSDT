# dict of the potential issues : {issue: {test: [test1, test2, ...], solution: [solution1, solution2, ...]}}
library = {
'heteroscedasticity': {'test': ['Breusch Pagan', 'White'], 'solution': ['FGLS_heteroscedasticity']},
'serial_correlation': {'test': ['Breusch Godfrey', 'Ljung Box'], 'solution': ['Cochran Orcutt', 'Prais Winsten']},
'polynomial': {'test': ['Ramsey RESET', 'Harvey Collier', 'Rainbow'], 'solution': ['polynomial']},
'structural_change': {'test': ['CUSUM', 'recursive'], 'solution': ['split']},
'unit_root': {'test': ['Augmented Dickey Fuller', 'Dickey Fuller GLS', 'KPSS', 'Phillips Perron', 'Variance Ratio'], 'solution': ['differentiate']},
'spatial': {'test': ['Lagrange Multiplier', 'Moran'], 'solution': ['SAC', 'SLX', 'SEM']}
}

# a rajouter plus tard
# serial : Box-Pierce, Durbin Watson
# heterosc : Goldfeld Quandt
# struc change : Hansen, Chow
