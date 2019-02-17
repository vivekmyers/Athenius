import numpy as np

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
        for j in range(len(arr.shape[0])):
            if arr[j][i] == vote:
                ns.append([reps[j][1], reps[j][2]])
                dists.append(np.linalg.norm(centroid - arr[:, i]))
    ns = np.array([n for _, n in sorted(zip(dists, ns))])
    k = 5
    avg = [0, 0]
    for i in range(k):
        avg[0] += ns[i][0]
        avg[1] += ns[i][1]
    avg[0] /= k
    avg[1] /= k
    return avg

def nominateScoreFromAnswers(arr, reps, centroids, votes):
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