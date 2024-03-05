import numpy as np

import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
from matplotlib.colors import ListedColormap
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class MLP(nn.Module):
    def __init__(self, in_channels):
        super().__init__()
        
        self.layer1 = nn.Linear(in_channels, 128)
        self.layer2 = nn.Linear(128, 128)
        self.layer3 = nn.Linear(128, 1)
        

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        x = self.layer3(x)
        return x

class MLP_N(nn.Module):
    def __init__(self, in_channels, n_layers, hidden_size):
        super().__init__()
        self.layers = nn.ModuleList()
        self.layers.append(nn.Linear(in_channels, hidden_size))
        for _ in range(n_layers-2):
            self.layers.append(nn.Linear(hidden_size, hidden_size))
        self.layers.append(nn.Linear(hidden_size, 1))

    def forward(self, x):
        for layer in self.layers[:-1]:
            x = F.relu(layer(x))
        return self.layers[-1](x)
        

def scale_split(ds):
    """ Apply standard scaling and split a dataset into train/val sets.
    ds is a 2-tuple of X (N, d) and y (n,) 
    Returns:
        Xtr, Xva - train and val splits for X
        ytr, yva - train and val splits for y
        xx, yy - meshgrid coordinates for plotting"""
    X, y = ds
    X = StandardScaler().fit_transform(X)
    Xtr, Xva, ytr, yva = train_test_split(
        X, y, test_size=0.4, random_state=42
    )
    
    # Create a dense grid so we can show the decision boundary/classifier scores
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02), np.arange(y_min, y_max, 0.02))

    return (torch.Tensor(a) for a in (Xtr, Xva, ytr, yva, xx, yy))


def plot_dataset(Xtr, ytr):

    ax = plt.gca()
    cm = plt.cm.RdBu
    cm_bright = ListedColormap(["#FF0000", "#0000FF"])

    # Train:
    ax.scatter(Xtr[:, 0], Xtr[:, 1], c=ytr, cmap=cm_bright, edgecolors="k")


def make_stripes(N, num_stripes, noise=0.01):
    X = []
    y = []
    stripe_centers = np.linspace(noise, 1-noise, num_stripes)
    for i, sc in enumerate(stripe_centers):
        xs = np.column_stack([
            np.random.rand(N//num_stripes) * 2*noise - noise + sc,
            np.random.rand(N//num_stripes)
        ])
        X.append(xs)
                 
        y.append(np.ones((xs.shape[0],)) * i % 2)

    return torch.Tensor(np.concatenate(X, axis=0)), torch.Tensor(np.concatenate(y, axis=0))

        

    