import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

y = np.array(Image.open('img14g.tif'))
x = np.array(Image.open('img14sp.tif'))

rows = np.arange(20, y.shape[0], 20)
cols = np.arange(20, y.shape[1], 20)
# print(rows, cols)

Z = np.zeros([len(rows)*len(cols), 7*7])
Y = np.zeros([len(rows)*len(cols), 1])

for i, row in enumerate(rows):
    for j, col in enumerate(cols):
        index = i * len(cols) + j
        Y[index] = y[row, col]
        Z[index] = x[row-3:row+4, col-3:col+4].flatten()

# print(Z.shape)
# print(Y.shape)

R_zz_hat = np.dot(Z.T, Z) / Y.shape[0]
r_zy_hat = np.dot(Z.T, Y) / Y.shape[0]
theta_star = np.dot(np.linalg.inv(R_zz_hat), r_zy_hat)

print(theta_star.reshape([7, 7]))

output = np.zeros(x.shape)
for row in range(x.shape[0]):
    for col in range(x.shape[1]):
        if row < 3 or col < 3 or row > x.shape[0] - 4 or col > x.shape[1] - 4:
            output[row, col] = 0
            continue
        z_s = x[row-3:row+4, col-3:col+4].flatten()
        # print(z_s)
        # print(z_s.shape)
        # print(theta_star.shape)
        output[row, col] = z_s @ theta_star

# print(np.amax(result))
output = np.clip(output, 0, 255)

plt.plot()
plt.imshow(output, cmap='grey')
plt.show()