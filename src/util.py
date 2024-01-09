import numpy as np
import matplotlib.pyplot as plt

def byte2float(img):
    """ Convert an image from bytes (0-255) to floats (0.0-1.0) """
    return img.astype(np.float32) / 255.0


def imshow_gray(img):
    assert len(img.shape) == 2
    plt.imshow(img, cmap="gray")