# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 13:46:51 2021
@author: Benjamin Lowe
Functions used as part of Benjamin Lowe's second Phd study paradigm.
"""
def calc_stimulus_area(length):
    ''' 
    Calculates the area of stimulus used in Benjamin Lowe's PhD study two
    experimental paradigms.
    
    Parameter(s)
    ============
    length : int or float
        The side length of the stimulus. To find, refer to the second value
        of the image's file name, or enter the value of either its length or 
        width as can be found within image details.
        
    Return
    ======
    area : float
        Area of stimulus as found using the following equation: y = (3x^2)/4.
    '''
    
    return (3*length**2)/4

def finding_mu(image_file, x, y, baseline_lumin):
    '''
    Finds the mean for a normal distribution of background colours sampled 
    during the presentation of a given stimulus during Benjamin Lowe's PhD 
    study two experimental paradigm. This is to maintain equiluminance
    throughout the paradigm's duration.
    
    Parameters(s)
    =============
    image_file : string
        Name of stimulus image file. Assumes that the first number represents
        its colour (RBG pixel value) and second represents its side length.
    
    x, y : ints or floats
        Width and height of Psychopy window.
    
    baseline_lumin : int or float
        Average pixel luminance within window that the experimenter is trying
        to maintain over the course of the paradigm.
    
    Return
    ======
    background_pixel_value : float
        Mean of normally distributed pixel values required of equiluminance.
    '''
    image_colour = int(image_file.split('_')[0].split('//')[1])
    image_length = int(image_file.split('_')[1].split('.')[0])
    image_area = calc_stimulus_area(image_length)
    image_lumin = image_area*image_colour
    
    total_pixels = x*y
    remaining_pixels = total_pixels-image_area
    desired_lumin = total_pixels*baseline_lumin
    lumin_discrepancy = desired_lumin-image_lumin
    
        
    return lumin_discrepancy/remaining_pixels

def convert_byte_value(input_value):
    '''
    Converts a byte value ranging from 0 to 255 to a psychopy equivalent real
    number value ranging from -1 to 1 according to the following formula:
    y = 2x/255 - 1
    
    Parameter(s)
    ============
    input_value : int or float
        Input value ranging from 0 to 255. For the most accurate converstion, 
        use a float (calculated using finding_mu for example). Of course, bytes
        are by nature natural numbers so this may not always be possible.
        
    Return
    ======
    output_value : float
        Output value ranging from -1 to 1.
    '''
    
    return (2*input_value)/255 -1
