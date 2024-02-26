import numpy as np
import matplotlib.pyplot as plt

# Load data.npy
data = np.load('data.npy', allow_pickle=True)[()]
reflect = np.load('reflect.npy', allow_pickle=True)[()]

x = data['x']
y = data['y']
z = data['z']
illum1 = data['illum1']
illum2 = data['illum2']
R = reflect['R']
I = np.zeros(R.shape)
xyz = np.array([x, y, z])

for i in range(R.shape[2]):
    I[:, :, i] = np.dot(R[:, :, i], illum2[0, i])


XYZ = np.zeros((R.shape[0], R.shape[1], 3))

for i in range(XYZ.shape[2]):
    # Iterate over the wavelengths
    for j in range(R.shape[2]):
        XYZ[:, :, i] += xyz[i][0, j] * I[:, :, j]

Rec_709 = np.array([[0.640, 0.330, 0.030],
                    [0.300, 0.600, 0.100],
                    [0.150, 0.060, 0.790]])

D65_white_point = np.array([0.3127, 0.3290, 0.3583])

temp = np.array([D65_white_point[0]/D65_white_point[1], 1, D65_white_point[2]/D65_white_point[1]])
scale_coeff = np.dot(np.linalg.inv(Rec_709.T), temp)
M = np.dot(Rec_709.T, np.diag(scale_coeff))
# print('M = ', M)

RGB = np.zeros(XYZ.shape)
# Take each pixel in XYZ array to RGB coordinates
for i in range(XYZ.shape[0]):
    for j in range(XYZ.shape[1]):
        RGB[i, j] += np.dot(np.linalg.inv(M), XYZ[i, j]).flatten()
        for k in range(XYZ.shape[2]):
            if RGB[i, j, k] > 1:
                RGB[i, j, k] = 1
            elif RGB[i, j, k] < 0:
                RGB[i, j, k] = 0

gamma = 2.2            
RGB = RGB**(1/gamma)

plt.figure()
plt.title('Fluorescent Light Source')
plt.imshow(RGB)
plt.show()
