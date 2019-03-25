import imagehash
import json
from sklearn.metrics.pairwise import cosine_similarity


def norm_name(name):
    return name.replace("/data/", '').replace(".png", '').split('_')


def binarize(v):
    return [0 if i < .5 else 1 for i in v]


def binarize_avg(v):
    avg = sum(v) / len(v)
    return [0 if i < avg else 1 for i in v]


def max_squash(v, rate=2):
    l = len(v)
    tmp = []
    for i in range(l // rate):
        tmp.append(max(v[rate * i:rate * (i + 1)]))
    return tmp


def avg_squash(v, rate=2):
    l = len(v)
    tmp = []
    for i in range(l // rate):
        t = v[rate * i:rate * (i + 1)]
        avg = sum(t) / len(t)
        tmp.append(1 if avg > .5 else 0)
    return tmp


if __name__ == '__main__':
    vectors = []
    hashes = {}
    for l in open("/features/features.json"):
        d = json.loads(l)
        h = {
            "b": binarize(d[1]),
            "ba": binarize_avg(d[1]),
        }
        vectors.append(d)
        h.update({
            "mb2": max_squash(h["b"], 2),
            "mb4": max_squash(h["b"], 4),
            "mb8": max_squash(h["b"], 8),
            "mb16": max_squash(h["b"], 16),
            "mb32": max_squash(h["b"], 32),
            "mb64": max_squash(h["b"], 64),
            "mba2": max_squash(h["ba"], 2),
            "mba4": max_squash(h["ba"], 4),
            "mba8": max_squash(h["ba"], 8),
            "mba16": max_squash(h["ba"], 16),
            "mba32": max_squash(h["ba"], 32),
            "mba64": max_squash(h["ba"], 64),
            "mab2": avg_squash(h["b"], 2),
            "mab4": avg_squash(h["b"], 4),
            "mab8": avg_squash(h["b"], 8),
            "mab16": avg_squash(h["b"], 16),
            "mab32": avg_squash(h["b"], 32),
            "mab64": avg_squash(h["b"], 64),
            "maba2": avg_squash(h["ba"], 2),
            "maba4": avg_squash(h["ba"], 4),
            "maba8": avg_squash(h["ba"], 8),
            "maba16": avg_squash(h["ba"], 16),
            "maba32": avg_squash(h["ba"], 32),
            "maba64": avg_squash(h["ba"], 64),
        })
        nn = norm_name(d[0])
        if nn[0] not in hashes:
            hashes[nn[0]] = {}
        hashes[nn[0]][nn[1]] = h
    r = {}
    for p, v in enumerate(vectors):
        nn = norm_name(v[0])
        if nn[0] in r:
            continue
        elif nn[1] == 'original':
            r[nn[0]] = {'crop': None, 'rotate': None, 'noise': None,
                        'blur': None, 'brightness': None}
            tmp = []
            for v2 in vectors:
                nn2 = norm_name(v2[0])
                # if nn == nn2:
                #     continue
                # tmp.append((nn2, cosine_similarity([v[1]], [v2[1]])[0][0]))
            for i, v in enumerate(
                    sorted(tmp, key=lambda x: x[1], reverse=True)):
                if v[0][0] == nn[0] and v[0][1] != "original":
                    r[nn[0]][v[0][1]] = i
    # json.dump(r, open("/features/vect_eval.json", "w"))
    hr = {}
    for im, h in hashes.items():
        for t, h in h.items():
            for hn, h in h.items():
                if hn == "original":
                    continue
                if hn not in hr:
                    hr[hn] = {}
                hr[hn][im] = {'crop': False, 'rotate': False, 'noise':
                    False, 'blur': False, 'brightness': False}
                if hashes[im]["original"][hn] == h:
                    hr[hn][im][t] = True
    json.dump(hr, open("/features/vect_hash_eval.json", "w"))
