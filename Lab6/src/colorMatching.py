import numpy as np
import matplotlib.pyplot as plt

# Load data.npy
data = np.load('data.npy', allow_pickle=True)[()]

x = data['x']
y = data['y']
z = data['z']
illum1 = data['illum1']
illum2 = data['illum2']

wavelength = np.arange(400, 710, 10)
# plt.plot(wavelength, x.flatten())
# plt.plot(wavelength, y.flatten())
# plt.plot(wavelength, z.flatten())
# plt.legend([r'$x_0$', r'$y_0$', r'$z_0$'])
# plt.show()

A_inv = np.array([[0.2430, 0.8560, -0.0440], [-0.3910, 1.1650, 0.0870], [0.0100, -0.0080, 0.5630]])
temp = np.array([x.flatten(), y.flatten(), z.flatten()])
lms = np.dot(A_inv, temp)
l, m, s = lms[0, :], lms[1, :], lms[2, :]
# plt.plot(wavelength, l)
# plt.plot(wavelength, m)
# plt.plot(wavelength, s)
# plt.legend([r'$l_0$', r'$m_0$', r'$s_0$'])
# plt.show()

plt.plot(wavelength, illum1.flatten())
plt.plot(wavelength, illum2.flatten())
plt.legend([r'$D_{65}$', 'Fluorescent'])
plt.show()