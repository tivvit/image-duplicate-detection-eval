import imagehash
import json
from eval import norm_name

r = {}
c = ["avh", "ph", "dh", "wh"]
for i in c:
    r[i] = []

for l in open("/features/hashes.json", "r"):
    d = json.loads(l)
    n = norm_name(d["f"])
    for i in c:
        r[i].append((n, imagehash.hex_to_hash(d[i])))

for t in c:
    res = {}
    res2 = {}
    res3 = {t: {}}
    for v in r[t]:
        nn = v[0]
        if nn[0] in res:
            continue
        elif nn[1] == 'original':
            res[nn[0]] = {'crop': None, 'rotate': None, 'noise': None,
                          'blur': None, 'brightness': None}
            res2[nn[0]] = {'crop': None, 'rotate': None, 'noise': None,
                          'blur': None, 'brightness': None}
            res3[t][nn[0]] = {'crop': False, 'rotate': False, 'noise': False,
                           'blur': False, 'brightness': False}
            tmp = []
            for v2 in r[t]:
                nn2 = v2[0]
                # if nn == nn2:
                #     continue
                tmp.append((nn2, v[1] - v2[1]))
            lp = 0
            vp = 1
            vp2 = 1
            for i, v in enumerate(sorted(tmp, key=lambda x: x[1])):
                if v[1] != lp:
                    lp = v[1]
                    vp = i + 1
                    vp2 = i + 1
                if v[0][0] == nn[0] and v[0][1] != "original":
                    if lp == 0:
                        res3[t][nn[0]][v[0][1]] = True
                    res2[nn[0]][v[0][1]] = vp2
                    res[nn[0]][v[0][1]] = vp
                    vp += 1
    json.dump(res, open("/features/hash_{}_eval.json".format(t), "w"))
    json.dump(res2, open("/features/hash_{}_pos_eval.json".format(t), "w"))
    json.dump(res3, open("/features/hash_{}_exact_eval.json".format(t), "w"))
