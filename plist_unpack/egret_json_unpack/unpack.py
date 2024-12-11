#!python
import json
import os, sys
from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(__file__)))
V_SPF_KEYS = ['x', 'y', 'w', 'h', 'offX', 'offY', 'sourceW', 'sourceH']
SPF_DICT_KEYS = {}

for key in V_SPF_KEYS:
    SPF_DICT_KEYS[key] = key


def enumfiles(path, dest):
    files = os.listdir(os.path.join(dir, path))
    for f in files:
        subpath = os.path.join(path, f)
        abspath = os.path.join(dir, subpath)

        if (os.path.isfile(abspath)
                and str.lower(os.path.splitext(abspath)[1]) == '.json'):
            dest.append(subpath.replace('.json', ''))
        elif (os.path.isdir(abspath)):
            if (f[0] == '.'):
                pass
            else:
                enumfiles(subpath, dest)


def parse_spf_sheet_ary(meta_filename):
    spf_sheet_ary = []
    f = open(meta_filename).read()
    fjson = json.loads(f)
    frames = fjson['frames']
    for k in frames:
        spf = frames[k]
        spf['name'] = k
        spf_sheet_ary.append(spf)
    return spf_sheet_ary


def gen_png_from_meta(meta_filename, png_filename):
    spf_sheet_ary = parse_spf_sheet_ary(os.path.join(dir, meta_filename))
    file_path = dir + '/output/' + meta_filename.replace('.json', '')
    big_image = Image.open(os.path.join(dir, png_filename))
    for spf in spf_sheet_ary:
        width = int(spf['w'])
        height = int(spf['h'])
        x = int(spf['x'])
        y = big_image.height - int(spf['y']) - height
        y = int(spf['y'])

        box = (x, y, x + width, y + height)
        rect_on_big = big_image.crop(box)
        sizelist = [width, height]
        result_image = Image.new('RGBA', sizelist, (0, 0, 0, 0))
        result_image.paste(rect_on_big, (0, 0))

        if not os.path.isdir(file_path):
            os.makedirs(file_path)
        fname = spf['name']
        if hidePng:
            fname = fname.replace('_png', '')
        outfile = (file_path + '/' + fname + '.png')
        result_image.save(outfile)
    print(file_path + ' generated')


dir = input('input files path:')
if len(dir) == 0:
    dir = '.'

bReplace_Png = input('hide extends suffix name [x_png.png -> x.png] ? (y/n)')

if len(bReplace_Png) == 0:
    bReplace_Png = 'y'

hidePng = bReplace_Png == 'y'

dest = []
if os.path.isdir(dir):
    enumfiles('.', dest)

total = 0
for filename in dest:
    meta_filename = filename + '.json'
    png_filename = filename + '.png'
    if (os.path.isfile(os.path.join(dir, meta_filename))
            and os.path.isfile(os.path.join(dir, png_filename))):
        gen_png_from_meta(meta_filename, png_filename)
        total += 1
print('\n')
print('total unpack :' + str(total))
os.system('pause')
