import glob
import os
from shutil import copyfile

src = '/usr/local/fsl/etc/flirtsch/ident.mat'

# make reg directories 

# location of the first level feats/reg directories 
fls = glob.glob('/its/home/ws231/Desktop/cisc1/projects/critchley_vibe/rs-sbfc/sub-*/lev_1/task_cluster_1_rPCG.feat/')

for i in fls:
    os.mkdir(i+'reg/')
    dst = i+'reg/example_func2standard.mat'
    copyfile(src, dst)
print (src, dst)

# now move mean_funk

for i in fls:
    src = i+'mean_func.nii.gz'
    dst = i+'reg/standard.nii.gz'
    try:
        copyfile(src,dst)
    except IOError:
        print('Subject {} has missing mean_func.nii.gz file'.format(i.split('/')[9]))


