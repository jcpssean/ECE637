import sys
sys.path.append('../')

from training_data.read_data import read_data
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

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
# plt.show()

Y = np.dot(U[:, 0:10].T, X)
x = [i for i in range(1, 11)]
plt.plot(x, Y[0:10, 0])
plt.plot(x, Y[0:10, 1])
plt.plot(x, Y[0:10, 2])
plt.plot(x, Y[0:10, 3])
plt.legend(["a", "b", "c", "d"])
# plt.show()

m = [1, 5, 10, 15, 20, 30]
fig, axs = plt.subplots(3, 2)
for i in range(6):
    Y = np.dot(U[:, 0:m[i]].T, X)
    X_hat = np.dot(U[:, 0:m[i]], Y)
    axs[i//2, i%2].imshow(X_hat[:, 0].reshape((64, 64)), cmap=plt.cm.gray, interpolation='none')
    axs[i//2, i%2].set_title(f"m = {m[i]}")
# plt.show()
    

A = U[:, 0:10]
Y = np.dot(A[:, 0:10].T, X)
Ck = Y.shape[1] // 26

params = []
for i in range(26):
    temp_mu = 0
    for j in range(Ck):
        temp_mu += Y[:, i + 26*j]
    mu_k = temp_mu/Ck
    params.append({'mean': mu_k})

for i in range(26):
    temp_R = 0
    for j in range(Ck):
        Yi = Y[:, i+26*j].reshape(10, 1)
        mu_k = params[i]['mean'].reshape(10, 1)
        temp_R += np.dot((Yi - mu_k), (Yi - mu_k).T)
    R_k = temp_R/(Ck-1)
    params[i]['cov'] = R_k
# print(params[0])



datadir='../test_data'    # directory where the data files reside
dataset=['veranda']
datachar='abcdefghijklmnopqrstuvwxyz'
Rows=64    # all images are 64x64
Cols=64
n=len(dataset)*len(datachar)  # total number of images
p=Rows*Cols   # number of pixels

X_test=np.zeros((p,n))  # images arranged in columns of X_test
k=0
for dset in dataset:
    for ch in datachar:
        fname='/'.join([datadir,dset,ch])+'.tif'
        im=Image.open(fname)
        img = np.array(im)
        X_test[:,k]=np.reshape(img,(1,p))
        k+=1

for n in range(X_test.shape[1]):
    X_test[:, n] -= mu
Y_test = np.dot(A.T, X_test)


error = []
############## Rk ##################
# for i in range(Y_test.shape[1]):
#     err = []
#     for cl in range(len(params)):
#         R_k = params[cl]['cov']
#         temp = Y_test[:, i] - params[cl]['mean']
#         temp1 = np.linalg.inv(R_k)
#         temp2 = np.log(np.linalg.det(R_k))
#         err.append(np.dot(temp.T, np.dot(temp1, temp)) + temp2)
#     predicted_class = datachar[np.argmin(err)]
#     if datachar[i] != predicted_class:
#         error.append([datachar[i], predicted_class])

############## Lambda_k ##################
# for i in range(Y_test.shape[1]):
#     err = []
#     for cl in range(len(params)):
#         Lambda_k = np.diag(np.diag(params[cl]['cov']))
#         temp = Y_test[:, i] - params[cl]['mean']
#         temp1 = np.linalg.inv(Lambda_k)
#         temp2 = np.log(np.linalg.det(Lambda_k))
#         err.append(np.dot(temp.T, np.dot(temp1, temp)) + temp2)
#     predicted_class = datachar[np.argmin(err)]
#     if datachar[i] != predicted_class:
#         error.append([datachar[i], predicted_class])

############## R_wc ##################
# for i in range(Y_test.shape[1]):
#     err = []
#     for cl in range(len(params)):
#         R_wc = 0
#         for j in range(26):
#             R_wc += params[j]['cov']
#         R_wc = R_wc/params[cl]['cov'].shape[0]
#         temp = Y_test[:, i] - params[cl]['mean']
#         temp1 = np.linalg.inv(R_wc)
#         temp2 = np.log(np.linalg.det(R_wc))
#         err.append(np.dot(temp.T, np.dot(temp1, temp)) + temp2)
#     predicted_class = datachar[np.argmin(err)]
#     if datachar[i] != predicted_class:
#         error.append([datachar[i], predicted_class])

############## Lambda ##################
# for i in range(Y_test.shape[1]):
#     err = []
#     for cl in range(len(params)):
#         R_wc = 0
#         for j in range(26):
#             R_wc += params[j]['cov']
#         Lambda = np.diag(np.diag(R_wc/params[cl]['cov'].shape[0]))
#         temp = Y_test[:, i] - params[cl]['mean']
#         temp1 = np.linalg.inv(Lambda)
#         temp2 = np.log(np.linalg.det(Lambda))
#         err.append(np.dot(temp.T, np.dot(temp1, temp)) + temp2)
#     predicted_class = datachar[np.argmin(err)]
#     if datachar[i] != predicted_class:
#         error.append([datachar[i], predicted_class])

############## Identity ##################
for i in range(Y_test.shape[1]):
    err = []
    for cl in range(len(params)):
        I = np.identity(params[cl]['cov'].shape[1])
        temp = Y_test[:, i] - params[cl]['mean']
        temp1 = np.linalg.inv(I)
        temp2 = np.log(np.linalg.det(I))
        err.append(np.dot(temp.T, np.dot(temp1, temp)) + temp2)
    predicted_class = datachar[np.argmin(err)]
    if datachar[i] != predicted_class:
        error.append([datachar[i], predicted_class])

print('Wrong classifications: ', error)