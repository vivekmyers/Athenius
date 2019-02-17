import numpy as np

# TODO(nikhil): will be provided by nikhil
# senate_centroids_d = [[0,0]]*34
# senate_centroids_r = [[0,0]]*37
# house_centroids_d = [[0,0]]*99
# house_centroids_r = [[0,0]]*103

def nominateScoreFromSinglePoint(arr, reps, centroid, vote):
    """
    arr: <num reps> x <num bills> matrix
    reps: dict of reps
    centroid: coords of question in reps-basis
    vote: 1 for yea, -1 for nay
    """
    ns = []
    dists = []
    for i in range(len(arr.shape[1])):
        count = 0
        ns.append([0, 0])
        for j in range(len(arr.shape[0])):
            if arr[j][i] == vote:
                ns[i][0] += reps[j][1]
                ns[i][1] += reps[j][2]
                dists.append(np.linalg.norm(centroid - arr[:, i]))
        ns[i][0] /= count
        ns[i][1] /= count
    ns = np.array([n for _, n in sorted(zip(dists, ns))])
    k = 5
    avg = [0, 0]
    for i in range(k):
        avg[0] += ns[i][0]
        avg[1] += ns[i][1]
    avg[0] /= k
    avg[1] /= k
    return avg

def nominateScoreFromPoints(arr, reps, centroids, votes):
    """
    arr: <num reps> x <num bills> matrix
    reps: dict of reps
    centroids: list of coords of question in reps-basis
    votes: list of 1 for yea, -1 for nay
    """
    avg = [0, 0]
    for i in range(len(centroids)):
        single = nominateScoreFromSinglePoint(arr, reps, centroids[i], votes[i])
        avg[0] += single[0]
        avg[1] += single[1]
    avg[0] /= i
    avg[1] /= i
    return avg

def nominateScore(votes):
    """Predict user's nominate score based on their responses to the questions."""
    overall_avg = [0,0]
    votefiles = ["senate_votes_d.npy", "senate_votes_r.npy", "house_votes_d.npy", "house_votes_r.npy"]
    centroidfiles = ["senate_centroids_d.npy", "senate_centroids_r.npy", "house_centroids_d.npy", "house_centroids_r.npy"]
    for i in range(4):
        arr, reps, bills = np.load(votefiles[i])
        subscore = nominateScoreFromPoints(arr, reps, np.load(centroidfiles[i]), votes[i*5:(i+1)*5])
        overall_avg[0] += subscore[0]
        overall_avg[1] += subscore[1]
    overall_avg[0] /= 4
    overall_avg[1] /= 4
    return overall_avg

def nearestNeighbors(votes, m=2, n=1):
    """Find closest m members of senate followed by closest n members of house."""
    score = nominateScore(votes)
    _, senatereps, _ = data_loader.senate_records()
    _, housereps, _ = data_loader.house_records()
    ret = []
    dists = []
    for i in range(len(senatereps)):
        dists.append((senatereps[i][1]-score[0])**2 + (senatereps[i][2]-score[1])**2)
    ret += [rep for _, rep in sorted(zip(dists, senatereps))][:m]
    dists = []
    for i in range(len(housereps)):
        dists.append((housereps[i][1]-score[0])**2 + (housereps[i][2]-score[1])**2)
    ret += [rep for _, rep in sorted(zip(dists, senatereps))][:n]
    return ret