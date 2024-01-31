import numpy as np                 # Numpy is a library support computation of large, multi-dimensional arrays and matrices.
from PIL import Image              # Python Imaging Library (abbreviated as PIL) is a free and open-source additional library for the Python programming language that adds support for opening, manipulating, and saving many different image file formats.
import matplotlib.pyplot as plt    # Matplotlib is a plotting library for the Python programming language.
from SpecAnal import BetterSpecAnal


x = np.random.uniform(-0.5, 0.5, [512, 512])
x_scaled = 255 * (x + 0.5)
plt.imshow(x_scaled.astype(np.uint8), cmap=plt.cm.gray)
plt.show()


y = np.zeros([512, 512])

for i in range(512):
    for j in range(512):
        y[i][j] = 3 * x[i][j]
        if (i-1 >= 0):
            y[i][j] += 0.99 * y[i-1][j]
        if (j-1 >= 0):
            y[i][j] += 0.99 * y[i][j-1]
        if (i-1 >= 0 and j-1 >= 0):
            y[i][j] += -0.9801 * y[i-1][j-1]



plt.imshow(y+127, cmap=plt.cm.gray)
plt.show()

# Section 3
# Plot the result using a 3-D mesh plot and label the x and y axises properly. 
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
a = b = np.linspace(-np.pi, np.pi, num = 64)
X, Y = np.meshgrid(a, b)

S_y = (1/12) * abs(3/((1-0.99*np.exp(-1j*X))*(1-0.99*np.exp(-1j*Y))))**2
surf = ax.plot_surface(X, Y, np.log(S_y), cmap=plt.cm.coolwarm)

ax.set_xlabel('$\mu$ axis')
ax.set_ylabel('$\\nu$ axis')
ax.set_zlabel('Z Label')

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()

# Section 4
# Plot the result using a 3-D mesh plot and label the x and y axises properly. 
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
a = b = np.linspace(-np.pi, np.pi, num = 64)
X, Y = np.meshgrid(a, b)

surf = ax.plot_surface(X, Y, np.log(BetterSpecAnal(y)), cmap=plt.cm.coolwarm)

ax.set_xlabel('$\mu$ axis')
ax.set_ylabel('$\\nu$ axis')
ax.set_zlabel('Z Label')

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()