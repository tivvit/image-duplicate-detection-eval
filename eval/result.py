import json

for fin, fout, fpos, fex in [
    ("/features/vect_eval.json", "/features/vect_result.json",
     "/features/vect_eval.json", "/features/vect_hash_eval.json"),
    ("/features/hash_avh_eval.json", "/features/hash_avh_result.json",
     "/features/hash_avh_pos_eval.json", "/features/hash_avh_exact_eval.json"),
    ("/features/hash_ph_eval.json", "/features/hash_ph_result.json",
     "/features/hash_ph_pos_eval.json", "/features/hash_ph_exact_eval.json"),
    ("/features/hash_dh_eval.json", "/features/hash_dh_result.json",
     "/features/hash_dh_pos_eval.json", "/features/hash_dh_exact_eval.json"),
    ("/features/hash_wh_eval.json", "/features/hash_wh_result.json",
     "/features/hash_wh_pos_eval.json", "/features/hash_wh_exact_eval.json"),
]:
    d = json.load(open(fin, "r"))
    pos = json.load(open(fpos, "r"))

    res = {'crop': 0, 'rotate': 0, 'noise': 0, 'blur': 0, 'brightness': 0}
    a = 0
    l = len(d)

    for n, r in d.items():
        a += (1 + 2 + 3 + 4 + 5) / sum(r.values())
        for i in r:
            res[i] += pos[n][i]

    r = {
        "all": a / l,
    }

    for i in res:
        r[i] = res[i] / l

    ex = json.load(open(fex, "r"))
    for t in ex:
        cnt = 0
        pos = {'crop': 0, 'rotate': 0, 'noise': 0, 'blur': 0, 'brightness': 0}
        for k, v in ex[t].items():
            cnt += 1
            for cl, i in v.items():
                if cl == "original":
                    continue
                if i:
                    pos[cl] += 1
        for k, v in pos.items():
            r[t + "_" + k + "_ex"] = v / cnt
        r[t + "_all_ex"] = sum(pos.values()) / (cnt * 5)

    json.dump(r, open(fout, "w"))
