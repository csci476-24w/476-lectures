import numpy as np
import imageio

# some handy filter definitions
gauss1d5 = np.array([0.0625, 0.25, 0.375, 0.25, 0.0625]).reshape((1, 5))

sobel_x = np.array([
    [1, 0, -1],
    [2, 0, -2],
    [1, 0, -1]], dtype=np.float32)
sobel_y = sobel_x.T

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
    

def filter(img, kernel):
    """ Apply filter to img using cross-correlation. Preconditions:
      - img is a grayscale (2d) float image
      - filter is 2d and has odd side lengths """
    H, W = img.shape
    out = np.zeros_like(img)

    # half-widths:
    hwi = kernel.shape[0] // 2 
    hwj = kernel.shape[1] // 2 
    in_pad = np.pad(img, ((hwi, hwi), (hwj, hwj)))
    
    for i in range(H):
        for j in range(W):
            total = 0.0
            for ioff in range(-hwi, hwi+1):
                for joff in range(-hwj, hwj+1):
                    weight = kernel[hwi + ioff, hwj+joff]
                    total += weight * in_pad[hwi + i+ioff, hwj + j+joff]
            out[i, j] = total
    return out

def convolve(img, kernel):
    """ Apply filter to img using cross-correlation. Preconditions:
      - img is a grayscale (2d) float image
      - filter is square and has odd side length """
    return filter(img, np.fliplr(np.flipud(kernel)))

def separable_filter(img, kernel1d):
    """ Apply a filter kernel1d, then its transpose, to img.
    Precondition: kernel1d is symmetric. """
    return filter(filter(img, kernel1d), kernel1d.T)
    
def grad_mag(img):
    dx = convolve(img, sobel_x)
    dy = convolve(img, sobel_y)
    return np.sqrt(dx ** 2 + dy ** 2)

def down_2x(img):
    """ Downsample img by a factor of 2 in each dimension.
    Use prefiltering to avoid aliasing. 
    Pre: img is grayscale (2d) """
    out = separable_filter(img, gauss1d5)
    return out[::2,::2]

def down_4x(img):
    return down_2x(down_2x(img))

def up_2x(img, interp="nn"):
    """ Upsample img by a factor of 2 in each dimension.
    Pre: img is grayscale (2d)
    interp is one of ("nn", "gaussian", "linear") """
    H, W, = img.shape
    out = np.zeros((2*H, 2*W), dtype=img.dtype)
    if interp == "none":
        out[::2,::2] = img
        return out
    if interp == "nn":
        H, W, = img.shape
        out = np.zeros((2*H, 2*W), dtype=img.dtype)
        for (io, jo) in ((0, 0), (0, 1), (1, 0), (1, 1)):
            out[io::2, jo::2] = img
        return out
        
    elif interp == "gaussian":
        out[::2,::2] = img
        return separable_filter(out, gauss1d5) * 4

    elif interp == "linear":
        raise NotImplementedException # todo
 
def up_4x(img, interp="nn"):
    return up_2x(up_2x(img, interp=interp), interp=interp)