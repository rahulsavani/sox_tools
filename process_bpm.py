#! /usr/bin/env python3

import os
import glob
from subprocess import PIPE, Popen
import argparse 

###############################################################################
###############################################################################

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

###############################################################################
###############################################################################

def get_new_name(name):

    # new_name = '%03d.wav' % (START_INDEX)
    # START_INDEX += 1

    # new_name = '%03d.wav' % (i+START_INDEX)

    # exec_str =  'soxi -D %s' % name
    # found_length = float(cmdline(exec_str))
    # print('found_length: %f' % found_length)

    # name includes sdir, e.g., SDIR/FNAME.wav
    new_name = name.split('/')[1]

    if n_fields_to_drop > 0:
        new_name = new_name.split('_')[:-(n_fields_to_drop)]
        new_name = '_'.join(new_name)
        new_name = new_name + '.wav'
    
    # print(new_name)
    return new_name

def call_sox(name, new_name, speed):
    # exec_str = 'sox %s %s speed %s' % (name, fname, speed)
    exec_str = 'sox %s -b 16 %s speed %s remix 1 norm -0.1' % (name, new_name, speed)
    print(exec_str)
    os.system(exec_str)

def process_given_bpm(i, name, current_bpm, target_bpm, START_INDEX):

    print(name)

    new_name = get_new_name(name)

    speed = target_bpm/float(current_bpm)

    print('speed: %f' % speed)
    
    print('=============================================')

    call_sox(name, new_name, speed)

    return START_INDEX

###############################################################################
###############################################################################

def process_found_length(n_bars, name, i=None):

    # new_name = '%03d.wav' % (i+START_INDEX)
    print(name)

    new_name = get_new_name(name)

    # Get found lenght with soxi
    exec_str =  'soxi -D %s' % name
    found_length = float(cmdline(exec_str))

    print('found_length: %f' % found_length)

    target_length = 60.0*4*n_bars/target_bpm
    print('target_length: %f' % target_length)

    speed = found_length/target_length

    print('speed: %f' % speed)
    
    print('=============================================')

    call_sox(name, new_name, speed)

###############################################################################
###############################################################################


if __name__ == '__main__':


    parser = argparse.ArgumentParser(description='Convert to target bpm')
    parser.add_argument('--target_dir', '-d', required=True)
    parser.add_argument('--type', '-t', required=True, choices=['folder_name', 'found_length'])
    parser.add_argument('--nbars', '-n')
    parser.add_argument('--bpm', '-b', required=True, choices=['70', '85', '140','170'])
    parser.add_argument('--n_fields_to_drop', '-nb', default=0)

    args = parser.parse_args()
    target_dir = args.target_dir 

    TYPE = args.type
    target_bpm = float(args.bpm)

    if TYPE == 'found_length':
        assert args.nbars is not None

    n_fields_to_drop = int(args.n_fields_to_drop)
    # n_fields_to_drop = 2 # drop e.g., _150bpm with value 1, _Aminor_150bpm with 2

    # start index is needed when one overrides the files names
    # START_INDEX = 1

    # n_bars is needed for the found length option
    # n_bars = 2 # 1
    # sdir = '%dbar' % n_bars

    if TYPE == 'folder_name':

        # Assumes current working directory
        cwd = os.getcwd()

        """
        All sub-directories must be labelled by a bpm
        """
        direcs = [d for d in os.listdir(cwd) if os.path.isdir(d)]

        print(direcs)

        START_INDEX = 1

        for sdir in direcs:
            print("Processing sdir: %s" % sdir)
            current_bpm = float(sdir)
            for i,name in enumerate(glob.glob('%s/*.wav' % sdir)):
                print("Processing:", name)
                START_INDEX = process_given_bpm(i, 
                                                name, 
                                                current_bpm, 
                                                target_bpm, 
                                                START_INDEX)

    elif TYPE == 'found_length':

        sdir = args.target_dir
        n_bars = int(args.nbars)

        for i, name in enumerate(glob.glob('%s/*.wav' % sdir)):
            process_found_length(n_bars, name, i)

    else:
    
        raise Exception('TYPE %s not recognised' % TYPE)
