from PIL import Image
import numpy as np
from scipy.signal import convolve2d


def rmse(f, b):
    f = f.astype(float)
    b = b.astype(float)

    rows, cols = np.shape(f)
    sum = 0
    for i in range(rows):
        for j in range(cols):
            sum += (f[i,j] - b[i,j])**2
        
    return np.sqrt((1/(rows*cols)) * sum)


def fidelity(f, b):
    gamma = 2.2
    f_l = 255 * ((f/255) ** gamma)
    b_l = 255 * ((b/255) ** gamma)
    
    # define h    
    var = 2
    size = 7
    h = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            h[i,j] = np.exp(-((i-3)**2 + (j-3)**2) / (2*var))

    C = 1/np.sum(h)
    h = C*h

    # pass f and b through h
    filtered_f = convolve2d(f_l, h, mode='same', boundary='fill', fillvalue=0)
    filtered_b = convolve2d(b_l, h, mode='same', boundary='fill', fillvalue=0)

    filtered_f = 255 * (filtered_f/255) ** (1/3)
    filtered_b = 255 * (filtered_b/255) ** (1/3)

    fid = rmse(filtered_f, filtered_b)

    return fid


im = Image.open('house.tif')
f = np.array(im)

im = Image.open('error_diffused.tif')
b = np.array(im)
# img_out = Image.fromarray(bin_im.astype(np.uint8))
# img_out.save('house_binary.tif')
        
RMSE = rmse(f, b)
print("RMSE = ", RMSE)

fid = fidelity(f, b)
print("fidelity = ", fid)