from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm


gray = cm.get_cmap('gray', 256)
im = Image.open('kids.tif')
x = np.array(im)
plt.hist(x.flatten(),bins=np.linspace(0,255,256))
plt.title('Histogram of kids.tif')
plt.xlabel('pixel value')
plt.ylabel('number of pixels')
plt.xlim(0, 260)
plt.show()