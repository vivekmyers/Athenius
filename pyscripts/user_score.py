import numpy as np
import matplotlib.pyplot as plt
import mpld3
import sys
import data_loader

# TODO(nikhil): will be provided by nikhil
# senate_centroids_d = [[0,0]]*34
# senate_centroids_r = [[0,0]]*37
# house_centroids_d = [[0,0]]*99
# house_centroids_r = [[0,0]]*103

arr_s, reps_s, bills_s = data_loader.senate_records()
arr_h, reps_h, bills_h = data_loader.house_records()

def nominateScoreFromSinglePoint(arr, reps, centroid, vote):
    """
    arr: <num reps> x <num bills> matrix
    reps: dict of reps
    centroid: coords of question in reps-basis
    vote: 1 for yea, -1 for nay
    """
    ns = np.zeros([arr.shape[1], 3])
    num_select = 10
    for i in sorted([x for x in range(arr.shape[1])], key=lambda k: np.linalg.norm(centroid - arr[:, k]))[:num_select]:
        for j in range(arr.shape[0]):
            if arr[j][i] == vote:
                ns[i][0] += float(reps[j][1])
                ns[i][1] += float(reps[j][2])
                ns[i][2] += 1
    sums = [0, 0, 0]
    for i in range(num_select):
        sums[0] += ns[i][0]
        sums[1] += ns[i][1]
        sums[2] += ns[i][2]
    return sums

def nominateScoreFromPoints(arr, reps, centroids, votes):
    """
    arr: <num reps> x <num bills> matrix
    reps: dict of reps
    centroids: list of coords of question in reps-basis
    votes: list of 1 for yea, -1 for nay
    """
    sums = [0, 0, 0]
    for i in range(len(centroids)):
        single = nominateScoreFromSinglePoint(arr, reps, centroids[i], votes[i])
        sums[0] += single[0]
        sums[1] += single[1]
        sums[2] += single[2]
    return sums

def nominateScore(votes):
    """Predict user's nominate score based on their responses to the questions."""
    overallsums = [0,0,0]
    votefiles = ["senate_votes_d.npy", "senate_votes_r.npy", "house_votes_d.npy", "house_votes_r.npy"]
    centroidfiles = ["senate_centroids_d.npy", "senate_centroids_r.npy", "house_centroids_d.npy", "house_centroids_r.npy"]
    for i in range(4):
        arr, reps, bills = np.load(votefiles[i])
        subscore = nominateScoreFromPoints(arr, reps, np.load(centroidfiles[i]), votes[i*4:(i+1)*4])
        overallsums[0] += subscore[0]
        overallsums[1] += subscore[1]
        overallsums[2] += subscore[2]
    return [overallsums[0]/overallsums[2], overallsums[1]/overallsums[2]]

def nearestNeighbors(votes, m=2, n=1):
    """Find closest m members of senate followed by closest n members of house, and save plots."""
    score = nominateScore(votes)
    senatereps = reps_s
    housereps = reps_h

    # plots
    fig = plt.figure()
    allreps = np.concatenate((senatereps, housereps))
    x = [float(rep[1]) for rep in allreps]
    y = [float(rep[2]) for rep in allreps]
    names = [rep[0] for rep in allreps]
    c = [("red" if rep[0][-5] == "R" else "blue") for rep in allreps]
    x.append(score[0])
    y.append(score[1])
    c.append("green")

    norm = plt.Normalize(1,4)

    fig,ax = plt.subplots()
    sc = plt.scatter(x,y,c=c, s=100, norm=norm)

    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(ind):
        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))), 
                               " ".join([names[n] for n in ind["ind"]]))
        annot.set_text(text)
        annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
        annot.get_bbox_patch().set_alpha(0.4)

    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)

    mpld3.save_html(fig, "../public/nominateplot.html")

    dists = []
    indices = list(range(len(senatereps)))
    for i in range(len(senatereps)):
        dists.append((float(senatereps[i][1])-score[0])**2 + (float(senatereps[i][2])-score[1])**2)
    ret = [senatereps[index] for _, index in sorted(zip(dists, indices))][:m]

    dists = []
    indices = list(range(len(housereps)))
    for i in range(len(housereps)):
        dists.append((float(housereps[i][1])-score[0])**2 + (float(housereps[i][2])-score[1])**2)
    ret2 = [housereps[index] for _, index in sorted(zip(dists, indices))][:n]    

    return [ret, ret2]

def getBillKey(bill, isHouse):
    if isHouse: return 10000*int(bill["congress"]) + 1000*int(bill["session"][0]) + int(bill["rollcall-num"])
    else: return 10000*int(bill["congress"]) + 1000*int(bill["session"]) + int(bill["vote_number"])
    
def getVote(rep_name, bill_idx, isHouse):
    if isHouse:
        rep_idx = None
        for i in range(len(reps_h)):
            if(reps_h[i][0] == rep_name):
                rep_idx = i
                break
        if(rep_idx == None): return 0
        return arr_h[rep_idx][bill_idx]
    else:
        rep_idx = None
        for i in range(len(reps_s)):
            if(reps_s[i][0] == rep_name):
                rep_idx = i
                break
        if(rep_idx == None): return 0
        return arr_h[rep_idx][bill_idx]

def votingHistory(votes, name, isHouse):
    SNN, HNN = nearestNeighbors(votes, 5, 5)
    results = []
    if not isHouse:
        for bill_idx in range(len(bills_s)):
            committee = [getVote(sen[0], bill_idx, False) for sen in SNN]
            repvote = getVote(name, bill_idx, False)
            committeevote = sum(committee)
            if(committeevote >= 1): committeevote = 1
            if(committeevote <= -1): committeevote = -1
            if(repvote and committeevote != 0): results.append([bills_s[bill_idx], committeevote, repvote])
            if(repvote and committeevote != 0): results.append([bills_s[bill_idx], committeevote, repvote])
    else:
        for bill_idx in range(len(bills_h)):
            committee = [getVote(rep[0], bill_idx, False) for rep in HNN]
            repvote = getVote(name, bill_idx, False)
            committeevote = sum(committee)
            if(committeevote >= 1): committeevote = 1
            if(committeevote <= -1): committeevote = -1
            if(repvote and committeevote != 0): results.append([bills_h[bill_idx], committeevote, repvote])
            if(repvote and committeevote != 0): results.append([bills_h[bill_idx], committeevote, repvote])
    return results