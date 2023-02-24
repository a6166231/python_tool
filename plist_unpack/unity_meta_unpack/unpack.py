#!python
import os,sys
from PIL import Image
reload(sys)
sys.setdefaultencoding('utf-8')

os.chdir(os.path.dirname(os.path.abspath(__file__)))
DEEP_SPACE = 2
SPF_SHEET_KEY = 'sprites:'
V_SPF_KEYS = ['name','x','y','width','height']
SPF_DICT_KEYS = {}

for key in V_SPF_KEYS:
    SPF_DICT_KEYS[key] = key

def enumfiles(path, dest):
    files = os.listdir(os.path.join(dir, path))
    for f in files:
        subpath = os.path.join(path, f)
        abspath = os.path.join(dir, subpath)

        if (os.path.isfile(abspath) and str.lower(os.path.splitext(abspath)[1]) == '.meta'):
            dest.append(subpath.replace('.meta', ''))
        elif (os.path.isdir(abspath)):
            if (f[0] == '.'):
                pass
            else:
                enumfiles(subpath, dest)

def parse_spf_sheet_ary(meta_filename):
    spf_sheet_ary = []
    f = open(meta_filename).read()
    sprites = f.split('sprites')
    if len(sprites) != 2:
        return spf_sheet_ary

    fsplit = sprites[1].split('    - serializedVersion:')

    for spf in fsplit:
        s_keys_values = spf.split('\n')
        spf_dict = {}
        if len(s_keys_values) < SPF_DICT_KEYS.__len__():
            continue
        for s in s_keys_values:
            key_value = s.lstrip(' ').split(':')
            
            # print(key_value)
            # print('-------------')
            if SPF_DICT_KEYS.get(key_value[0]):
                if len(key_value) > 2:
                    spf_dict[key_value[0]] = (':'.join(key_value[1:])).lstrip(' ')
                else:
                    spf_dict[key_value[0]] = key_value[1].lstrip(' ')
            if spf_dict.__len__() == SPF_DICT_KEYS.__len__():
                spf_sheet_ary.append(spf_dict)
                break
            
    # print(spf_sheet_ary)
    # print('result -----: ',len(spf_sheet_ary))
    return spf_sheet_ary

def gen_png_from_meta(meta_filename, png_filename):
    spf_sheet_ary = parse_spf_sheet_ary(os.path.join(dir, meta_filename))
    file_path = dir + '/output/' + meta_filename.replace('.png.meta', '')
    big_image = Image.open(os.path.join(dir, png_filename))
    for spf in spf_sheet_ary:
        width = int(spf['width'])
        height = int(spf['height'])
        x = int(spf['x'])
        y = big_image.height - int(spf['y']) - height

        box = (x, y, x + width, y + height)
        rect_on_big = big_image.crop(box)
        sizelist = [width,height]
        result_image = Image.new('RGBA', sizelist, (0,0,0,0))
        result_image.paste(rect_on_big,(0,0))

        if not os.path.isdir(file_path):
            os.makedirs(file_path)
        outfile = (file_path + '/' + spf['name']+ '.png')
        result_image.save(outfile)
        # print(outfile + ' generated')
    print(file_path + ' generated')

dir = raw_input('input files path:')

if len(dir) == 0:
    dir = '.'

dest = []
if os.path.isdir(dir):
    enumfiles('.', dest)

total = 0
for filename in dest:
    meta_filename = filename + '.meta'
    png_filename = filename
    if (os.path.isfile(os.path.join(dir, meta_filename)) and os.path.isfile(os.path.join(dir, png_filename))):
        gen_png_from_meta( meta_filename, png_filename )
        total+=1
    else:
        print("make sure you have boith meta and png files in the same directory")
print('\n')
print('total unpack :' + str(total))
os.system('pause')