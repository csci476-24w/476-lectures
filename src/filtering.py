import numpy as np
import imageio

def brightness(img, scale):
    """ Change the brightness of img by scaling its pixel
    values uniformly by scale """
    raise NotImplementedError


def threshold(img, thresh):
    """ Threshold img such that the output is
    1 if the input is >= t, and 0 otherwise. """
    raise NotImplementedError

def mean_filter(img, filter_size):
    """ Apply a square spatial mean filter with side length filter_size
    to a grayscale img. Preconditions:
      - img is a grayscale (2d) float image
      - filter_size is odd """
    raise NotImplementedError

def filter(img, filter):
    """ Apply filter to img. Preconditions:
      - img is a grayscale (2d) float image
      - filter is square and has odd side length """
    raise NotImplementedError