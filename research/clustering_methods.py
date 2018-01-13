from enum import Enum


class ClusteringMethods(Enum):
    Kmeans = 'kmeans'
    Spectral = 'spectral'
    DBScan = 'dbscan'
    HDBScan = 'hdbscan'
    PcaKmeans = 'pca-kmeans'
    PcaDBScan = 'pca-dbscan'
    PcaHDBScan = 'pca-hdbscan'
