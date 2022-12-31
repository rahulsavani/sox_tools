#! /usr/bin/env python3

"""
Script for case where (a subset of) samples in a folder have their bpm in the filename

The script uses a regex to put files into corresponding bpm (or 'NO_BPM') subdirs
"""

import os
import re
import glob
import argparse 
import shutil

def extract_bpm_from_fname(fname):
    found = regex.search(fname)

    if found is None:
        return
    else:
        tmp1 = found.group(0)
        tmp2 = tmp1.replace('bpm.wav','')
        tmp2 = tmp2.replace('_','')
        tmp2 = '%03d' % int(tmp2)
        return tmp2

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Split by bpm into subdirs')
    parser.add_argument('--target_dir', '-d', required=True)
    args = parser.parse_args()
    target_dir = args.target_dir 

    # Example fname with bpm: InTheAir_Dry_keyFmin_70bpm.wav
    regex = re.compile('_[0-9]+bpm\.wav')

    for src_full_path in glob.glob(target_dir + '/*.wav'):

        fname = os.path.basename(src_full_path) 

        found = extract_bpm_from_fname(fname)

        if found is None:
            print(fname, 'NO_BPM')
            subdir = os.path.join(target_dir, 'NO_BPM')
        else:
            print(fname, found)
            subdir = os.path.join(target_dir, found)

        # Create subdir if it doesn't exist
        os.makedirs(subdir, exist_ok=True)

        # Now move file to the appropriate subdir
        destination = os.path.join(subdir, fname)
        shutil.move(src_full_path, destination)
