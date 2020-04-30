#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 10:38:41 2020

@author: willstrawson
"""
import pandas as pd 
import glob 
import os
import numpy as np
# This script will create the fsf files needed for group level rs-sbfc analysis in fsl
# It will extract avh metrics, mwf scores and symtom scores for each patient and populate an fsf template 

# ------ #
# First it makes the dataframe needed to extract rest run metrics for rs-sbfc analysis group evs 
# It reads in a datafraem which contains AVH metrics, VAS scores, MWF scores, and symptoms 
# It outputs a dataframe with only rest run metrics 

#read in dataframe
dfff = pd.read_csv('/Users/willstrawson/Documents/PhD/Rotation_2/Data/vas_avh_pca_symptoms_perrun.csv')

# delete non rest rows
dfff = dfff.loc[dfff['run']=='0']
#change columns names 
dff = dfff.rename({'MeanAVHduration':'avh_meandur', 'total_avh_duration':'avh_totaldur', 
                   'BSIS_Voices':'BSIS_V', 'BAVQ_Persecutory':'BAVQ_P'}, axis=1)
# keep only columns which will be used as a regressor, just for tidyness 
cols = ['patient_run','patient','run','avh_instances','avh_meandur','avh_totaldur',
         'MWF1','MWF2','MWF3','MWF4','MWF5','MWF6','AVHF1','AVHF2',
         'AVHF1_2','AVHF2_2','BAVQ_P', 'avh_pca']

df = dff[cols]

# Add Age and BSIS_v column from per_patient dataframe to include as regressor 
# If you want to include Any perpatient symptoms, now's the time... its easy!
agedf = pd.read_csv('/Users/willstrawson/Documents/PhD/Rotation_2/Data/ViBE_age_bsisv_sdt.csv')
agedf.rename(columns={'BSIS_Voices':'BSIS_V'})

# Merge age df into main df
df = pd.merge(df, agedf, on='patient', how='outer')


# Now to read in framewise displacement  
fds = {}
fd_fls = glob.glob('/Users/willstrawson/Documents/PhD/Rotation_2/fmriprep_regressors/*')
for i in fd_fls:
    fds[os.path.split(i)[1][4:10]] = pd.read_csv(i, sep='\t')
# Keep only fd 
cols2 =  ['framewise_displacement']
for i in fds:
    fds[i] = fds[i][cols2]
    # Take the mean 
    fds[i] = fds[i].mean()
    # renamecolum
    fds[i].rename(columns={'0':'mean_fd'})

# Make these individual Series into one dataframe where columns = patient mean_fd 
mean_fd = pd.DataFrame(fds).T
# Reset index so patient number because normal column
mean_fd = mean_fd.reset_index()
# Rename patient column
mean_fd.rename(columns={'index':'patient'}, inplace=True)
#Turn patient column into int
mean_fd= mean_fd.apply(pd.to_numeric, errors='coerce')
# merge this dataframe with the main one :-)
df = pd.merge(df, mean_fd, on='patient', how='outer')

#Turn whitespzce into NaN
df = df.replace(r'^\s*$', np.nan, regex=True)
# Turn all numbers to numbers 
df[cols[1:]] = df[cols[1:]].apply(pd.to_numeric, errors='coerce')
#Do the following columns individually as the abovemethjod did not work 
df['Age']=pd.to_numeric(df['Age'], errors='coerce')
df['BSIS_Voices']=pd.to_numeric(df['BSIS_Voices'], errors='coerce')
df['SDT_criterion']=pd.to_numeric(df['SDT_criterion'], errors='coerce')

# replace NaNsand create new imputed df
dfi = df.fillna(df.mean())

# TODO: output statistics on how many missing values were imputed


# Demean columns
allcols = df.columns.tolist()
dfi[allcols[3:]] = dfi[allcols[3:]].sub(dfi[allcols[3:]].mean(), axis='columns')

# rename framewise displacement column 
dfi.rename(columns={'framewise_displacement':'mean_fd'},inplace=True)

# make column headers lowercase
dfi.columns = [x.lower() for x in dfi.columns]

# remove patient 54665 because they're not in analysis and mess up indexing
dfi = dfi[dfi.patient != 54665]



# ------ #

# Need to engineer search terms that appear in fsf template
# These are uppercase column names + _ sub number
# Engineer these using the existing column names 
searchterms = []
# Add uppercase EV names
[searchterms.append(i.upper()) for i in dfi.columns[3:]]
# Add patient number after each variable name 
# Thislist should contain all the possible search terms present in the fsf 
srchs = []
for i in searchterms:
    for n in dfi['patient']:
        srchs.append(str(i) + '_' + str(n))  
        
# Create replacements dict where key = searchterms and value is number from dfi
replacements = {}
for i in srchs:
    # reegnineer column header name from search terms
    var = i[:-7].lower()
    print (var)
    # ... and the same for participant name
    ps = i[-6:]
    print (ps)
    # Add the specific values for each patient and variable
    replacements[i] = dfi[var].loc[dfi['patient'] == int(ps)]

#Read in fsf template
template = '/Users/willstrawson/Documents/PhD/Rotation_2/fsfs/template_rest/rs-sbfc_group_mwfs_template.fsf'
# Specify name of output fsf
fsf_out = '/Users/willstrawson/Documents/PhD/Rotation_2/fsfs/template_rest/rs-sbfc_group_mwfs.fsf'

with open (template, 'r') as infile:
    with open (fsf_out, 'w') as outfile:
        for line in infile:
            print (line)
            for src, target in replacements.items():
                #print (src, target)
                line = line.replace(str(src),str(target.to_numpy()[0]))
            outfile.write(line)







