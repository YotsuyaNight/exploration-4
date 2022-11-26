from dataclasses import dataclass
import json
import re
import numpy as np
from rev_index import read_all_documents, build_rev_index, fetch_phrase_freq_from_index

@dataclass
class CarObject:
    id: str
    features: np.ndarray

def __read_car_data__(id):
    data_filepath = f'scrapped_data/data/{id}.txt'
    with open(data_filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def _clean_numeric__(value):
    return int(re.sub('(cm3)|\D', '', value))

documents = read_all_documents()
rev_index = build_rev_index(documents)

# Build feature vectors for KNN
vectors = []
for id in documents.keys():
    car_data = __read_car_data__(id)
    vector = [
        _clean_numeric__(car_data["Rok produkcji"]),
        _clean_numeric__(car_data["Przebieg"]),
        _clean_numeric__(car_data["Moc"]),
        _clean_numeric__(car_data["Pojemność skokowa"]),
    ]
    vectors.append(CarObject(id, np.array(vector)))

# Normalizing feature vectors
features_count = len(vectors[0].features)
for i in range(0, features_count):
    minval = float('inf')
    maxval = float('-inf')
    for vector in vectors:
        minval = min(minval, vector.features[i])
        maxval = max(maxval, vector.features[i])
    for vector in vectors:
        vector.features[i] = (vector.features[i] - minval) / (maxval - minval) * 100

# Prepare centroids
cluster_count = 3
centroids = []
clusters = []
for i in range(0, cluster_count):
    value = 100 / (cluster_count - 1) * i
    centroids.append(np.ones(features_count) * value)

# Run k-means clustering
passes = 20
for _ in range(0, passes):
    new_clusters = [[] for _ in range(0, cluster_count)]
    # Assign objects to clusters based on centroids
    for vector in vectors:
        distances_from_centroids = [np.linalg.norm(centroid - vector.features) for centroid in centroids]
        assignment = distances_from_centroids.index(min(distances_from_centroids))
        new_clusters[assignment].append(vector)
    # Recalculate centroids
    clusters = new_clusters
    for i, cluster in enumerate(clusters):
        if not cluster: continue
        cluster_elems = np.array([vector.features for vector in cluster])
        centroids[i] = np.average(cluster_elems, axis=0)

# Save clustering result
for i, cluster in enumerate(clusters):
    cluster_filepath = f'scrapped_data/clusters/{i}.txt'
    with open(cluster_filepath, "w+", encoding="utf-8") as file:
        for vector in cluster:
            file.write(vector.id + "\n")
