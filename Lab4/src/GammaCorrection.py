from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm

gray = cm.get_cmap('gray', 256)
im = Image.open('gamma15.tif')
x = np.array(im)

output = 255 * ((x/255)**(1.3398/1.5))

plt.imshow(output, cmap=gray)
plt.axis('off')
plt.show()