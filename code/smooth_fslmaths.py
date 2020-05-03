#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 11:41:59 2020

@author: willstrawson
"""

import subprocess
import sys
import glob



# Script to smooth a nifti using fslmaths (not SUSAN) - currently using this to 
# smooth a mask so simplicity is prefered. 

def smooth(inp, kernal):
    # Ensure input are lists of images, so that multiple can be smoothed at once
    if type(inp) != list:
        inp = list(inp)
        
    #
    for i in inp:
        # define output name from input
        o = i.replace('.nii.gz', '_smooth_{}mm.nii.gz'.format(kernal))
        print ('smoothing: {}'.format(i))
        print ('output: {}'.format(o))
        # run the smoothing operation using the input, output and 
        subprocess.call(['fslmaths', i, '-kernel', 'gauss', str(kernal), '-fmean', o])


# define arguments
inp = glob.glob('/its/home/ws231/Desktop/cisc1/projects/critchley_vibe/masks/task_cluster_*.nii.gz')
kernal = 5

#run function 
smooth(inp, kernal)
