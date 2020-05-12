''' This script is to transform a mask so that its dimensions are the same as first-level functional files (stats/cope)
After this, they should be able to be used in FeatQuery

see: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FLIRT/FAQ#How_do_I_transform_a_mask_with_FLIRT_from_one_space_to_another.3F

'''
import subprocess 

# set this variable to store the masks you want transformed 
msk = ['/its/home/ws231/Desktop/cisc1/projects/critchley_vibe/masks/HO_anterior_cingulate.nii.gz']
# set this variable to the reference image (the target)
rf = '/its/home/ws231/Desktop/cisc1/projects/critchley_vibe/lev_1/sub-427272/run-001.feat/reg/standard.nii.gz'

# for sanity check, get header info on mask and reference image
print ('header info for mask')
[subprocess.call(['fslinfo', m]) for m in msk]
print ('header info for reference')
subprocess.call(['fslinfo',rf])

# Now tranform the mask using flirt 

for i in msk:
    newmsk = i.replace('.nii.gz','_new.nii.gz')
    subprocess.call(['flirt','-in',i,'-ref',rf,'-applyxfm','-usesqform','-out',newmsk])
    newbinmsk = newmsk.replace('.nii.gz','_bin.nii.gz')
    subprocess.call(['fslmaths',newmsk,'-thr','0.5','-bin',newbinmsk])

'''
Here is the code from the wiki:

flirt -in mask3mm -ref $FSLDIR/data/standard/MNI152_T1_2mm -applyxfm -usesqform -out mask2mm

fslmaths mask2mm -thr 0.5 -bin highres_mask

''' 



