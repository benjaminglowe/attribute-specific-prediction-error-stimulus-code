# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 15:50:44 2020

@author: Benjamin Lowe

Program designed to draw stimuli used within Benjamin Lowe's second PhD study.
The stimuli drawn varies across three dimensions: size, pixel intensity 
(colour), and orientation, as specified by the ranges below. 
"""
#%% Importing important libraries
import os
from PIL import Image

#%% Defining important functions
def paste_im_center(im, background, win_size):
    win_x, win_y = (int(win_size[0]/2), int(win_size[1]/2))
    im_x, im_y = (int(im.size[0]/2), int(im.size[1]/2))
    paste_x, paste_y = (win_x-im_x, win_y-im_y)
    background.paste(im, (paste_x, paste_y))

#%% Creating required directories
if os.path.isdir('stimuli') == False:
    os.mkdir('stimuli')

#%% Hard coding important variables
pixel_intensity_range = range(128, 256)
max_size = 400
size_range = range(50, max_size+1, 2)
orientation_range = range(0, 85, 5)
win_size = (int(max(size_range)*1.5), int(max(size_range)*1.5))

#%% Creating stimuli
for i in pixel_intensity_range:
    im = Image.new('RGBA', (2, 2))
    im_data = [(i, i, i, 255), (0, 0, 0, 0), 
               (i, i, i, 255), (i, i, i, 255)]
    im.putdata(im_data)
    print(i)
    for j in size_range:
        im = im.resize((j, j))
        background = Image.new('RGBA', win_size)
        paste_im_center(im, background, win_size)
        for k in orientation_range:
            out_name = 'stimuli//{}_{}_{}.png'.format(i, j, k)
            if os.path.exists(out_name) == False:
                out = background.rotate(k*-1)
                out.save(out_name)
                print('saved: {}'.format(out_name))