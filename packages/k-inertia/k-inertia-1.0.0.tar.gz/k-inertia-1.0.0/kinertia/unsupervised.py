import numpy as np

def euclidian_distance(x1, x2):
    return np.sqrt(np.sum((x1-x2)**2))

#K-Means Clustering
class KMeans:
    
    def __init__(self, k=5, max_iters = 100):
        self.k = k
        self.max_iters = max_iters
        self.clusters = [[] for i in range(self.k)]
        self.centroids = []

    
    def predict(self, X):
        '''predicts the data and classify in the form of clusters'''
        self.X = X
        self.n_samples, self.n_features = X.shape
        random_sample_idx = np.random.choice(self.n_samples, self.k, replace = False)
        self.centroids = [self.X[idx] for idx in random_sample_idx]

        for _ in range(self.max_iters):
            #create clusters
            self.clusters = self.create_cluster(self.centroids)
            #update centroids
            centroid_old = self.centroids
            self.centroids = self.get_centroids(self.clusters)
            #check if converged
            if self.is_converged(centroid_old, self.centroids):
                break
        
        return self.get_cluster_labels(self.clusters)
    
    def get_cluster_labels(self, clusters):
        labels = np.empty(self.n_samples)
        for cluster_idx, cluster in enumerate(clusters):
            for sample_idx in cluster:
                labels[sample_idx] = cluster_idx
        return labels
    
    def create_cluster(self, centroids):
        clusters = [[] for i in range(self.k)]
        for idx,point in enumerate(self.X):
            centroid_idx = self.closest_centroid(point,centroids)
            clusters[centroid_idx].append(idx)
    
        return clusters
    
    def closest_centroid(self, data_point,centroids):
        distance = [euclidian_distance(data_point, centroid) for centroid in centroids]
        short_distance = np.argmin(distance)
        return short_distance

    def get_centroids(self, clusters):
        centroids = np.zeros((self.k , self.n_features))
        for cluster_idx , cluster in enumerate(clusters):
            cluster_mean = np.mean(self.X[cluster], axis = 0)
            centroids[cluster_idx] = cluster_mean
        
        return centroids

    def is_converged(self, old_centroids, new_centroids):
        distance = [euclidian_distance(old_centroids, new_centroids) for _ in range(self.k)]
        return sum(distance) == 0