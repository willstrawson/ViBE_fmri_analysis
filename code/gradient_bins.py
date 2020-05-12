#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 11:51:56 2020

@author: willstrawson
"""
import glob
import subprocess
import os

# Script to produce binarized and binned versions of each gradient mask 

'''
From Murphey (2019):
 This map was then divided into five-percentile bins 
 (all voxels with the value 0–5 were assigned to bin1; 6–10 1⁄4 bin 2 etc) yielding 20 bins in total. 
'''

bins = {0:5, 6:10, 11:15, 16:20, 21:25, 26:30,31:35, 36:40, 41:45, 46:50,
        51:55, 56:60, 61:65, 66:70, 71:75, 76:80, 81:85, 86:90, 91:95, 96:100}
# Read in gradients niftis
fls = glob.glob('/Users/willstrawson/Documents/PhD/Rotation_2/fMRI/gradients/g*/volume.313.*_new.nii.gz')
print ('masks to be binned: {}'.format(fls))

# Loop thought each nifti 
for i in fls:
    # loop through each percentile bin - should be 20 loops 
    for b in bins.items():
        print ('thresholding {} into the {} bin'.format(os.path.split(i)[1], b))
        #Create output name for lower thresholded imags
        outname1 = i.replace('.nii.gz', '{}.nii.gz'.format(str(b[0]).strip().replace(',','')))
        # lower threshold first i.e. 0 anything below this range
        # don't binarize or else all will get removed inthe next call!
        subprocess.call(['fslmaths', i, '-thrp', str(b[0]), outname1])
        # Create final upper threshold name
        outname2 = i.replace('.nii.gz', '{}.nii.gz'.format(str(b).strip().replace(',','')))
        # then upper threshold i.e. 0 anything above this range 
        subprocess.call(['fslmaths', outname1, '-uthrp', str(b[1]), '-bin', outname2])
        #then delete the intermediary outname1 mask 
        os.remove(outname1)
    
    
