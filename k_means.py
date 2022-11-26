from dataclasses import dataclass
import json
import re
import numpy as np
from rev_index import read_all_documents, build_rev_index, fetch_phrase_freq_from_index

@dataclass
class CarObject:
    id: str
    features: list[float]

def __read_car_data__(id):
    data_filepath = f'scrapped_data/data/{id}.txt'
    with open(data_filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def _clean_numeric__(value):
    return int(re.sub('(cm3)|\D', '', value))

def __euclidean_distance__(v1, v2):
    return sum([(x[0] - x[1])**2 for x in zip(v1, v2)])

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
    vectors.append(CarObject(id, vector))

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

print(vectors)

# Prepare centroids
cluster_count = 3
centroids = []
clusters = []
for i in range(0, cluster_count):
    centroid = [100 / (cluster_count - 1) * i] * features_count
    centroids.append(centroid)

# Run k-means clustering
passes = 1
for _ in range(0, passes):
    new_clusters = [[] for _ in range(i, cluster_count)]
    # Assign objects to clusters based on centroids
    for vector in vectors:
        distances_from_centroids = [__euclidean_distance__(centroid, vector.features) for centroid in centroids]
        assignment = distances_from_centroids.index(min(distances_from_centroids))
        new_clusters[assignment].append(vector)
    # Recalculate centroids
    clusters = new_clusters
    for i, cluster in enumerate(clusters):
        for j in range(0, features_count):
            centroids[i][j] = sum([x[j] for x in cluster]) / len(cluster)
