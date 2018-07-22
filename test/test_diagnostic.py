from amsdt.diagnostic import Diagnostic



if __name__=='__main__':
    diag = Diagnostic()
    diagnostic.apply_diagnostic()

    # on teste
    for spec in [[], ['serial_correlation'], ['heteroscedasticity'], ['specification'], ['unit_root'], ['heteroscedasticity','serial_correlation'], ['heteroscedasticity','serial_correlation', 'specification'], ['specification', 'unit_root']]:
        y, X, beta, X_observed, X_observed_ur, y_ur, eps = gen_data(spec)
        model_result = generate_model_result(X_observed_ur, y_ur)
        print('==========\n%s : %s' % (spec, apply_diagnostic(model_result)))
