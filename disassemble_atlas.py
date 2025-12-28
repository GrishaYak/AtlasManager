from sys import argv
from PIL import Image
from os import path, listdir, mkdir
import numpy as np
import xml.etree.ElementTree as et

def dissasemble_atlas(texture_fullname, description_fullname, save_on_disk=False, out_dir=None):
    if (save_on_disk and out_dir is None):
        out_dir = path.dirname(path.realpath(__file__)) + '/images/'
    
    if not path.exists(out_dir):
        mkdir(out_dir)

    tree = et.parse(description_fullname)
    rt = tree.getroot()
    regions = rt.find('Regions')
    res = {}
    atlas_img = Image.open(texture_fullname)
    for region in regions:
        atr = region.attrib
        name = atr['name']
        x = int(atr['x'])
        y = int(atr['y'])
        width = int(atr['width'])
        height = int(atr['height'])
        region = atlas_img.crop((x, y, x + width, y + height))
        if save_on_disk:
            region.save(out_dir + name + '.png')
            continue
        res[name] = region
    atlas_img.close()
    return res


if __name__ == '__main__':
    print('\n')
    print('-'*10)
    if len(argv) == 1:
        args = []
        with open("input.txt") as f:
            for i in range(2):
                args.append(f.readline().rstrip())
    else:
        args = argv[1:]
    
    if len(args) == 2:
        dissasemble_atlas(*args, save_on_disk=True)
    else:
        raise Exception('Wrong amount of arguments given!')