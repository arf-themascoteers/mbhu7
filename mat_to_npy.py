import numpy as np
from scipy.io import loadmat
import os
import os
import shutil


def convert_mat_to_npy(mat_file_path, save_dir):
    data = loadmat(mat_file_path)
    data = {k: v for k, v in data.items() if not k.startswith('__')}

    os.makedirs(save_dir, exist_ok=True)

    for key, value in data.items():
        npy_path = os.path.join(save_dir, f"{key}.npy")
        np.save(npy_path, value)
        print(f"Saved {key} to {npy_path}")


os.makedirs("datasets/samson", exist_ok=True)

mat_file_path = "mat_datasets/samson_1.mat"
gt_file_path = "mat_datasets/end3.mat"

os.makedirs("tempwork", exist_ok=True)

convert_mat_to_npy(mat_file_path, "tempwork")
shutil.copy("tempwork/V.npy","datasets/samson/data.npy")

convert_mat_to_npy(gt_file_path, "tempwork")
shutil.copy("tempwork/A.npy","datasets/samson/gt.npy")