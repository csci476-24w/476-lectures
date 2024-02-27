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

    Minv = np.linalg.inv(M)
    for y in range(DH):
        for x in range(DW):
            xh, yh, wh = Minv @ [x, y, 1]
            xsrc = round(xh/wh)
            ysrc = round(yh/wh)
            if (0 <= xsrc < W) and (0 <= ysrc < H):
                out[y, x] = img[ysrc, xsrc]
    
    return out


def estimate_translation(correspondences):
    """ Returns a translation vector (tx, ty) that is the average
    of the correspondences, given in the format as returned by
    features.get_matches """


def cross(a, b):
    """ Return the cross product of 3-vectors a and b. """
    x1, y1, z1 = a
    x2, y2, z2 = b
    return np.array([
        y1*z2 - z1*y2,
        z1*x2 - x1*z2,
        x1*y2 - y1*x2
    ])

def cross_matrix(a):
    """ Return the 3x3 skew-symmetric matrix A such that
    matrix multiplying A @ b yields cross(a, b) """
    x, y, z = a
    return np.array([
        [ 0, -z,  y],
        [ z,  0, -x],
        [-y,  x,  0]
    ])