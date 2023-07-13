# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 16:54:31 2021

@author: Benjamin Lowe

Code written to test for equiluminance throughout the duration of a given
paradigm. The program requires the directory the paradigm was run in saved
each frame displayed within a sub-directory named "screenshots". From here, 
the program stores the pixel values of each image into a 2D array with each
row representing a unique screenshot. Deviant screenshots are intentified as
those with a mean pixel value greater or lower than 10% the baseline specified.
"""
#%% Importing important libraries
import os, glob
import numpy as np
from PIL import Image
path = os.getcwd()

#%% User inputs
baseline = 127.5
glitch_ind = 0 # if your screenshots are forming black bars up the top of your saved images, set this to 36479 (assuming screen resolution was 1920x1080) -> otherwise, set this variable to 0 -> I have also found that it doesn't make a difference either way

#%% Making important lists
os.chdir(path)
os.chdir('screenshots')
files = glob.glob('*.tif')
x, y = Image.open(files[0]).size
image_data = np.zeros((len(files), x*y))
for i, file in enumerate(files):
    print('loading in screenshot: {}'.format(i))
    im = Image.open(file)
    image_data[i, :] = np.array(im.getdata()).mean(axis=1)

#%% Removing black bars from top of images
for i in range(image_data.shape[0]):
    image_data[i, :glitch_ind] = image_data[i, glitch_ind+1]

#%% Finding outlier frames
deviant_inds = []
for i, val in enumerate(image_data.mean(axis=1)):
    if val > baseline+baseline*0.035 or val < baseline-baseline*0.035:
        deviant_inds.append(i)

percentage_deviant = round(len(deviant_inds)/len(files), 2)
print('Percentage of deviant frames: {}%'.format(percentage_deviant*100))

#%% Storing deviant frames into list to be viewed in consol
deviant_frames = []
for i in deviant_inds:
    deviant_frames.append(Image.open(files[i]))