"""
Load the data, reformat it to have [SAMPLES, ....] dimensions,
split it into train, test and val sets and save them in .h5 file with
'train', 'val' and 'test' groups, each having 'data' and 'labels' keys.
"""

import os
import numpy as np
import clize
from clize.parameters import multi

import mbcnn.mbcnn_io as io
import mbcnn.preprocessing as preprocessing
import mbcnn.utils as utils

EXTENSION = 1


def main(*,
         data_file_path: str,
         ground_truth_path: str,
         output_path: str = None,
         train_size: ('train_size', multi(min=0)),
         val_size: float = 0.1,
         stratified: bool = True,
         background_label: int = 0,
         neighborhood_size: int = None,
         channels_idx: int = 0,
         save_data: bool = False,
         seed: int = 0,
         use_unmixing: bool = False,
         spatial_overlap: bool = True):
    """
    :param data_file_path: Path to the data file. Supported types are: .npy
    :param ground_truth_path: Path to the data file.
    :param output_path: Path under in which the output .h5 file will be stored.
        Used only if the parameter save_data is set to True
    :param train_size: If float, should be between 0.0 and 1.0,
                        if stratified = True, it represents percentage of each
                        class to be extracted,
                 If float and stratified = False, it represents
                    percentage of the whole dataset to be extracted
                    with samples drawn randomly, regardless of their class.
                 If int and stratified = True, it represents number of samples
                    to be drawn from each class.
                 If int and stratified = False, it represents overall number of
                    samples to be drawn regardless of their class, randomly.
                 Defaults to 0.8
    :type train_size: float or int
    :param val_size: Should be between 0.0 and 1.0. Represents the
                     percentage of each class from the training set
                     to be extracted as a validation set, defaults to 0.1
    :param stratified: Indicated whether the extracted training set should be
                     stratified, defaults to True
    :param background_label: Label indicating the background in GT file.
    :param neighborhood_size: Size of the spatial patch.
    :param channels_idx: Index specifying the channels position in the provided
                         data
    :param save_data: Whether to save data as .md5 or to return it as a dict
    :param seed: Seed used for data shuffling
    :param use_unmixing: Boolean indicating whether to perform experiments
        on the unmixing datasets, where classes in each pixel
        are present as fractions.
    :param spatial_overlap: Boolean indicating whether to create non
        overlapping patches of training and test subsets.
    :raises TypeError: When provided data or labels file is not supported
    """
    train_size = utils.parse_train_size(train_size)
    if data_file_path.endswith('.npy') and ground_truth_path.endswith('.npy'):
        data, labels = io.load_npy(data_file_path, ground_truth_path,
                                   use_unmixing)
        height, width, _ = data.shape
        if neighborhood_size is None:
            data, labels = preprocessing.reshape_cube_to_2d_samples(
                data, labels, channels_idx, use_unmixing)

        else:
            data, labels = preprocessing.reshape_cube_to_3d_samples(
                data, labels, neighborhood_size,
                background_label, channels_idx, use_unmixing)
    elif data_file_path.endswith('.h5') and ground_truth_path.endswith(
            '.tiff'):
        data, gt_transform_mat = io.load_satellite_h5(data_file_path)
        labels = io.load_tiff(ground_truth_path)
        data_2d_shape = data.shape[1:]
        labels = preprocessing.align_ground_truth(data_2d_shape, labels,
                                                  gt_transform_mat)
        height, width, _ = data.shape
        if neighborhood_size is None:
            data, labels = preprocessing.reshape_cube_to_2d_samples(
                data, labels, channels_idx)
        else:
            data, labels = preprocessing.reshape_cube_to_3d_samples(
                data, labels, neighborhood_size, background_label,
                channels_idx)
    else:
        raise ValueError(
            "The following data file type is not supported: {}".format(
                os.path.splitext(data_file_path)[EXTENSION]))
    data, labels = preprocessing.remove_nan_samples(data, labels)
    print(data.shape)
    print(labels.shape)
    if not use_unmixing:
        data = data[labels != background_label]
        labels = labels[labels != background_label]
        labels = preprocessing.normalize_labels(labels)
    train_x, train_y, val_x, val_y, test_x, test_y = \
        preprocessing.train_val_test_split(
            data, labels, train_size, val_size,
            stratified, seed, spatial_overlap,
            neighborhood_size, height, width, output_path)

    if save_data:
        io.save_md5(output_path, train_x, train_y, val_x, val_y, test_x,
                    test_y)
        return None
    else:
        return utils.build_data_dict(train_x, train_y, val_x, val_y, test_x,
                                     test_y, data_file_path)


if __name__ == '__main__':
    #clize.run(main)
    main(
        data_file_path="D:\\src\\mbhu7\\datasets\\samson\\data.npy",
        ground_truth_path="D:\\src\\mbhu7\\datasets\\samson\\gt.npy",
        train_size=[0.8],
        val_size=0.1,
        save_data=True,
        output_path="output.h5",
        use_unmixing=True
    )
