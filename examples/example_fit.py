import matplotlib.pyplot as plt
import numpy as np

from example_project import CurveFitter

rng = np.random.default_rng()

def squarefunc(x,a,b):
    return a + b * x**2

xvals = np.linspace(start=0.0, stop=10.0, num=100)
yvals = squarefunc(xvals, a=0.1, b = 2.0) + rng.normal(scale=10.0, size=xvals.shape)

fit1 = CurveFitter(xvals,yvals)

fit2 = CurveFitter(xvals,yvals,func=squarefunc, show=False)
_, ax = fit2.plot()
plt.show()