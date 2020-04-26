#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 10:38:41 2020

@author: willstrawson
"""
import pandas as pd 

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
dff = dfff.rename({'MeanAVHduration':'avh_meandur', 'total_avh_duration':'avh_totaldur'}, axis=1)
# keep only columns which will be used as a regressor, just for tidyness 
cols = ['patient_run','patient','run','avh_instances','avh_meandur','avh_totaldur',
         'MWF1','MWF2','MWF3','MWF4','MWF5','MWF6','AVHF1','AVHF2',
         'AVHF1_2','AVHF2_2','BSIS_Voices','BAVQ_Persecutory']

df = dff[cols]


df[cols[1:]] = df[cols[1:]].apply(pd.to_numeric, errors='coerce')

# replace NaNs
df.fillna(df.mean())

# ------ #


#Read in fsf template
template = '/Users/willstrawson/Documents/PhD/Rotation_2/fsfs/template_rest/pretemplate_group.fsf'
# Specify name of output fsf
fsf_out = '/Users/willstrawson/Documents/PhD/Rotation_2/fsfs/template_rest/rs-sbfc_group_template.fsf'



# TODO : Demean 