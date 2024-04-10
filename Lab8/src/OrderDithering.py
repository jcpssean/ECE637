from PIL import Image
import numpy as np


def dither(img, I):
    T = 255*(I+0.5)/(I.shape[0]**2)
    dithered_img = np.zeros(img.shape)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i,j] > T[i % I.shape[0], j % I.shape[0]]:
                dithered_img[i,j] = 255
                
    return dithered_img


im = Image.open('house.tif')
input = np.array(im)

gamma = 2.2
f_l = 255 * ((input/255) ** gamma)

I2 = np.block([[1, 2], [3, 0]])
I4 = np.block([[4*I2 + 1, 4*I2 + 2], [4*I2 + 3, 4*I2]])
I8 = np.block([[4*I4 + 1, 4*I4 + 2], [4*I4 + 3, 4*I4]])

dithered_2 = dither(f_l, I2)
dithered_4 = dither(f_l, I4)
dithered_8 = dither(f_l, I8)

img_out = Image.fromarray(dithered_2.astype(np.uint8))
img_out.save('dithered_2.tif')

img_out = Image.fromarray(dithered_4.astype(np.uint8))
img_out.save('dithered_4.tif')

img_out = Image.fromarray(dithered_8.astype(np.uint8))
img_out.save('dithered_8.tif')
