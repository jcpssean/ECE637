from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm

board = np.zeros((256, 256))
gray = 0
white_start = 1

for i in range(0, 256, 2):
    if gray == 16: 
        gray = 0

    for j in range(0, 256, 2):
        if gray < 8:
            if white_start == 1:
                board[i:i+2, j:j+2] = 255
                white_start = 0
            else:
                board[i:i+2, j:j+2] = 0
                white_start = 1
        else:
            board[i:i+2, j:j+2] = 152

    white_start = 1 - white_start
    gray += 1
        


plt.imshow(board, cmap='gray')
plt.axis('off')
plt.show()