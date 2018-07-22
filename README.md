# AMSDT
Automated Model Specification and Diagnostic Test

2 objectives:
- Apply automatically a large variety of specification and diagnostic tests
- Find the best specification for a regression task (the model which minimize the number of failed tests)

- jeu de données
- variable cible  
- variables explicatives

objectif : trouver la meilleur spécification possible
- homoscedasticité (Goldfeld - Quandt, Breusch Pagan, White)
- données entrée et sortie stationnaire (Dickey Fuller, ADF, KPSS, Philips Perron)
- pas d'endogénéité (Haussman) -> il faut au moins 1 variable instrumentale
- pas d'autocorrélation (Durbin Watson, Breusch Godfrey)
- tous les tests de spécifications passent (Ramsey RESET)
- pas trop de multicolinéarité
- pas de dépendance spatiales dans les résidus
- pas de rupture structurelle (Chow, CUSUM)
- pas d'individualité dans les résidus
- pas d'autoséléction (heckman two step model)
- instruments sains (Sargan–Hansen)
- outliers


algorithmes de résolutions possibles:
- serial correlation : Cochran-Orcutt, Prais-Winsten
- variables instrumentales : 2SLS
- simultanée : 2SLS
- autoséléction : heckman two step model, tobit
- effets individuels dans les résidus : fixed effects
- détéction automatique des instruments possible : Sargan-Hansen


retour:
- spécification
- transformations appliquées (stationnarisation en particulier)
- estimation des coefficients
- covariance des coefficients
- sommaire de tous les tests


packages :
- spécification test : statsmodels
- spatial : pysal
- linear models : linearmodels
- arch : test de stationnarité


critères d'optimisation / d'arrêt:
- minimiser les diagnostics qui failent --> on reste sur ça
- maximiser le fit : vraisemblance / r2 / SCR
"On veut trouver un modèle sain et identifier où se trouve l'information pure"
