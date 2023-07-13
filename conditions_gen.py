# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 10:54:12 2021

@author: Benjamin Lowe

Program designed to generate a conditions file needed during for PsychoPy
deployment of the fMRI paradigm part of Benjamin Lowe's second study within his 
PhD candidature.
"""
#%% Importing important libraries
import numpy as np
import pandas as pd
from statistics import mean
from random import randint

#%% Defining important functions
def vio(traj_i_key): # violation of trajectory priors
    if traj_i_key.split('_')[1] == '0':
        out = '{}_{}'.format(traj_i_key.split('_')[0], '1')
    
    if traj_i_key.split('_')[1] == '1':
        out = '{}_{}'.format(traj_i_key.split('_')[0], '0')
        
    return out

#%% Defining key variables
attributes = 3
stim_path = 'stimuli//{}_{}_{}.png'
imaging_method = input('fMRI, EEG, or MEG? ')
assert imaging_method in ['fMRI', 'EEG', 'MEG']

if imaging_method == 'fMRI':
    catch_appears = np.array([0, 0.4, 0.8, 1.2]) # time at which any of the catches can appear
    reps = 2
    total_trials = reps*attributes*(2**attributes)*2 # reps * attributes * trajectories (2^attributes) * 2 (violation and control)
    inter_trial_durs = np.array([.5, .5, .75, 1, 1, 1, 2, 2, 3, 4.75, 7, 12])
    inter_trial_durs = list(np.repeat(inter_trial_durs, 
                                 total_trials/len(inter_trial_durs)))
    assert round(mean(inter_trial_durs)) == 3
    catch_dur = 0.4
    blocks = 2

else:
    catch_appears = np.array([0, 30, 60, 90]) # frame at which any of the catches can appear
    reps = 2
    total_trials = reps*attributes*(4**attributes)*2 # reps * attributes * trajectories (4^attributes) * 2 (violation and control)
    inter_trial_durs = list(np.ones(total_trials)*0.5)
    catch_dur = 30
    blocks = 8

#%% Defining attribute trajectories
a_incs = pd.read_excel('perceptually_uniform_attribute_increments.xlsx') # attribute increments found via JND tasks

col_incs = np.array((a_incs['colour']))
siz_incs = np.array((a_incs['size']))
ori_incs = np.array(range(0, 80, 5))

if imaging_method == 'fMRI':
    participant = int(input('Participant: '))
    if participant%2 != 0:
        traj_i = {'0_0' : [0, 3, 6, 9, 12], # up in threes
                  '0_1' : [15, 13, 11, 9, 7]} # down in twos  
    else:
        traj_i = {'1_0' : [0, 2, 4, 6, 8], # up in twos
                  '1_1' : [15, 12, 9, 6, 3]} # down in threes

else:
    traj_i = {'0_0' : [0, 3, 6, 9, 12], # up in threes
              '0_1' : [15, 13, 11, 9, 7], # down in twos
              '1_0' : [0, 2, 4, 6, 8], # up in twos
              '1_1' : [15, 12, 9, 6, 3]} # down in threes

#%% Making dataframe
columns = ['trial_label', 'im_0_file', 'im_1_file', 'im_2_file', 'im_3_file', 
           'im_4_file', 'inter_trial_dur', 'catch_appears', 'catch_dur', 
           'resp_dur', 'trig_0', 'trig_1', 'trig_2', 'trig_3', 'trig_4']
df = pd.DataFrame(columns=columns)

#%% Filling in dataframe with violation trials
i = 0
for r in range(reps):
    for c in traj_i.keys(): # for each colour
        for s in traj_i.keys(): # for each size
            for o in traj_i.keys(): # for each orientation
                
               col = col_incs[traj_i[c]]
               siz = siz_incs[traj_i[s]]
               ori = ori_incs[traj_i[o]]
               
               col_v = col_incs[traj_i[vio(c)]]
               siz_v = siz_incs[traj_i[vio(s)]]
               ori_v = ori_incs[traj_i[vio(o)]]
               
               col_v[4] = col[4]
               siz_v[4] = siz[4]
               ori_v[4] = ori[4]
               
               inter_trial_dur = inter_trial_durs[randint(0, 
                                                    len(inter_trial_durs)-1)]
               inter_trial_durs.remove(inter_trial_dur)
               
               df.loc[i] = ['col vio: col_{}; siz_{}; ori_{}'.format(c, s, o),
                             stim_path.format(col_v[0], siz[0], ori[0]),
                             stim_path.format(col_v[1], siz[1], ori[1]),
                             stim_path.format(col_v[2], siz[2], ori[2]),
                             stim_path.format(col_v[3], siz[3], ori[3]),
                             stim_path.format(col_v[4], siz[4], ori[4]),
                             inter_trial_dur, 0, 0, 0, 1, 2, 3, 4, 10]

               inter_trial_dur = inter_trial_durs[randint(0, 
                                                    len(inter_trial_durs)-1)]
               inter_trial_durs.remove(inter_trial_dur)

               df.loc[i+1] = ['siz vio: col_{}; siz_{}; ori_{}'.format(c, s, o),
                             stim_path.format(col[0], siz_v[0], ori[0]),
                             stim_path.format(col[1], siz_v[1], ori[1]),
                             stim_path.format(col[2], siz_v[2], ori[2]),
                             stim_path.format(col[3], siz_v[3], ori[3]),
                             stim_path.format(col[4], siz_v[4], ori[4]),
                             inter_trial_dur, 0, 0, 0, 1, 2, 3, 4, 20]

               inter_trial_dur = inter_trial_durs[randint(0, 
                                                    len(inter_trial_durs)-1)]
               inter_trial_durs.remove(inter_trial_dur)

               df.loc[i+2] = ['ori vio: col_{}; siz_{}; ori_{}'.format(c, s, o),
                             stim_path.format(col[0], siz[0], ori_v[0]),
                             stim_path.format(col[1], siz[1], ori_v[1]),
                             stim_path.format(col[2], siz[2], ori_v[2]),
                             stim_path.format(col[3], siz[3], ori_v[3]),
                             stim_path.format(col[4], siz[4], ori_v[4]),
                             inter_trial_dur, 0, 0, 0, 1, 2, 3, 4, 30]
              
               i += 3

#%% Filling in dataframe with control trials
i = len(df)
for r in range(reps):
    for a in range(attributes):
        for c in traj_i.keys():
            for s in traj_i.keys():
                for o in traj_i.keys():
                   
                   col = col_incs[traj_i[c]]
                   siz = siz_incs[traj_i[s]]
                   ori = ori_incs[traj_i[o]]

                   inter_trial_dur = inter_trial_durs[randint(0, 
                                                    len(inter_trial_durs)-1)]
                   inter_trial_durs.remove(inter_trial_dur)

                   df.loc[i] = ['control: col_{}; siz_{}; ori_{}'.format(c, s, o),
                                 stim_path.format(col[0], siz[0], ori[0]),
                                 stim_path.format(col[1], siz[1], ori[1]),
                                 stim_path.format(col[2], siz[2], ori[2]),
                                 stim_path.format(col[3], siz[3], ori[3]),
                                 stim_path.format(col[4], siz[4], ori[4]),
                                 inter_trial_dur, 0, 0, 0, 1, 2, 3, 4, 40]
                    
                   i += 1

#%% Fill in dataframe with catch trials               
catch_trials_n = round(len(df)*0.1)
while catch_trials_n%4 != 0:
    catch_trials_n += 1

catch_appears = np.repeat(catch_appears, catch_trials_n/len(catch_appears))
catch_inds = np.random.choice(np.array(range(len(df))), int(catch_trials_n), 
                              replace=False)

catch_trials = df.loc[catch_inds].reset_index()
catch_trials = catch_trials.drop("index", axis=1)
catch_names = ['(CATCH) {}'.format(x) for x in catch_trials['trial_label']]
catch_trials['trial_label'] = catch_names
catch_trials['catch_appears'] = catch_appears
catch_trials['catch_dur'] = catch_dur
catch_trials['resp_dur'] = np.ones((len(catch_trials)))*catch_dur*5-catch_appears
catch_trials['trig_4'] = 50

out = pd.concat([df, catch_trials], ignore_index=True)

#%% Outputting dataframe
conds_df = pd.DataFrame(columns=['block'])

if imaging_method != 'fMRI':
    out = out.sample(frac=1).reset_index(drop=True) # shuffling conditions file before splitting it into blocks
    block_trials_n = len(out)/blocks
    assert block_trials_n == int(block_trials_n)
    blocks_range = range(0, len(out), int(block_trials_n))
    for b, block in enumerate(blocks_range):
        block_out = out[block:block+int(block_trials_n)]
        block_name = '{}_block_{}.xlsx'.format(imaging_method, b)
        block_out.to_excel(block_name, index=False)
        conds_df.loc[b] = [block_name]
else:
    block_name = '{}_block_0.xlsx'.format(imaging_method)
    out.to_excel(block_name, index=False)
    conds_df.loc[0] = [block_name]

conds_df.to_excel('{}_conditions.xlsx'.format(imaging_method), index=False)
