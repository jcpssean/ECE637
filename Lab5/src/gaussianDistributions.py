import numpy as np
import matplotlib.pyplot as plt

Rx = np.array([[2, -1.2], [-1.2, 1]])
W = np.random.normal(0, 1, (2, 1000))
eval, evec = np.linalg.eig(Rx)

X_tilde = np.dot(np.sqrt(np.diag(eval)), W)
X = np.dot(evec, X_tilde)

# plt.figure()
# plt.scatter(W[0, :], W[1, :], marker='.')
# plt.axis('equal')
# plt.show()

# plt.figure()
# plt.scatter(X_tilde[0, :], X_tilde[1, :], marker='.')
# plt.axis('equal')
# plt.show()

# plt.figure()
# plt.scatter(X[0, :], X[1, :], marker='.')
# plt.axis('equal')
# plt.show()

n=1000
mu_hat = np.mean(X, axis=1).reshape((2, 1))
print(mu_hat)
R_hat = 1/(n-1) * np.dot((X-mu_hat), ((X-mu_hat)).T)
print(R_hat)

eval1, evec1 = np.linalg.eig(R_hat)

X_tilde1 = np.dot(evec1.T, X)
W1 = np.dot(np.diag(1/np.sqrt(eval1)), X_tilde1)

mu = np.mean(W1, axis=1).reshape((2, 1))
print(mu)
Rw_hat = 1/(n-1) * np.dot((W-mu), ((W-mu)).T)
print(Rw_hat)

# plt.figure()
# plt.scatter(X_tilde1[0, :], X_tilde1[1, :], marker='.')
# plt.axis('equal')
# plt.show()

# plt.figure()
# plt.scatter(W1[0, :], W1[1, :], marker='.')
# plt.axis('equal')
# plt.show()
