"""
This module is an example of a barebones numpy reader plugin for napari.

It implements the Reader specification, but your plugin may choose to
implement multiple readers or even other plugin contributions. see:
https://napari.org/stable/plugins/guides.html?#readers
"""
# import numpy as np


# def napari_get_reader(path):
#     """A basic implementation of a Reader contribution.

#     Parameters
#     ----------
#     path : str or list of str
#         Path to file, or list of paths.

#     Returns
#     -------
#     function or None
#         If the path is a recognized format, return a function that accepts the
#         same path or list of paths, and returns a list of layer data tuples.
#     """
#     if isinstance(path, list):
#         # reader plugins may be handed single path, or a list of paths.
#         # if it is a list, it is assumed to be an image stack...
#         # so we are only going to look at the first file.
#         path = path[0]

#     # if we know we cannot read the file, we immediately return None.
#     if not path.endswith(".npy"):
#         return None

#     # otherwise we return the *function* that can read ``path``.
#     return reader_function


# def reader_function(path):
#     """Take a path or list of paths and return a list of LayerData tuples.

#     Readers are expected to return data as a list of tuples, where each tuple
#     is (data, [add_kwargs, [layer_type]]), "add_kwargs" and "layer_type" are
#     both optional.

#     Parameters
#     ----------
#     path : str or list of str
#         Path to file, or list of paths.

#     Returns
#     -------
#     layer_data : list of tuples
#         A list of LayerData tuples where each tuple in the list contains
#         (data, metadata, layer_type), where data is a numpy array, metadata is
#         a dict of keyword arguments for the corresponding viewer.add_* method
#         in napari, and layer_type is a lower-case string naming the type of
#         layer. Both "meta", and "layer_type" are optional. napari will
#         default to layer_type=="image" if not provided
#     """
#     # handle both a string and a list of strings
#     paths = [path] if isinstance(path, str) else path
#     # load all files into array
#     arrays = [np.load(_path) for _path in paths]
#     # stack arrays into single array
#     data = np.squeeze(np.stack(arrays))

#     # optional kwargs for the corresponding viewer.add_* method
#     add_kwargs = {}

#     layer_type = "image"  # optional, default is "image"
#     return [(data, add_kwargs, layer_type)]



import json
import os

import numpy as np
from pathlib import Path

def napari_get_reader(path):
    """A basic implementation of a Reader contribution.

    Parameters
    ----------
    path : str or list of str
        Path to file, or list of paths.

    Returns
    -------
    function or None
        If the path is a recognized format, return a function that accepts the
        same path or list of paths, and returns a list of layer data tuples.
    """
    if isinstance(path, list):
        # reader plugins may be handed single path, or a list of paths.
        # if it is a list, it is assumed to be an image stack...
        # so we are only going to look at the first file.
        path = path[0]

    # if we know we cannot read the file, we immediately return None.
    if not path.endswith(".json"):
        return None

    # otherwise we return the *function* that can read ``path``.
    return reader_function


def reader_function(path):
    """Take a path or list of paths and return a list of LayerData tuples.

    Readers are expected to return data as a list of tuples, where each tuple
    is (data, [add_kwargs, [layer_type]]), "add_kwargs" and "layer_type" are
    both optional.

    Parameters
    ----------
    path : str or list of str
        Path to file, or list of paths.

    Returns
    -------
    layer_data : list of tuples
        A list of LayerData tuples where each tuple in the list contains
        (data, metadata, layer_type), where data is a numpy array, metadata is
        a dict of keyword arguments for the corresponding viewer.add_* method
        in napari, and layer_type is a lower-case string naming the type of
        layer. Both "meta", and "layer_type" are optional. napari will
        default to layer_type=="image" if not provided
    """
    # # handle both a string and a list of strings
    # paths = [path] if isinstance(path, str) else path
    # # load all files into array
    # arrays = [np.load(_path) for _path in paths]
    # # stack arrays into single array
    # data = np.squeeze(np.stack(arrays))

    # # optional kwargs for the corresponding viewer.add_* method
    # add_kwargs = {}

    # layer_type = "image"  # optional, default is "image"
    # return [(data, add_kwargs, layer_type)]

    path = os.path.normpath(path)

    # print(path)

    # print(os.path.dirname(path))
    # print(os.path.basename(path))
    # print(os.path.split(path))

    # print(os.path.split(os.path.dirname(path))[1])

    f = open(path)
    data = json.load(f)

    # test_points = np.random.randint(0,1000,size=(20000,3))
    test_points = np.array(data["labels"])

    label_name = os.path.split(os.path.dirname(path))[1]
    add_kwargs = {
        "name": label_name,
        "face_color": "transparent",
        "edge_color": "blue",
        "size": 20,
    }

    layer_type = "points"  # optional, default is "image"
    return [(test_points, add_kwargs, layer_type)]







def napari_get_reader_dir(path):
    """A basic implementation of a Reader contribution.

    Parameters
    ----------
    path : str or list of str
        Path to file, or list of paths.

    # Returns
    -------
    function or None
        If the path is a recognized format, return a function that accepts the
        same path or list of paths, and returns a list of layer data tuples.
    """
    if isinstance(path, list):
        # reader plugins may be handed single path, or a list of paths.
        # if it is a list, it is assumed to be an image stack...
        # so we are only going to look at the first file.
        path = path[0]

    # if we know there is not a single json file in the directory, we immediately return None.
    json_dir = str(path)
    files = [fl for fl in os.listdir(json_dir) if fl.endswith('.json') ]
    if len(files) == 0:
        return None

    return reader_pram_anno


def reader_pram_anno(path):
    # check if folder exist , regex
    image_dir = str(path).replace("_GT", "") 

    print(image_dir)
    base_dir = os.path.dirname(path)
    file_dir = os.path.basename(path)
    
    # new_dir = os.path.join(base_dir, file_dir)
    # print(new_dir)

    # print(os.listdir(Path(image_dir)))

    data_stk = []

    files = [fl for fl in os.listdir(image_dir) if fl.endswith('.tif') | fl.endswith('.tiff') | fl.endswith('.png')]


    for i, fl in enumerate(files):
        # data_stk.append(np.array([i, None, None]))

        ext = os.path.splitext(fl)[1][1:]

        if os.path.exists(os.path.join(path, fl.replace(ext, "json"))):  
            f = open(os.path.join(path, fl.replace(ext, "json")))

            # returns JSON object as
            # a dictionary
            data = json.load(f)
            # print(data["labels"])

            new_col = np.full((len(data["labels"]), 1), i)
            new_data = np.concatenate((new_col, data["labels"]), 1)
            data_stk.extend(new_data)

    test_points = np.array(data_stk)

    # test_points = np.random.randint(0,1000,size=(20000,3))
    # path.split("/")[-2]

    add_kwargs = {"face_color": "red", "size": 5}

    # add_kwargs =  {"face_color": "transparent", "edge_color": "blue", "size": 20}

    layer_type = "points"  # optional, default is "image"
    return [(test_points, add_kwargs, layer_type)]