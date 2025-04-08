from scipy.io import loadmat

data = loadmat('datasets/samson/samson_1.mat')
for key in data:
    if not key.startswith('__'):
        print(key, type(data[key]), data[key].shape if hasattr(data[key], 'shape') else 'scalar')
