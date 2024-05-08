import numpy as np
from scipy.special import erf
import matplotlib.pyplot as plt
plt.rc('axes.spines', **{'bottom':True, 'left':True, 'right':False, 'top':False})


# Create a range of points
x = np.linspace(0, 1, 30)
y = np.zeros_like(x) + 0.15

# smoothed sign of x
alpha = (x - x.min()) / (x.max() - x.min())
starting_u = 1
starting_v = 2
ending_u = -2
ending_v = 1
# Evaluate the vector field
u = starting_u * alpha + (1 - alpha) * ending_u
v = starting_v * alpha + (1 - alpha) * ending_v

u = u / (np.sqrt(u ** 2 + v ** 2))  # Normalize the arrows
v = v / (np.sqrt(u ** 2 + v ** 2))

# Plotting the arrows
plt.figure(figsize=(10, 2))
ax = plt.gca()
ax.quiver(x, y, u, v, scale=20, pivot='tail', color='black', width=0.004, headwidth=4, headlength=6, headaxislength=4)
ax.set_xlim(0, 1)
ax.set_ylim(-0.2, 0.5)
for spine in ['left', 'top', 'right', 'bottom']:
    ax.spines[spine].set_visible(False)

plt.xticks([])
plt.yticks([])

plt.annotate('', xy=(1, 0), xytext=(0, 0),
             arrowprops=dict(facecolor='black', arrowstyle='->', linewidth=2))

# Label the x-axis
plt.text(1, -0.1, 'Time', ha='right', va='center', fontsize=14)
plt.savefig('arrows.png', dpi=300, bbox_inches='tight')
