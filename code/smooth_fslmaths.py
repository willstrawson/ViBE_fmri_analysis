#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 11:41:59 2020

@author: willstrawson
"""

import subprocess
import sys

print (sys.argv[0]) # prints python_script.py
print (sys.argv[1]) # prints var1
print (sys.argv[2]) # prints var2

# Script to smooth a nifti using fslmaths (not SUSAN) - currently using this to 
# smooth a mask so simplicity is prefered. 

def smooth(inp, kernal):
    # Ensure input are lists of images, so that multiple can be smoothed at once
    if type(inp) != list:
        inp = list(inp)
        
    #
    for i in inp:
        # define output name from input
        o = inp.replace('.nii', '_smooth_{}mm.nii'.format(kernal))
        print ('smoothing: {}'.format(i))
        print ('output: {}'.format(o))
        # run the smoothing operation using the input, output and 
        subprocess.call(['fslmaths', i, '-kernel', 'gauss', kernal, '-fmean', o])

# enbale script to be run from command line
if __name__ == '__main__':
    smooth()
    

