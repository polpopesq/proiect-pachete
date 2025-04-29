from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def perform_clustering(data, n_clusters=3):
    scaler = StandardScaler()
    coords_scaled = scaler.fit_transform(data[['latitude', 'longitude']])
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    data['cluster'] = kmeans.fit_predict(coords_scaled)
    return data
