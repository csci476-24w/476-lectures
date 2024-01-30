import numpy as np
import matplotlib.pyplot as plt

def byte2float(img):
    """ Convert an image from bytes (0-255) to floats (0.0-1.0) """
    return img.astype(np.float32) / 255.0

def imshow_gray(img):
    assert len(img.shape) == 2
    plt.imshow(img, cmap="gray")

def imshow_truesize(img):
    dpi = plt.rcParams['figure.dpi']
    height, width = img.shape[:2]
    figsize = width / float(dpi), height / float(dpi)

    fig = plt.figure(figsize=figsize)
    ax = fig.gca()
    ax.set_axis_off()
    fig.subplots_adjust(0,0,1,1)
    plt.imshow(img, cmap="gray", interpolation="none")

    