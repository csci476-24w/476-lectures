import numpy as np
import cv2

def warp(img, tx, dsize=None, bottom_left_origin=True):
    """ Just for now, until we write our own:
    warp img according to tx, a 2x2 matrix representing a geometric transformation.
    Pre: tx is a 2x2 matrix"""

    H, W = img.shape[:2]
    txH, txW = tx.shape
    
    M = np.zeros((2, 3))
    M[:txH,:txW] = tx
    return cv2.warpAffine(img, M, dsize)

def estimate_translation(correspondences):
    """ Returns a translation vector (tx, ty) that is the average
    of the correspondences, given in the format as returned by
    features.get_matches """