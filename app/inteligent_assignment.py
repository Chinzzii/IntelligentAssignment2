from numpy import random as r
import numpy as np
import weighted_kmeans as wkmeans


def intelligent_assignment(x, w, data_id, mts):
    """Handles intelligent assignment of users to clusters based on weighted k-means."""
    print(w)  # Print the weight array
    # Perform hierarchical k-means clustering and print the result
    print(wkmeans.hierarchical_kmeans(len(x), len(x[0]), x, w, 3))


# Generate random data for testing
n, d = 100, 3
data = np.matrix(r.randint(100, size=(n, d)))  # Random dataset
weights = np.matrix(r.randint(1, 4, size=(1, n)))  # Random weights
intelligent_assignment(data, weights, [], 3)  # Run the assignment function
