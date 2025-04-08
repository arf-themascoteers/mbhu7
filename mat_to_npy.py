import numpy as np
from scipy.io import loadmat
import os


def convert_mat_to_npy(mat_file_path):
    data = loadmat(mat_file_path)
    data = {k: v for k, v in data.items() if not k.startswith('__')}

    save_dir = os.path.dirname(mat_file_path)
    os.makedirs(save_dir, exist_ok=True)

    for key, value in data.items():
        npy_path = os.path.join(save_dir, f"{key}.npy")
        np.save(npy_path, value)
        print(f"Saved {key} to {npy_path}")


mat_file_path = "datasets/samson/end3.mat"
convert_mat_to_npy(mat_file_path)