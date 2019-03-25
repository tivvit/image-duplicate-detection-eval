import imagehash
from glob import glob
from PIL import Image
import json

if __name__ == '__main__':
    g = glob("/data/*")
    l = len(g)
    with open("/out/hashes.json", "w") as f:
        for i in g:
            print(i)
            img = Image.open(i)
            avh = imagehash.average_hash(img)
            ph = imagehash.phash(img)
            dh = imagehash.dhash(img)
            wh = imagehash.whash(img)
            f.write(json.dumps({
                "f": i,
                "avh": str(avh),
                "ph": str(ph),
                "dh": str(dh),
                "wh": str(wh),
            }) + "\n")
