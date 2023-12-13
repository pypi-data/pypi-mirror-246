import argparse
import os
from typing import Tuple

import numpy as np


def rle(inarray: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """run length encoding.
    Multi datatype arrays catered for including non Numpy
    returns: tuple (runlengths, startpositions, values)"""
    ia = np.asarray(inarray)  # force numpy
    n = len(ia)
    assert n > 0, "Array must not be empty"
    y = ia[1:] != ia[:-1]  # pairwise unequal (string safe)
    i = np.append(np.where(y), n - 1)  # must include last element posi
    z = np.diff(np.append(-1, i))  # run lengths
    p = np.cumsum(np.append(0, z))[:-1]  # positions

    return (z, p, ia[i])


def format(anno_in: np.ndarray) -> np.ndarray:
    anno_le = rle(anno_in[:, 1])
    anno_out = []

    for i, c in enumerate(anno_le[2]):
        if c == 1:  # class 1 = outside
            pos_0 = anno_le[1][i]
            start = anno_in[pos_0, 0]
            if i + 1 < len(anno_le[1]):
                pos_1 = anno_le[1][i + 1]
                end = anno_in[pos_1, 0]
            else:
                end = anno_in[-1, 0]

            anno_out.append(np.array([start, end], dtype=np.int64))

    return np.vstack(anno_out)
