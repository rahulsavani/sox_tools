#! /usr/bin/env python3

import sys
import os
import glob
from subprocess import PIPE, Popen
import argparse 

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

def bar_length(bpm):
    return 4*60.0/bpm

def trim(source, dest, bpm, bar_number):

    bl = bar_length(bpm) 
    start = (bar_number-1)*bl
    # end = bar_number*bl
    # end = '3.428571'
    # print('bar_length for bpm %s is %s' % (bpm, bar_length(bpm)))
    # print('start: %s, end: %s' % (start, end))
    
    # sox 4bars/$i -b 16 $i rate 44100 trim 0 00:00:03.428571

    # remix 1: only take left channel (in case original was stereo
    # norm -0.1: normalise to -0.1 db
    # -b 16: convert to 16 bit if needed
    cmd_str = 'sox %s -b 16 %s norm -0.1 remix 1 trim 00:00:0%s 00:00:0%s' % (source, dest, start, bl)
    print(cmd_str)
    os.system(cmd_str)

def found_length(src):
    exec_str =  'soxi -D %s' % src
    found_length = float(cmdline(exec_str))
    return(found_length)

def get_n_bars(src, bpm):
    fl = found_length(src)
    bl = bar_length(bpm)
    n_bars = fl/bl
    import math
    n_bars_ceil = math.ceil(n_bars)
    print(n_bars,n_bars_ceil)
    return n_bars_ceil

def process(src,bpm):

    tmp = src.replace('.wav','')
    os.makedirs(tmp)

    nb = get_n_bars(src,bpm)

    for i in range(nb):
        j = i+1

        dest = '%s_b%02d.wav' % (tmp, j)
        dest = os.path.join(tmp,dest)

        trim(src, dest, bpm, bar_number=j)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Extract bars by length implied by bpm')
    parser.add_argument('--bpm', '-b', required=True, choices=['140','170'])
    args = parser.parse_args()
    bpm = int(args.bpm)

    for src in glob.glob('*.wav'):
        process(src,bpm)
