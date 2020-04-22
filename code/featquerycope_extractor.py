#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 13:02:38 2020

@author: willstrawson
"""

# This script should incoperate COPE values extracted from FeatQuery into the
# dataframe which contains avh data,thought data and symptom data. 
import pandas as pd
import glob 
import numpy as np

# Location of main perrun dataframe
data = ('/Users/willstrawson/Documents/PhD/Rotation_2/Data/perrun_postspss_precope.csv')
maindf = pd.read_csv(data) 

# Function to extract cope names, mean cope values and mask name and apppend to existing datafram

#Input path MUST follow this directory structure
#TODO: make more robust - shouldnt rely on indexing 
inputpath = '/Users/willstrawson/Documents/PhD/Rotation_2/fMRI/lev_1/sub-*/run-*.feat/featquery_*_nonbin_7copes/report.txt'
maskname = 'rA1_ACC'
def fq_extractor(inputpath, maskname):
    # Collect list of all relevent file names to read 

    fls = glob.glob(inputpath)
    
    # Create dictionary where pateint name and run are keys and cope values are values  
    copes = {}
    # loop through each file 
    for f in fls:
        # extract data from relevent column/s and add to value
        # TODO: stip file name to patient and run in a more robust way
        patient = f.split('/')[8][4:]
        run = f.split('/')[9][6]
        # This is not robust but this needs to == the index of the mask namein title 
        mask = f.split('/')[10][10:13]
        # Pateint number and run as key, dataframe as value 
        # from dataframe, extrat cope name and mean cope value 
        copes[patient, run, mask]=pd.read_csv(f, sep = ' ',usecols = [1,5], header=None)
    
    #Now transpose these dataframes into wide format 
    for idx,df in enumerate(copes):
        copes[df] = copes[df].T
        # Input mask name (the 2nd index of the dict key) with cope name 
        mask = df[2]
        copes[df].iloc[0] = copes[df].iloc[0] + '_' + mask
        #Shift row 1 to header
        copes[df].rename(columns=copes[df].iloc[0], inplace = True)
        copes[df].drop(copes[df].index[0], inplace = True)
        # Add pateint and run column to dataframe
        copes[df]['patient'] = df[0]
        copes[df]['run'] = df[1]
        # subtract 'stats/' from cope name 
        copes[df].columns = copes[df].columns.str.replace('stats/','')
        # merge all this into one BIG DF
        if idx == 0: 
            bigdf = copes[df]
        else:
            bigdf = bigdf.append(copes[df])
        
    # Collapse data frame so only one row per run
    bigdf = bigdf.groupby(['run','patient'], as_index=False ).first()
            
    # convert contents to float or else merge gets mad
    bigdf = bigdf.astype(float)        
    maindf['run'] = pd.to_numeric(maindf['run'], errors = 'coerce')
    # merge copedf with the main df 
    merged = pd.merge(left = maindf, right = bigdf, on=['patient', 'run'], how='left')
    
    merged.to_csv('/Users/willstrawson/Documents/PhD/Rotation_2/Data/perrun_spssdata_{}.csv'.format(maskname))

fq_extractor(inputpath, maskname)


    

    
    
    
    
    