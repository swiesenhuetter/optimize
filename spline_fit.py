import numpy as np
from scipy.interpolate import splrep, splev, CubicSpline
import matplotlib.pyplot as plt


x = np.arange(0, 10*np.pi, 1.5)
y = np.sin(x)
y[-1] = y[0]  # to make the curve close
x[-1] = 10.0*np.pi  # to make the curve close
cs = CubicSpline(x, y, bc_type='periodic')
spl = splrep(x, y, per=True, k=3)

xs = np.arange(-1, 50, 0.1)

fig, ax = plt.subplots(figsize=(6.5, 4))

ax.plot(x, y, 'o', label='data')

ax.plot(xs, np.sin(xs), label='sin', linestyle='--', alpha=0.5)
ax.plot(xs, cs(xs), label='spline')
ax.plot(xs, splev(xs, spl), label='spline 2')


ax.set_xlim(-1, 50)
ax.legend(loc='lower left', ncol=2)
plt.show()
