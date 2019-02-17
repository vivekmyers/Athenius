import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE, MDS
from sklearn.decomposition import PCA
import numpy as np
import math
import os

#set flags
#republican = False
republican = True
senate = False
#senate = True
num_clust = 4

begstr = ""
endstr  = ""

if(republican):
	endstr = "r"
else:
	endstr = "d"

if(senate):
	begstr = "senate"
else:
	begstr = "house"

arr, reps, bills = np.load(begstr + "_votes_" + endstr + ".npy")
print(arr.shape)
print(arr.T[0].shape)
print(reps)
print(len(bills))
print(bills[0].keys())
print(bills[0].get("vote_title"))

distances = np.zeros((arr.shape[1], arr.shape[1]))
for i in range(arr.shape[1]):
    for j in range(arr.shape[1]):
        distances[i][j] = np.sum(np.absolute(arr[:, i] - arr[:, j]))

model = MDS(n_components=3, dissimilarity='precomputed', random_state=1, n_jobs=4)
out = model.fit_transform(distances)
"""
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.title('Clustering of Senate Bills')
ax.set_axis_off()
ax.scatter(out[:, 0], out[:, 1], out[:, 2])
plt.show()
"""
nc = range(1,20)
kmeans = [KMeans(n_clusters=i) for i in nc]
score = [kmeans[i].fit(arr.T).score(arr.T) for i in range(len(kmeans))]
"""
plt.plot(nc, score)
plt.show()
"""

centers = KMeans(n_clusters=num_clust).fit_predict(arr.T)

mask = np.array(['(D' in x for x in reps])
print(mask.shape)

print(centers)

for i in range(num_clust):
	print(f'{"-" * 20} Cluster {i} {"-" * 20}')
	for j in range(len(bills)):
		if(i == centers[j]):
			print(bills[j].get("vote_title"))

print(f'{"-" * 20} CENTERS CENTERS CENTERS {i} {"-" * 20}')

ctz = KMeans(n_clusters=num_clust).fit(arr.T)
print(ctz.cluster_centers_)

cc = np.empty([num_clust, arr.T[0].shape[0]])

q = 0
for i in ctz.cluster_centers_:
	print()
	print()
	print()
	print(f'{"-" * 20} A Center Follows {"-" * 20}')
	print(i)
	mindist = math.inf
	minbill = None
	for j in range(len(bills)):
		if "QUORUM" in bills[j].get("vote-type") or "JOURNAL" in bills[j].get("legis-num"):
			continue
		if bills[j].get("vote-desc"):
			if "Adopting rules" in bills[j].get("vote-desc") or "Midnight" in bills[j].get("vote-desc"):
				continue
		if bills[j].get("vote-type"):
			if "RECORDED VOTE" in bills[j].get("vote-type"):
				continue
		s = 0
		for k in range(arr.T[j].shape[0]):
			s += abs(i[k] - arr.T[j][k])

		if(s<mindist):
			mindist = s
			minbill = j

	print(bills[minbill])
	print(arr.T[minbill])
	cc[q] = arr.T[minbill]
	#print(mindist)
	#print(np.absolute(arr.T[minbill] - i))
	#print(np.sum(np.absolute(arr.T[minbill] - i)))
	q += 1

print(cc)

np.save(begstr + "_centroids_" + endstr, cc)
"""
for i in range(num_clust):
    print(f'{"-" * 20} Cluster {i} {"-" * 20}')
    for bill, vec in zip(bills[centers == i][:20], arr[:, centers == i].T):
        dem = np.dot(vec, mask)
        rep = np.dot(vec, ~mask)
        if rep > dem:
            print('(Rep Supported ' +str(rep-dem)+' )', end=' ')
        else:
            print('(Dem Supported ' + str(dem-rep) + ' )', end=' ')
        print(f"{bill['vote_title'][:50]}")


    print()
"""
"""
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.title('Clustering of Senate Bills')
ax.set_axis_off()
for i in range(num_clust):
    ax.scatter(out[centers == i, 0], out[centers == i, 1], out[centers == i, 2])
plt.show()
"""