from amsdt.settings import library

# nos données bonnes
import numpy as np
from numpy.linalg import inv
from scipy.stats import multivariate_normal, norm

class FakeData:
    def __init__(self, N=1000, p=3, specifications=[], noise_level=0.1):
        '''
        Generate fake data and model (OLS) with some required specifications.
        '''
        self.available_specifications = [specification for specification in library]
        self.N = N
        self.p = p
        self.specifications = specifications
        self.noise_level = noise_level
        self.rho = 0.4

        # Handle the most simple OLS model, useful to test our hypothesis
        self.estimated_model = None

        # The dataset which will be built
        self.y = None
        self.X = None
        self.X_observed = None
        self.eps = None
        self.beta = None

        if not self.check_specification():
            raise ValueError('specification should be in %s, got %s' % (','.join(self.available_specifications), self.specifications))

    def check_specification(self):
        """
        Check if all the specifications spent are within the available one
        :rtype: bool
        """
        for specification in self.specifications:
            if specification not in self.available_specifications:
                return False
        return True

    def generate_data(self):
        """
        Generate a dataset (X,y) following the required specifications
        """
        X = multivariate_normal(mean=np.zeros(self.p),
                                cov=np.identity(self.p)
                                ).rvs(self.N)
        X_observed = X.copy()
        eps = norm(loc=0, scale=self.noise_level).rvs(self.N)

        if 'heteroscedasticity' in self.specifications:
            # sigma_eps_i ~ Normal(0, exp(X0_i + X1_i + ...) )
            X_sum = np.sum(X, axis=1)
            eps *= np.sqrt(np.exp(X_sum))

        if 'serial_correlation' in self.specifications:
            for i in range(1, self.N):
                eps[i] += self.rho*eps[i-1]

        if 'polynomial' in self.specifications:
            X = np.hstack([X, X**2])
            self.p *= 2

        beta = norm(loc=0, scale=1).rvs(self.p)
        y = X @ beta + eps

        # X_observed_ur = X_observed
        # y_ur = y
        # if 'unit_root' in specification:
        #     y_ur = [0]
        #     X_observed_ur = [[0 for i in range(p)]]
        #     for i in range(1, N):
        #         y_ur.append(y_ur[-1]+y[i-1])
        #         X_observed_ur.append(X_observed_ur[-1]+X[i-1])
        #     X_observed_ur = np.array(X_observed_ur)
        #     y_ur = np.array(y_ur)

        #if 'structural_change' in specification:
        #    # at half time, we change the model (new_beta = beta/2)
        #    half = int(y.shape[0]/2)
        #    new_beta = -beta #norm(loc=0, scale=1).rvs(p)
        #    y[half:] = X[half:,:] @ new_beta + eps[half:]

        # store all the data within the class
        self.y = y
        self.X = X
        self.X_observed = X_observed
        self.eps = eps
        self.beta = beta

    def generate_model(self):
        """
        Fill the self.estimated_model attribute with a class, similar to the OLSResuts of the statsmodels package,
        and others (pysal, linearmodels, arch), for multi compatibility
        """
        beta_ols = inv(self.X_observed.T @ self.X_observed) @ self.X_observed.T @ self.y
        residuals_ols = self.y - self.X_observed @ beta_ols
        self.estimated_model = RegressionResult(y=self.y, X=self.X_observed, beta=beta_ols, resid=residuals_ols)

class RegressionResult:
    def __init__(self, y, X, beta, resid):
        """
        Class to handle diagnostic test from multiple package (pysal, linearmodels, arch) simultanly
        """
        self.model = Model(exog=X, endog=y)

        self.nobs = X.shape[0]
        self.n = X.shape[0]

        self.dof_model = X.shape[1]
        self.k = X.shape[1]

        self.dof_resid = X.shape[0] - self.dof_model

        self.beta = beta
        self.y = y
        self.fittedvalues = y
        self.mean_y = y.mean()
        self.x = X
        self.xtx = X.T @ X

        self.resid = resid
        self.u = resid
        self.utu = [resid.T @ resid]
        self.ssr = np.sum(self.resid**2)


class Model:
    def __init__(self, exog, endog):
        self.exog = exog
        self.endog = endog
