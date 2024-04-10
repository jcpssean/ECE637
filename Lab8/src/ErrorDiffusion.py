from PIL import Image
import numpy as np

def errorDiffusion(img_l):
    T = 127
    out = np.zeros(img_l.shape)
    img_l = np.pad(img_l, ((1, 1), (1, 1)))

    for i in range(1, img_l.shape[0]-1):
        for j in range(1, img_l.shape[1]-1):
            if img_l[i, j] > T:
                out[i-1, j-1] = 255
            else:
                out[i-1, j-1] = 0

            error = img_l[i, j] - out[i-1, j-1]

            img_l[i, j+1] += error * 7/16
            img_l[i+1, j-1] += error * 3/16
            img_l[i+1, j] += error * 5/16
            img_l[i+1, j+1] += error * 1/16

    return out

im = Image.open('house.tif')
input_img = np.array(im, dtype=np.float32)
f_l = 255 * ((input_img / 255) ** 2.2)

output_img = errorDiffusion(f_l)

img_out = Image.fromarray(output_img)
img_out.save('error_diffused.tif')
