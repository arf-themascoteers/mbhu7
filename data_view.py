import numpy as np
import matplotlib.pyplot as plt

data = np.load('datasets/samson/A.npy')
data = data.reshape((3,95,95))
print(data.shape)

np.save('datasets/samson/A_modified.npy', data)
# view = data[0]
# plt.imshow(view, cmap='gray')
# plt.colorbar()
# plt.show()