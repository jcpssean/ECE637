from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm

def stretch(X, T1, T2):
    output = np.zeros(np.shape(X))
    
    for i in range(np.shape(X)[0]):
        for j in range(np.shape(X)[1]):
            if X[i, j] <= T1:
                output[i, j] = 0
            elif X[i, j] >= T2:
                output[i, j] = 255
            else:
                output[i, j] = (255 / (T2-T1)) * (X[i, j] - T1)
                
    return output

gray = cm.get_cmap('gray', 256)
im = Image.open('kids.tif')
x = np.array(im)

output = stretch(x, 75, 177)

plt.hist(output.flatten(),bins=np.linspace(0,255,256))
plt.title('Histogram of stretched kids.tif')
plt.xlabel('pixel value')
plt.ylabel('number of pixels')
plt.xlim(0, 260)
plt.show()

plt.imshow(output, cmap=gray)
plt.show()