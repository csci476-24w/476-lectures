import numpy as np
import cv2

def warp_cv(img, tx, dsize=None):
    """ Just for now, until we write our own:
    warp img according to tx, a matrix representing a geometric transformation.
    Pre: tx is 3x3, 2x3, or 2x2"""

    H, W = img.shape[:2]
    txH, txW = tx.shape
    
    M = np.zeros((2, 3))
    M[:txH,:txW] = tx
    return cv2.warpAffine(img, M, dsize)

def warp(img, tx, dsize=None):
    """ Warp img using tx, a matrix representing a geometric transformation.
    Pre: tx is 3x3 (or some upper-left slice of a 3x3 matrix). img is grayscale.
    Returns: an output image of shape dsize with the warped img"""
    H, W = img.shape[:2]

    # turn a 2x2 or 2x3 tx into a full 3x3 matrix
    txH, txW = tx.shape
    M = np.eye(3)
    M[:txH,:txW] = tx

    # set the output size to the input size if not specified
    if dsize is None:
        DH, DW = (H, W)
    else:
        DH, DW = dsize[::-1]
    out = np.zeros((DH, DW))

    # your code here
    
    return out


def estimate_translation(correspondences):
    """ Returns a translation vector (tx, ty) that is the average
    of the correspondences, given in the format as returned by
    features.get_matches """