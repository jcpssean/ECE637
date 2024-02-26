import numpy as np
import matplotlib.pyplot as plt

# Load data.npy
data = np.load('data.npy', allow_pickle=True)[()]

x = data['x']
y = data['y']
z = data['z']
illum1 = data['illum1']
illum2 = data['illum2']
X = np.zeros((1, np.size(x)))
Y = np.zeros((1, np.size(y)))

wavelength = np.arange(400, 710, 10)

for i in range(np.size(x)):
    X[0, i] = x[0, i] / (x[0, i] + y[0, i] + z[0, i])
    Y[0, i] = y[0, i] / (x[0, i] + y[0, i] + z[0, i])

CIE_1931 = np.array([[0.73467, 0.26533, 0.0],
                     [0.27376, 0.71741, 0.00883], 
                     [0.16658, 0.00886, 0.82456]])

Rec_709 = np.array([[0.640, 0.330, 0.030],
                    [0.300, 0.600, 0.100],
                    [0.150, 0.060, 0.790]])

D65_white_point = np.array([0.3127, 0.3290, 0.3583])

EE_white_point = np.array([0.3333, 0.3333, 0.3333])


plt.plot(np.append(X, X[0]).flatten(), np.append(Y, Y[0]).flatten(), '-')
plt.plot(np.append(CIE_1931[:, 0], CIE_1931[0, 0]), np.append(CIE_1931[:, 1], CIE_1931[0, 1]), '-')
plt.plot(np.append(Rec_709[:, 0], Rec_709[0, 0]), np.append(Rec_709[:, 1], Rec_709[0, 1]), '-')
plt.plot(D65_white_point[0], D65_white_point[1], 'o')
plt.plot(EE_white_point[0], EE_white_point[1], 'x')

labels_cie = [r'$R_{CIE\_1931}$', r'$G_{CIE\_1931}$', r'$B_{CIE\_1931}$']
labels_709 = [r'$R_{709}$', r'$G_{709}$', r'$B_{709}$']

for i in range(3):
    plt.text(CIE_1931[i, 0], CIE_1931[i, 1], labels_cie[i])
    plt.text(Rec_709[i, 0], Rec_709[i, 1], labels_709[i])

plt.text(D65_white_point[0]-0.1, D65_white_point[1]-0.05, r'$D_{65}$ white point')
plt.text(EE_white_point[0], EE_white_point[1]+0.03, r'EE white point')

plt.show()