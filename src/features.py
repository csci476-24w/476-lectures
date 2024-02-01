import numpy as np
import filtering
from filtering import convolve, separable_filter
from filtering import sobel_x, sobel_y, gauss1d5
import geometry

def harris_score(img):
    """ Returns the smaller eigenvalue of the structure tensor for each pixel in img.
    Pre: img is grayscale, float, [0,1]. Returns an array the same shape as img."""
    dx = convolve(img, sobel_x)
    dy = convolve(img, sobel_y)
    A = separable_filter(dx * dx, gauss1d5)
    B = separable_filter(dx * dy, gauss1d5)
    C = separable_filter(dy * dy, gauss1d5)

    det = A*C - B*B
    tr = A+C
    
    m = tr / 2
    p = det
    sqrtm2mp = np.sqrt(m**2 - p)
    eig1 = m - sqrtm2mp
    eig2 = m + sqrtm2mp
    return np.minimum(eig1, eig2)

def harris_corners(img, threshold):
    scores = harris_score(img)
    scores_maxfilter = filtering.maximum_filter(scores, 7)
    features_mask = np.logical_and(scores > threshold, scores == scores_maxfilter)
    return features_mask

def get_harris_points(harris_mask):
    i, j = np.nonzero(harris_mask)
    return np.vstack((i, j))

def extract_MOPS(img, point):
    """ point is in (j, i) format so it can be treated as (x, y) with origin
    in the top left """
    # translate center patch to origin
    y, x = point
    tx1 = np.array([
        [1, 0, -x],
        [0, 1, -y],
        [0, 0, 1]], dtype=np.float32)

    # scale down by 1/8
    scale = np.array([
        [.125, 0, 0],
        [0, .125, 0],
        [0, 0, 1]], dtype=np.float32)
    
    # rotate to gradient magnitude direction to 0
    dx, dy = filtering.grad(img)[59, 32, :]
    angle = np.arctan2(dy, dx)
    rot = np.array([
        [np.cos(angle), np.sin(angle), 0],
        [-np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]], dtype=np.float32)

    # translate so a 5x5 patch has its corner at (0, 0)
    tx2 = np.array([
        [1, 0, 2.5],
        [0, 1, 2.5],
        [0, 0, 1]], dtype=np.float32)

    # compose the transformations and warp the image into a 5x5 output image
    M = tx2 @ rot @ scale @ tx1 # TODO - compose all the transformations
    
    desc = geometry.warp(img, M[:2,:], dsize=(5, 5))

    # TODO: standardize intensity values
    
    return desc
    
def ssd(f, g):
    # TODO
    pass




### messy visualization code - read at your own risk

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

def visualize_harris(img, i, j, topdown=True, window_halfwidth=3, error_surface_halfwidth=6):
    """ I'm sorry """
    # img: grayscale float image
    # i, j: image coordinates of the candidate keypoint to visualize
    # topdown: whether to default to a top-down view of the error surface

    k = window_halfwidth # Harris window is a square with side length 2k+1
    uv_k = error_surface_halfwidth # size of the error surface grid (a 2uv_k+1 square)
    
    # center of window (i.e., feature location)
    y, x = i, j
    
    ## plot the image with a red box around the window
    fig = plt.gcf()
    fig.clf()
    fig.set_size_inches(8, 8)
    
    plt.subplot(2, 2, 1, title="Window around the candidate feature point")
    plt.imshow(img, cmap='gray')
    box = patches.Rectangle((x-k-1, y-k-1), 2*k+1, 2*k+1, # (left, bottom), width, height
                            linewidth=1, edgecolor='r', facecolor='none')
    ax = plt.gca()
    ax.add_patch(box)
    
    
    ## compute measured E(u,v) for a grid of nearby offsets
    I = img.copy()
    ys, ye = y-k, y+k+1 # start and end of the patch y range
    xs, xe = x-k, x+k+1 # start and end of the patch x range
    e_true = np.zeros((2*uv_k+1,2*uv_k+1))
    orig_patch = I[ys:ye, xs:xe]
    for u in range(-uv_k, uv_k + 1):
      for v in range(-uv_k, uv_k + 1):
        e_true[u+uv_k, v+uv_k] = np.sum((orig_patch - I[ys+u:ye+u, xs+v:xe+v])**2)
    
    # plot it
    ax = plt.subplot(2, 2, 2, projection='3d', title="E(u,v) actual")
    X, Y = np.meshgrid(range(-uv_k, uv_k + 1), range(-uv_k, uv_k + 1))
    ax.set_proj_type('ortho')
    ax.plot_surface(X, Y, e_true, cmap=cm.coolwarm)
    ax.set_zlim(0, 4)
    if topdown:
        ax.view_init(elev=90, azim=0)   
    
    ## compute approximate E(u,v) based on first-order Taylor approximation
    Ix = sp.ndimage.sobel(I, axis=1) / 8
    Iy = sp.ndimage.sobel(I, axis=0) / 8
    
    e_approx = np.zeros_like(e_true)
    orig_patch = I[ys:ye, xs:xe]
    for u in range(-uv_k, uv_k + 1):
      for v in range(-uv_k, uv_k + 1):
        Ixu = (Ix[ys:ye, xs:xe])*u
        Iyv = (Iy[ys:ye, xs:xe])*v
        e_approx[u+uv_k, v+uv_k] = np.sum((Ixu + Iyv)**2)
    
    # plot it
    ax = plt.subplot(2, 2, 3, projection='3d', title="E(u,v) approximate")
    X, Y = np.meshgrid(range(-uv_k, uv_k + 1), range(-uv_k, uv_k + 1))
    ax.set_proj_type('ortho')
    ax.plot_surface(X, Y, e_approx, cmap=cm.coolwarm)
    ax.set_zlim(0, 10)
    if topdown:
        ax.view_init(elev=90, azim=0)

    ax = plt.subplot(2, 2, 4, projection='3d', title="E(u,v) approximate contours")
    ax = plt.subplot(2, 2, 4, title="E(u,v) approximate contours")

    # X, Y = np.meshgrid(range(-uv_k, uv_k + 1), range(-uv_k, uv_k + 1))
    # ax.set_proj_type('ortho')
    ax.contour(e_approx, cmap=cm.coolwarm)

    # ax.contour(X, Y, e_approx, cmap=cm.coolwarm)
    # ax.set_zlim(0, 10)
    # if topdown:
    #     ax.view_init(elev=90, azim=0)
    plt.show()

def overlay_features(img, corners):
    h, w = img.shape
    out = np.zeros((h, w, 3))
    out[:,:,:] = img[:,:,np.newaxis] / 2
    out[corners>0, :] = [1, 0, 0]
    return out