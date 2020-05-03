# Script to run run seed based functional connectivity in a given mask 
# This script is in 4 sections:
# 1. Extract time series from ALREADY CREATED MASK
# 2. Create 1st level fsfs from template
# 3. Run these 1st level fsfs (locally, so this will take a while)
# 4. Run group level fsfs

import subprocess
import os
import glob



# Note: maskpath needs to == to the binary version!

def timeseries(maskpath, maskname):
    # Create list of off resting runs' functional niftis
    fls = glob.glob('/its/home/ws231/Desktop/cisc1/projects/critchley_vibe/skullstrip_smooth/sub-*/sub-*_task-rest_run-001_space-MNI152NLin2009cAsym_desc-preproc_smoothsklstrpd.nii.gz')
    # Loop through each nifti and run fslmeants on each for the given mask
    for f in fls:
	# extract participant id
	ps = f.split('/')[9]
	#define output directory
	outputdir = ('/its/home/ws231/Desktop/cisc1/projects/critchley_vibe/rs-sbfc/{}/{}_{}.txt'.format(ps,ps,maskname))
        # extract timeseries
	print('Running timeseries extraction for {} in {}'.format(ps, maskname))
	subprocess.call(['fslmeants','-i',f,'-o', outputdir, '-m', maskpath])

# Run functions...
timeseries('/its/home/ws231/Desktop/cisc1/projects/critchley_vibe/masks/task_cluster_3_smooth_5mm_thr_0.15_bin.nii.gz','task_cluster_3_ACC')
timeseries('/its/home/ws231/Desktop/cisc1/projects/critchley_vibe/masks/task_cluster_2_smooth_5mm_thr_0.19_bin.nii.gz','task_cluster_2_rA1')
timeseries('/its/home/ws231/Desktop/cisc1/projects/critchley_vibe/masks/task_cluster_1_smooth_5mm_thr_0.10_bin.nii.gz','task_cluster_1_rPCG')

'''

# ------------------------------------------------#

#FIRST LEVEL FSF MAKER - RS-SBFC for given mask 

# where sub### drs are stored
#get all paths 
subdirs = glob.glob('/its/home/ws231/Desktop/cisc1/projects/critchley_vibe/skullstrip_smooth/sub-*/sub-*_task-rest_run-001_space-MNI152NLin2009cAsym_desc-preproc_smoothsklstrpd.nii.gz')
# 1st level fsf template 
template = str('/its/home/ws231/Desktop/cisc1/projects/critchley_vibe/fsfs/template_rest/template_rest.fsf')
#  where to store fsf files 
fsfdir = str('/its/home/ws231/Desktop/cisc1/projects/critchley_vibe/rs-sbfc/fsfs/')

def lev_1_fsfmaker(maskname):

	for dr in list(subdirs):
	    splitdir = dr.split('/')
	    splitdir_sub = splitdir[9]
	    subnum = splitdir_sub[-6:] #delete duplicates??
	    print(subnum)

	    ntime = os.popen('fslnvols {}'.format(dr)).read().rstrip()
	    print (ntime)

	    replacements = {'SUBNUM': subnum, 'NTPTS':ntime, 'MSKNAME':maskname}

	    with open (template) as infile:
		with open (fsfdir + 'sub-{}_{}.fsf'.format(subnum, maskname), 'w') as outfile:
		    for line in infile:
		        for src, target in replacements.items():
		            line = line.replace(src,target)
		        outfile.write(line)

	print ('num files read in:', len(subdirs))

lev_1_fsfmaker(maskname)

# ------------------------------------------------#

# FIRST LEVEL FEAT RUNNER 

#run all fsf files through FEAT 

fls = glob.glob('/its/home/ws231/Desktop/cisc1/projects/critchley_vibe/rs-sbfc/fsfs/sub-*_{}.fsf'.format(maskname))

for i in fls:
    print ('Running FEAT for:', os.path.split(i)[1])
    subprocess.call(["feat",i])

# -----------------------------------------------#
# TODO : Include reg work around 
#------------------------------------------------#

# GROUP LEVEL FEAT RUNNER 

# First replace mask name in templates
maskname = ('ACC')
	
#List all fsfs in the directory containing all the post-template group fsfs
fls = glob.glob('/its/home/ws231/Desktop/cisc1/projects/critchley_vibe/fsfs/template_rest/group_fsfs/rA1/*.fsf')
# Specify output dir for new fsf
out = '/its/home/ws231/Desktop/cisc1/projects/critchley_vibe/fsfs/template_rest/group_fsfs/{}/'.format(maskname)
# replace rA1 with mask name
replacements = {'rA1+':maskname,'rA1':maskname}


# Loop through each fsfs
for f in fls:
    print(f)
    with open(f) as infile:
        with open (out + os.path.split(f)[1], 'w') as outfile:
	    for line in infile:
		for src, target in replacements.items():
		    line = line.replace(src, target)
		outfile.write(line)
	# add new fsfs to outfsfs


# now run fsfs - loop through newly created files

fls = glob.glob('/its/home/ws231/Desktop/cisc1/projects/critchley_vibe/fsfs/template_rest/group_fsfs/ACC/*.fsf')

print (fls)

for f in fls:
    print (f)
    print ('Running group feat for {}'.format(os.path.split(f)[1]))
    subprocess.call(["feat",f])
    


'''





