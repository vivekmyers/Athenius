import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE, MDS
from sklearn.decomposition import PCA
import numpy as np

arr, reps, bills = np.load("senate_votes.npy")
print(arr.shape)
print(reps)
print(len(bills))

distances = np.zeros((arr.shape[1], arr.shape[1]))
for i in range(arr.shape[1]):
    for j in range(arr.shape[1]):
        distances[i][j] = np.sum(np.absolute(arr[:, i] - arr[:, j]))

model = MDS(n_components=3, dissimilarity='precomputed', random_state=1, n_jobs=4)
out = model.fit_transform(distances)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.title('Clustering of Senate Bills')
ax.set_axis_off()
ax.scatter(out[:, 0], out[:, 1], out[:, 2])
plt.show()

nc = range(1,20)
kmeans = [KMeans(n_clusters=i) for i in nc]
score = [kmeans[i].fit(arr.T).score(arr.T) for i in range(len(kmeans))]
plt.plot(nc, score)
plt.show()

num_clust = 5
centers = KMeans(n_clusters=num_clust).fit_predict(arr.T)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.title('Clustering of Senate Bills')
ax.set_axis_off()
for i in range(num_clust):
    ax.scatter(out[centers == i, 0], out[centers == i, 1], out[centers == i, 2])
plt.show()
