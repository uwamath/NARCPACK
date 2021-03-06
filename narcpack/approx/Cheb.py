import numpy as np

class Cheb:
    """Very simple polynomial class

    This is an extremely simple Chebyshev polynomial class for use in approximation classes.
    """

    def __init__(self, f, interval=[-1,1], n=10):
        """
        Parameters
        ----------
        f : scalar valued function or coefficients for basis
        interval : array_like, optional
               Left and right endpoints of interval over which to approximate f.
               f is approximated over interval[0] <= x <= interval[1]
        n : integer
            degree of approximation
        """

        self.interval = interval
        a,b = interval
        
        # check if f is a callable function or list
        if callable(f):
            
            x = (np.arange(n+1)+0.5)*np.pi/(n+1)
            
            T = np.cos(np.outer(np.arange(n+1),x))
            
            c = (2/(n+1))*T@f(np.cos(x)*(b-a)/2+(b+a)/2) # could implement as DCT instead of matrix multiply
            c[0] /= 2
            
            self.coeffs = c
            self.n = n
            
        elif isinstance(f, (list, tuple, np.ndarray)):
            self.coeffs = np.array(f)
            self.n = len(self.coeffs)

        else:
            raise ValueError("Cheb class must be initialized on scalar function or list like object")
        
        # need j=j because of python 'late binding closures'
        self.basis = [(lambda x, j=j: np.cos(j*np.arccos(2*(x-a)/(b-a)-1))) for j in range(n)]
        
    def __add__(self, other):
        """Override the + operator"""
        return Cheb(self.coeffs+other.coeffs)

    def __sub__(self, other):
        """Override the - operator"""
        return Cheb(self.coeffs-other.coeffs)

    def __call__(self, x):
        """
        A function to evaluate the polynomial at given point or points x.
        
        Notes
        -----
        There are better algorithms for evaluating Chebyshev polynomials
        """
        
        # check that evaluation point(s) are in the correct interval
        assert np.all( (self.interval[0] <= x) * (x <= self.interval[1]) ), f"x must be in the interval {self.interval}"

        a = 0.0
        for j in range(self.n):
            a += self.coeffs[j]*self.basis[j](x)
        return(a)

    def deriv(self):
        """A function to return the derivative"""
        
        a,b = self.interval

        c = self.coeffs
        c_ = np.zeros(self.n)
        
        # update coefficients
        for j in range(self.n-3,-1,-1):
            c_[j] = c_[j+2]+2*(j+1)*c[j+1]
        
        # normalize based on interval width
        c_ *= 2/(b-a)
        
        return Cheb(c_,interval=self.interval,n=self.n)
