# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 17:44:19 2020

@author: ws231
"""
#TODO: Skull strip -> smooth -> skull stip
#mask.key = cisc1 nii / mask.value = cisc2 nii
# Susan Script

import subprocess 
import os
import glob
import numpy as np
#Change this when in remote environment - change to where niftis are stores
funcdir = '/its/home/ws231/Desktop/cisc1/projects/critchley_vibe/skullstrip_smooth/'

maskdir = '/its/home/ws231/Desktop/cisc2/projects/critchley_vibe/data/derivatives/fmriprep-1.5.1/'

os.chdir(funcdir)
niftis = glob.glob(funcdir+'sub-[0-9][0-9][0-9][0-9][0-9][0-9]/sub-[0-9][0-9][0-9][0-9][0-9][0-9]_task-*_run-00[0-3]_space-MNI152NLin2009cAsym_desc-preproc_bold_sklstrp.nii.gz')

#Pair up nii with mask
masks = {}
for i in niftis:
    masks[i] = glob.glob(maskdir+i[72:82]+'/func/'+os.path.split(i)[1][:-27]+'brain_mask.nii.gz')
    print os.path.exists((maskdir+i[72:82]+'/func/'+os.path.split(i)[1][:-27]+'brain_mask.nii.gz'))

#how to index just ps number
os.path.split(i)[1][:9] # where i is i in nifti 

fwhm=6
suffix='_smooth.nii.gz'

masks = {k: str(v[0]) for k,v in masks.iteritems()}

# Basically by this point, you have a dictionary where the KEY is the NIFTI YOU WANT TO SMOOTH and the VaALUE is the BINARY BRAIN MASK FOR THE PARTICIPANT WHOS NIFTI YOU WANT TO SMOOTH. Rubbish script so far haha

for i in masks.items():
    print ('key:', i[0])
    print ('val:', i[1])

#change to where smooth images are to be stored
smoothdir = '/its/home/ws231/Desktop/cisc1/projects/critchley_vibe/skullstrip_smooth/'

for i in masks.items():
    output =  str(smoothdir+os.path.split(i[0])[1][:10]+'/'+os.path.split(i[0])[1][:-19]+'smooth.nii.gz')
    print ('OUTPUT:',output)
    if os.path.exists(output) == False:
        median = subprocess.check_output(['fslstats', str(i[0]), '-k', str(i[1]), '-p', '50'])
        sigma = str((fwhm / (2 * np.sqrt(2 * np.log(2)))))
        bt =  str((float(median) * 0.75))
        print('median:', median)
        print('bt:', bt)
        print ('sigma:', sigma)
        subprocess.call(['susan', str(i[0]), bt, sigma, '3', '1', '0', output])
    elif os.path.exists(output) == True:
        print (output, 'ALREADY EXISTS')
        continue
'''
