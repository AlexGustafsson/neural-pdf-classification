# Run with: python3 -m clustering.py "/path/to/dataset.txt"

from ast import literal_eval as parse_tuple

import sys

import hdbscan
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn.datasets as data
sns.set_context('poster')
sns.set_style('white')
sns.set_color_codes()
plot_kwds = {'alpha' : 0.5, 's' : 80, 'linewidths':0}

from sklearn.datasets import make_blobs

filename = sys.argv[1]

# List of tuples containing features:
dataset = []
texts = []

with open(filename, 'r') as dataset_file:
    for line in dataset_file:
        page_index, top, left, width, height, font, font_size, text = parse_tuple(line)
        dataset.append([top, left, width, height, font_size])
        texts.append(text)

# Calculate clusters
clusterer = hdbscan.HDBSCAN(min_cluster_size=2)
labels = clusterer.fit_predict(dataset)

print("Found {} clusters.".format(labels.max()))

# Map cluster labels to texts
clusters = {}
for i, label in enumerate(labels):
    if label not in clusters:
        clusters[label] = []
    clusters[label].append(texts[i])

# Sort the clusters descending based on size
sorted_clusters = list(clusters.values())
sorted_clusters.sort(key=len, reverse=True)

# Print the top 2 clusters
for i in range(1,20):
    print(sorted_clusters[i][:10])
