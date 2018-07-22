from amsdt.settings import library
from amsdt.statistical_test import StatisticalTest

class Diagnostic:
    def __init__():
        '''
        Apply sequentially all the possible statistical diagnostic tests.

        Return descriptions :
        '''
        return


    def apply_diagnostic(model_result):
        '''
        Apply all our diagnostic to the model and residuals
        '''

        diagnostic = {specification: StatisticalTest(specification).test(model_result) for specification in library}
        return diagnostic
