import numpy as np
import plotly.graph_objects as go
from scipy.optimize import differential_evolution

X = np.linspace(-5.12, 5.12, 500)
Y = np.linspace(-5.12, 5.12, 500)
X, Y = np.meshgrid(X, Y)

def rastrigin(p):
    xx = p[0]
    yy = p[1]
    z = (xx ** 2 - 10 * np.cos(2 * np.pi * xx)) + \
        (yy ** 2 - 10 * np.cos(2 * np.pi * yy)) + 20
    return z


Z = rastrigin((X, Y))

# find minimum
bounds = [(-5.12, 5.12), (-5.12, 5.12)]
result = differential_evolution(rastrigin, bounds)
print(result.x, result.fun)

fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])

# minimum : black dot
fig.add_trace(go.Scatter3d(x=[result.x[0]], y=[result.x[1]], z=[result.fun],
                           mode='markers', marker=dict(size=5, color='black')))

fig.update_layout(title='Rastrigin function', width=1000, height=1000)
fig.show()

