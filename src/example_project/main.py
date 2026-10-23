import inspect
from collections.abc import Callable
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import scipy
from numpy.typing import NDArray

print("This should always appear.")

def function():
    print("I am a function.")

def whocalled():
    import __main__
    callingscript = Path(__main__.__file__).resolve()
    if __name__ == "__main__":
        whodat = "myself"
    else:
        whodat = callingscript.name
    print(f"I was imported by {whodat}")
    print(f"I am located in {callingscript.parent}")
    print(f"My current working directory is {Path.cwd()}")

class CurveFitter:
    """
    An example of a class that can be used to fit data to a curve.

    Parameters
    ----------
    xvals : NDArray
        The x values to fit.
    yvals : NDArray
        The y values to fit.
    func : Callable, optional
        The function to fit. If None, then a simple linear function will be used.
        The first argument must be x, and the remaining arguments are the fit parameters.
    show : bool, default True
        If True, show a plot of the fit once it is done.
    """

    def __init__(self,xvals: NDArray,yvals: NDArray,func: Callable | None = None, show: bool = True):
        # We will use setters and getters, so we'll define local storage variables for our properties
        self._xvals = None
        self._yvals = None
        self._func = None
        self._popt = None
        self._perr = None
        self.xvals = xvals
        self.yvals = yvals
        self.func = func

        # Do a fit using the inputs and plot the result
        self.fit(show=show)

    def fit(self, show: bool = True):
        """
        Perform the fit and optionally show the results as a plot.
        """
        popt, pcov = scipy.optimize.curve_fit(self.func, self.xvals, self.yvals)
        self._popt = popt
        # The 1-sigma uncertainties of the parameters are the square roots of the diagonal of the covariance matrix
        self._perr = np.sqrt(np.diag(pcov))

        if show:
            fig, ax = self.plot()
            plt.show()

    def plot(self) -> tuple[plt.Figure, plt.Axes]:
        """
        Plot the data as a scatter plot and the fitted function as a line, with the fit parameters in the legend.

        Returns
        -------
        fig : Figure
            The matplotlib Figure containing the plot.
        ax : Axes
            The matplotlib Axes containing the plot.
        """
        if self.popt is None:
            raise RuntimeError("No fit has been done yet. Call fit() first.")

        # Build a label like "m = 2.01 ± 0.03" for each parameter
        param_labels = [
            f"{name} = {value:.3g} ± {err:.2g}"
            for name, value, err in zip(self.param_names, self.popt, self.perr)
        ]

        # Evaluate the fit on a fine grid so that nonlinear functions look smooth
        xfit = np.linspace(self.xvals.min(), self.xvals.max(), 200)
        yfit = self.func(xfit, *self.popt)

        fig, ax = plt.subplots()
        ax.scatter(self.xvals, self.yvals, label="Data")
        ax.plot(xfit, yfit, color="C1", label="Fit:\n" + "\n".join(param_labels))
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(f"Fit using {self.func.__name__}")
        ax.legend()
        return fig, ax

    @property
    def param_names(self) -> list[str]:
        """
        The names of the fit parameters, taken from the arguments of func (skipping the first one, which is x).
        """
        return list(inspect.signature(self.func).parameters)[1:]

    # popt and perr have getters but no setters, which makes them read-only to users of the class
    @property
    def popt(self) -> NDArray | None:
        """
        The best-fit parameter values, or None if no fit has been done.
        """
        return self._popt

    @property
    def perr(self) -> NDArray | None:
        """
        The 1-sigma uncertainties of the best-fit parameters, or None if no fit has been done.
        """
        return self._perr


    # use the staticmethod decorator for functions that don't use the "self" argument.
    @staticmethod
    def linearfunc(x: NDArray, m: float, b: float) -> NDArray:
        """
        Simple linear function: m * x + b
        """
        return m * x + b

    # This demonstrates how to implement a basic setters and getters model for data storage and verification.
    @property
    def xvals(self) -> NDArray:
        return self._xvals
    
    @xvals.setter
    def xvals(self, value):
        # Check to make sure that value can be cast into a numpy array
        try:
            value = np.array(value)
        except Exception as e:
            raise RuntimeError(f"Error converting input to array: {e}") from e
        
        if self.yvals is not None and value.shape != self.yvals.shape:
            raise ValueError(f"xval and yval shapes must match {value.shape} != {self.yvals.shape}")
        self._xvals = value


    @property
    def yvals(self) -> NDArray:
        return self._yvals

    @yvals.setter
    def yvals(self, value):
        # Check to make sure that value can be cast into a numpy array
        try:
            value = np.array(value)
        except Exception as e:
            raise RuntimeError(f"Error converting input to array: {e}") from e
        
        if self.xvals is not None and value.shape != self.xvals.shape:
            raise ValueError(f"xval and yval shapes must match {value.shape} != {self.xvals.shape}")
        self._yvals = value


    @property
    def func(self) -> Callable:
        return self._func
    
    @func.setter
    def func(self, value):
        if value is None: # This will set the default function to the linear one
            value = self.linearfunc
        elif not callable(value):
            raise TypeError("func must be callable")
        self._func = value





if __name__ == "__main__":
    print("This won't appear when I'm imported.")
    function()
    whocalled()