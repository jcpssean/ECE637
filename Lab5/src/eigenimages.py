import sys
sys.path.append('../')

from training_data.read_data import read_data
import numpy as np
import matplotlib.pyplot as plt

X = read_data()
mu = np.mean(X, axis=1)

for n in range(X.shape[1]):
    X[:, n] -= mu


Z = (1 / np.sqrt(312-1)) * X
U, S, V = np.linalg.svd(Z)
eigvecs = U
eigvals = S**2

fig, axs = plt.subplots(3, 4)
for k in range(12):
    img = np.reshape(eigvecs[:, k], (64, 64))

    axs[k//4,k%4].imshow(img, cmap=plt.cm.gray, interpolation='none') 
plt.show()

Y = np.dot(U[:, 0:10].T, X)
x = [i for i in range(1, 11)]
plt.plot(x, Y[0:10, 0])
plt.plot(x, Y[0:10, 1])
plt.plot(x, Y[0:10, 2])
plt.plot(x, Y[0:10, 3])
plt.legend(["a", "b", "c", "d"])
plt.show()

m = [1, 5, 10, 15, 20, 30]
fig, axs = plt.subplots(3, 2)
for i in range(6):
    Y = np.dot(U[:, 0:m[i]].T, X)
    X_hat = np.dot(U[:, 0:m[i]], Y)
    axs[i//2, i%2].imshow(X_hat[:, 0].reshape((64, 64)), cmap=plt.cm.gray, interpolation='none')
    axs[i//2, i%2].set_title(f"m = {m[i]}")
plt.show()