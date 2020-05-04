import glob
import os
from shutil import copyfile

src = '/usr/local/fsl/etc/flirtsch/ident.mat'

# make reg directories 

# location of the first level feats/reg directories 
fls = glob.glob('/its/home/ws231/Desktop/cisc1/projects/critchley_vibe/rs-sbfc/sub-*/lev_1/ACC.feat/')

for i in fls:
    os.mkdir(i+'reg/')
    dst = i+'reg/example_func2standard.mat'
    copyfile(src, dst)
print (src, dst)


# location of feats (but not lower reg/ directory)
fls2 = glob.glob('/its/home/ws231/Desktop/cisc1/projects/critchley_vibe/rs-sbfc/sub-*/lev_1/ACC.feat/')

for i in fls2:
    src = i+'mean_func.nii.gz'
    dst = i+'reg/standard.nii.gz'
    try:
        copyfile(src,dst)
    except IOError:
        print('Subject {} has missing mean_func.nii.gz file'.format(i.split('/')[9]))


