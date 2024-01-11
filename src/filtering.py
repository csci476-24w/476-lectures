import numpy as np
import imageio

def brightness(img, scale):
    """ Change the brightness of img by scaling its pixel
    values uniformly by scale """
    return img * scale


def threshold(img, thresh):
    """ Threshold img such that the output is
    1 if the input is >= t, and 0 otherwise. """
    out = np.zeros_like(img)
    out[img >= thresh] = 1
    return out

    
def mean_filter(img, filter_size):
    """ Apply a square spatial mean filter with side length filter_size
    to a grayscale img. Preconditions:
      - img is a grayscale (2d) float image
      - filter_size is odd """
    H, W = img.shape
    out = np.zeros_like(img)

    hw = filter_size // 2 # half-width

    in_pad = np.pad(img, ((hw, hw), (hw, hw)))
    
    for i in range(H):
        for j in range(W):
            total = 0.0
            for ioff in range(-hw, hw+1):
                for joff in range(-hw, hw+1):
                    total += in_pad[hw + i+ioff, hw + j+joff]
            out[i, j] = total / filter_size**2
    return out
    

def filter(img, filter):
    """ Apply filter to img using cross-correlation. Preconditions:
      - img is a grayscale (2d) float image
      - filter is square and has odd side length """
    raise NotImplementedException

def convolve(img, filter):
    """ Apply filter to img using cross-correlation. Preconditions:
      - img is a grayscale (2d) float image
      - filter is square and has odd side length """