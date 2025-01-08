from random import shuffle
from pyomo.environ import *
from numpy import linalg as la
from numpy import random as r
from collections import deque
import numpy as np

def build_model():
    """Builds the mathematical optimization model for k-means."""
    model = AbstractModel()
    model.k = Param(within=NonNegativeIntegers)  # Number of clusters
    model.n = Param(within=NonNegativeIntegers)  # Number of data points
    model.d = Param(within=NonNegativeIntegers)  # Number of dimensions

    model.I = RangeSet(1, model.k)
    model.J = RangeSet(1, model.n)

    model.x = Param(model.d, model.n)  # Data points (to be populated)
    return model

def get_clusters(X, pos, sites, k):
    """Assigns data points to the nearest cluster based on site proximity."""
    clusters = [[] for _ in range(k)]  # Create empty clusters
    for i in range(X.shape[0]):
        distance = la.norm(sites - X[i, :], axis=1)  # Compute distance to each site
        clusters[np.argmin(distance)].append(pos[i])  # Assign to the closest cluster
    return clusters

def update_sites(k, sites, X, W):
    """Update the cluster centroids based on weighted distances."""
    clusters, distances = np.repeat(np.array(W), k, axis=0), np.zeros((X.shape[0], k))
    
    for i in range(X.shape[0]):
        distance = la.norm(sites - X[i, :], axis=1)
        min_site = r.permutation(np.where(distance == np.min(distance))[0])[0]  # Randomly break ties
        assignment_vector = np.zeros(k)
        assignment_vector[min_site] = 1  # Assign the data point to the closest cluster
        distances[i, min_site] = np.min(distance)
        clusters[:, i] = clusters[:, i] * assignment_vector
    
    # Update the sites based on the weighted clusters
    distances = np.matrix(clusters) * np.matrix(distances) / clusters.sum(axis=1)
    return clusters * X / clusters.sum(axis=1).reshape(k, 1), distances.diagonal()

def weighted_kmeans(k, n, d, X, W, iters=1):
    """Performs k-means clustering with weights for a set number of iterations."""
    clusterings = {}
    for _ in range(iters):
        s, prev_s, distances = r.permutation(X)[:k, :], np.zeros((k, d)), np.zeros(k)
        while np.sum(la.norm(s - prev_s, axis=1)) > 0:  # Continue until convergence
            prev_s = s
            s, distances = update_sites(k, s, X, W)
        clusterings[np.sum(distances) / k] = s  # Store clustering by average distance
    return clusterings[np.min(list(clusterings.keys()))]  # Return the best clustering based on distance

def hierarchical_kmeans(n, d, X, W, k_plus):
    """Performs hierarchical k-means clustering recursively."""
    queue, pos, classif, clusterings = deque([np.array(range(n))]), np.arange(n), 0, np.zeros(n)
    
    while queue:
        c = queue.popleft()
        sub_X, sub_W, sub_n = X[c, :], W[0, c], c.shape[0]
        if sub_X.shape[0] <= k_plus:  # If the cluster is small enough, assign a label
            clusterings[c] = classif
            classif += 1
            continue
        clusters = get_clusters(sub_X, pos[c], weighted_kmeans(2, sub_n, d, sub_X, sub_W, 1), 2)
        for cluster in clusters:
            queue.append(np.array(cluster))  # Recurse for sub-clusters
    return clusterings
