import statsmodels.stats.diagnostic
import pysal.spreg.diagnostics
from statsmodels.stats.outliers_influence import reset_ramsey
import arch.unitroot
import numpy as np

from amsdt.settings import library

class StatisticalTest:
    def __init__(self, statistical_test_type):
        '''
        :param test_type: the specification we want to test (heteroscedasticity, serial correlation, etc.)
        :type test_type: str
        :param regression_result: OLS fitted
        :type regression_result: RegressionResult
        '''

        self.statistical_test_type = statistical_test_type
        #self.regression_result = regression_result

    def run_test(self, regression_result):
        '''

        '''
        tests_to_run = library[self.statistical_test_type]['test']
        pvalues = {}
        pvalue = -1

        for test in tests_to_run:

            # heteroscedasticity
            if test == 'Goldfeld Quandt':
                result = statsmodels.stats.diagnostic.het_goldfeldquandt(regression_result.resid, regression_result.model.exog)
                pvalue = result[1]
            elif test == 'Breusch Pagan':
                result = statsmodels.stats.diagnostic.het_breuschpagan(resid=regression_result.resid, exog_het=regression_result.model.exog)
                pvalue = result[1]
            #elif test == 'White':
            #    result = pysal.spreg.diagnostics.white(reg=regression_result)
            #    pval = result[1]

            # serial correlation
            if test == 'Breusch Godfrey':
                result = statsmodels.stats.diagnostic.acorr_breusch_godfrey(results=regression_result, nlags=None)
                pvalue = result[1]
            elif test == 'Ljung Box':
                # 1 pvalue per lag tested
                result = statsmodels.stats.diagnostic.acorr_ljungbox(x=regression_result.resid, lags=[1,2])
                pvalue = np.min(result[1])

            # non linearity
            if test == 'Ramsey RESET':
                result = reset_ramsey(res=regression_result, degree=2)
                pvalue = np.asscalar(result.pvalue)
            elif test == 'Harvey Collier':
                result = statsmodels.stats.diagnostic.linear_harvey_collier(regression_result)
                pvalue = result[1]
            elif test == 'Rainbow':
                result = statsmodels.stats.diagnostic.linear_rainbow(regression_result)
                pvalue = result[1]

            # structural change
            if test == 'CUSUM':
                result = statsmodels.sandbox.stats.diagnostic.breaks_cusumolsresid(regression_result.resid)
                #print(result)

                pvalue = result[1]
            #elif test == 'Hansen':
            #    result = statsmodels.sandbox.stats.diagnostic.breaks_hansen(olsresults=regression_result)
            #    H, crit95, ft, s = result[1]
            #    print(H)
            #    pvalue = 0.05 if H > crit95 else 1
            elif test == 'recursive':
                result = statsmodels.stats.diagnostic.recursive_olsresiduals(olsresults=regression_result)
                cusum, cusum_ci = result[5], result[6]
                #import matplotlib.pyplot as plt
                #plt.plot(cusum)
                #plt.plot(cusum_ci[0])
                #plt.plot(cusum_ci[1])
                #plt.figure()
                #print(cusum_ci)
                thresholds = np.sum((cusum[1:]>cusum_ci[1])|(cusum[1:]<cusum_ci[0]).astype(int))
                #print(thresholds)
                pvalue = 0.05 if thresholds > 0 else 1

            # unit root
            if test == 'Augmented Dickey Fuller':
                pvalue = []
                result = arch.unitroot.ADF(y=regression_result.model.endog, max_lags=3, trend='ct')
                pvalue.append(-result.pvalue+0.1) # H0 est il y a une racine unitaire
                for i in range(regression_result.model.exog.shape[1]):
                    result = arch.unitroot.ADF(y=regression_result.model.exog[:,i], max_lags=3, trend='ct')
                    pvalue.append(-result.pvalue+0.1) # H0 est il y a une racine unitaire
                pvalue = min(pvalue)
            elif test == 'Dickey Fuller GLS':
                pvalue = []
                result = arch.unitroot.DFGLS(y=regression_result.model.endog, max_lags=3, trend='ct')
                pvalue.append(-result.pvalue+0.1) # H0 est il y a une racine unitaire
                for i in range(regression_result.model.exog.shape[1]):
                    result = arch.unitroot.DFGLS(y=regression_result.model.exog[:,i], max_lags=3, trend='ct')
                    pvalue.append(-result.pvalue+0.1) # H0 est il y a une racine unitaire
                pvalue = min(pvalue)
            elif test == 'Phillips Perron':
                pvalue = []
                result = arch.unitroot.PhillipsPerron(y=regression_result.model.endog, trend='ct')
                pvalue.append(-result.pvalue+0.1) # H0 est il y a une racine unitaire
                for i in range(regression_result.model.exog.shape[1]):
                    result = arch.unitroot.PhillipsPerron(y=regression_result.model.exog[:,i], trend='ct')
                    pvalue.append(-result.pvalue+0.1) # H0 est il y a une racine unitaire
                pvalue = min(pvalue)
            elif test == 'KPSS':
                pvalue = []
                result = arch.unitroot.KPSS(y=regression_result.model.endog, trend='ct')
                pvalue.append(result.pvalue) # H0 est il y a une racine unitaire
                for i in range(regression_result.model.exog.shape[1]):
                    result = arch.unitroot.KPSS(y=regression_result.model.exog[:,i], trend='ct')
                    pvalue.append(result.pvalue) # H0 est il y a une racine unitaire
                pvalue = min(pvalue)
            elif test == 'Variance Ratio':
                pvalue = []
                result = arch.unitroot.VarianceRatio(y=regression_result.model.endog, trend='c')
                pvalue.append(-result.pvalue+0.1) # H0 est il y a une racine unitaire
                for i in range(regression_result.model.exog.shape[1]):
                    result = arch.unitroot.VarianceRatio(y=regression_result.model.exog[:,i], trend='c')
                    pvalue.append(-result.pvalue+0.1) # H0 est il y a une racine unitaire
                pvalue = min(pvalue)


            # spatial correlation
            # if test == 'Lagrange Multiplier':
            #     result = pysal.spreg.diagnostics_sp.LMtests(ols=regression_result, w=w)
            #     print(result)
            # elif test == 'Moran':
            #     result = pysal.spreg.diagnostics_sp.MoranRes(ols=regression_result, w=w, z=False)
            #     print(result)

            pvalues[test] = pvalue

        nb_test_failed = sum([1 if pvalues[test] < 0.05 else 0 for test in pvalues])
        return nb_test_failed, pvalues
