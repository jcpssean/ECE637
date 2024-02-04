from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm

def equalizer(X):
    Z = np.zeros(np.shape(X))
    F_hat = np.zeros(256)
    
    h = np.histogram(X.flatten(), bins=np.linspace(0, 255, 256))
    
    for i in range(0, 256):
        F_hat[i] = np.sum(h[0][0:i+1]/np.sum(h[0]))
    
    Ymax = np.max(F_hat)
    Ymin = np.min(F_hat)
    
    for i in range(np.shape(X)[0]):
        for j in range(np.shape(X)[1]):
            Z[i, j] = 255 * ((F_hat[X[i, j]] - Ymin) / (Ymax - Ymin))
            
    return Z, F_hat

gray = cm.get_cmap('gray', 256)
im = Image.open('kids.tif')
x = np.array(im)

Z, F_hat = equalizer(x)

plt.plot(np.linspace(0,255,256), F_hat)
plt.title('F_hat of kids.tif')
plt.xlabel('pixel value')
plt.ylabel('F_hat')
plt.xlim(0, 260)
plt.show()

plt.hist(Z.flatten(),bins=np.linspace(0,255,256))
plt.title('Histogram of equalized kids.tif')
plt.xlabel('pixel value')
plt.ylabel('number of pixels')
plt.xlim(0, 260)
plt.show()

plt.imshow(Z, cmap=gray)
plt.show()