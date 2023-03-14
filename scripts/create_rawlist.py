from util.FileKey import *
import glob
import os

configs=snakemake.input[0]
ignored_keyslist = os.path.join(configs, 'ignore_keys.keylist')
if os.path.isfile(ignored_keyslist):
    with open(ignored_keyslist, 'r') as f:
        ignore_keys = f.read().splitlines()
else:
    print("no ignore_keys.keylist file found")

keypart = snakemake.wildcards.keypart
setup = snakemake.params.setup

key = FileKey.parse_keypart(keypart)

item_list = []
for item in key:
    if "_" in item:
        item = item.split("_")
    if isinstance(item, list):
        item_list.append(item)
    else:
        item_list.append([item])

filekeys=[]
for i in item_list[0]:
    for j in item_list[1]:
        for k in item_list[2]:
            for l in item_list[3]:
                for m in item_list[4]:
                    filekeys.append(FileKey(i,j,k,l,m))

keys = []
for key in filekeys:
    fn_glob_pattern = key.get_path_from_filekey(get_pattern_tier_daq(setup))[0]
    files = glob.glob(fn_glob_pattern)

    for f in files:
        key = FileKey.get_filekey_from_pattern(f,get_pattern_tier_daq(setup))
        if key.name in ignore_keys:
            pass
        else:
            keys.append(key.name)

with open(snakemake.output[0], 'w') as f:
    for key in keys:
        f.write(f"{key}\n")