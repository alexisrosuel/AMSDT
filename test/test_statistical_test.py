import numpy as np

from amsdt.utils import FakeData, RegressionResult
from amsdt.statistical_test import StatisticalTest
from amsdt.settings import library

def compute_failed(specifications=[]):
    data = FakeData(N=1000, p=3, specifications=specifications, noise_level=0.1)
    data.generate_data()
    data.generate_model()

    results = {}
    for spec_to_test in library:
        test = StatisticalTest(statistical_test_type=spec_to_test)
        nb_test_failed, pvalues = test.run_test(regression_result=data.estimated_model)
        results[spec_to_test] = (nb_test_failed, pvalues)
    return results

if __name__=='__main__':
    nb_test_failed = compute_failed()
    print(nb_test_failed)
    nb_test_failed = compute_failed(['heteroscedasticity'])
    print(nb_test_failed)
    nb_test_failed = compute_failed(['serial_correlation'])
    print(nb_test_failed)
    nb_test_failed = compute_failed(['polynomial'])
    print(nb_test_failed)
    nb_test_failed = compute_failed(['rien'])
    print(nb_test_failed)
