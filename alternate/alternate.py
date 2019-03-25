from glob import glob
from PIL import Image
from PIL import ImageFilter
from os import path
import random
import numpy as np
import skimage

in_dir = "/data"
out_dir = "/data_alt"

MIN_CROP = .1
MAX_CROP = .3

MIN_ROTATE = 2
MAX_ROTATE = 30

MIN_L_BRIGHTNESS = 0.3
MAX_L_BRIGHTNESS = 0.80
MIN_H_BRIGHTNESS = 1.20
MAX_H_BRIGHTNESS = 1.7

random.seed(42)

LIMIT = 100
LIMITED = False


def name_from_filename(f):
    return ''.join(f.split('.')[:-1])


def alternate(name, op):
    def alt(image, fn):
        i = op(image)
        f = name_from_filename(fn.replace(in_dir + "/", ''))
        i.save(path.join(out_dir, '{}_{}.png'.format(f, name)), format='PNG')

    return alt


def crop(image):
    x, y = image.size
    x_cr_1 = x * random.uniform(MIN_CROP, MAX_CROP)
    x_cr_2 = x * random.uniform(MIN_CROP, MAX_CROP)
    y_cr_1 = y * random.uniform(MIN_CROP, MAX_CROP)
    y_cr_2 = y * random.uniform(MIN_CROP, MAX_CROP)
    return image.crop((x_cr_1, y_cr_1, x - x_cr_2, y - y_cr_2))


def rotate(image):
    return image.rotate(random.choice([1, -1]) *
                        random.uniform(MIN_ROTATE, MAX_ROTATE))


def original(image):
    return image


def brightness(image):
    br = random.choice([1, -1])
    if br == 1:
        f = random.uniform(MIN_H_BRIGHTNESS, MAX_H_BRIGHTNESS)
    else:
        f = random.uniform(MIN_L_BRIGHTNESS, MAX_L_BRIGHTNESS)
    return image.point(lambda p: p * f)


def blur(image):
    return image.filter(ImageFilter.GaussianBlur(2))


def noise(image):
    col, row = image.size
    ch = len(image.getbands())
    mean = 0.0
    sigma = 0.01
    # noise = np.clip(np.random.normal(mean, sigma, (row, col, ch)), -5, 5)
    noise = np.random.normal(mean, sigma, (row, col, ch))
    return Image.fromarray((np.uint8(np.array(image) + noise)))


def noise_sci(image):
    # var
    return Image.fromarray(
        skimage.img_as_ubyte(
            skimage.util.random_noise(np.uint8(image),
                                      mode='gaussian',
                                      seed=42,
                                      # var=0.01,
                                      clip=True)))


if __name__ == '__main__':
    ops = [
        alternate("original", original),
        alternate("crop", crop),
        alternate("rotate", rotate),
        alternate("brightness", brightness),
        alternate("blur", blur),
        alternate("noise", noise_sci),
        # alternate("noise2", noise),
    ]
    c = 0
    g = glob(path.join(in_dir, "*"))
    l = len(g)
    for i in g:
        image = Image.open(i)
        image = image.convert('RGB')
        for op in ops:
            op(image, i)
        c += 1
        print("\r{}/{}".format(c, l), end="", flush=True)
        if LIMITED and c > LIMIT:
            break
