from symfit import parameters, variables, sin, cos, Fit
import numpy as np
import matplotlib.pyplot as plt

plt.ion()

def fourier_series(x, f, n=0):
    """
    Returns a symbolic fourier series of order `n`.

    :param n: Order of the fourier series.
    :param x: Independent variable
    :param f: Frequency of the fourier series
    """
    # Make the parameter objects for all the terms
    a0, *cos_a = parameters(','.join(['a{}'.format(i) for i in range(0, n + 1)]))
    sin_b = parameters(','.join(['b{}'.format(i) for i in range(1, n + 1)]))
    # Construct the series
    series = a0 + sum(ai * cos(i * f * x) + bi * sin(i * f * x)
                     for i, (ai, bi) in enumerate(zip(cos_a, sin_b), start=1))
    return series

x, y = variables('x, y')
w, = parameters('w')
model_dict = {y: fourier_series(x, f=w, n=10)}
print(model_dict)

# Make step function data
xdata = np.linspace(0, 25, 25)
ydata = np.array([2.1,1.8,2.4,0.9,3.3,1.2,1.8,7.5,2.4,3.3,7.2,1.8,2.1,2.4,3.6,1.5,2.7,2.4,2.1,1.8,3.3,2.7,1.2,3.3,2.1])
print(xdata.shape)
print(ydata.shape)
# Define a Fit object for this model and data
fit = Fit(model_dict, x=xdata, y=ydata)
fit_result = fit.execute()
print(fit_result)

# Plot the result
plt.plot(xdata, ydata)
plt.plot(xdata, fit.model(x=xdata, **fit_result.params).y, color='green', ls=':')
plt.pause(1000)