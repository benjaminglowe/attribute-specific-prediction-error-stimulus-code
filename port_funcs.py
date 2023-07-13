# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 16:37:24 2021

@author: Benjamin Lowe

Serial communication port functions called within Benjamin Lowe's second PhD
study.
"""
#%% Importing important libraries
import serial
from psychopy import core, parallel

#%% Defining important functions
def port_init(port_type, port_address):
    '''
    Function written to initialise the parallel port within PsychoPy.
    
    Parameter(s)
    ============
    port_type : string
        The type of port you'd like to initialise within your script.
        Right now the function only accepts three values for this variable,
        those being: 'serial', 'parallel', and 'test'.
        - 'serial' is used for serial ports
        - 'parallel' is used for parallel ports
        - 'test' doesn't initialise any port but is useful for testing the
            timing of sent triggers
    
    port_address : string
        The address of the communication port.
    
    Return
    ======
    port : object
        An object which will send triggers to your initalised commication port.
    '''
    assert port_type in ['serial', 'parallel', 'test']
    if port_type == 'serial':
        port = serial.Serial(port_address)
        if port.is_open == False:
            port.open()
    if port_type == 'parallel':
        port = parallel.ParallelPort(port_address) # e.g., 57084 for KG-OB407
    if port_type == 'test':
        port = []
    #port_reset(port)
    
    return port

def set_data(port, trig_code):
    '''
    Function written for sending a given trigger code via the initalised
    communication port within a PsychoPy script.
    
    Parameters:
    ===========
    port : object
        The initalised port within the script. Can be ParallelPort or Serial.
        
    trig_code : int
        The trigger code to be sent via the initalised communication port.
    '''
    if type(port) == parallel.ParallelPort:
        port.setData(trig_code)
    if type(port) == serial.serialwin32.Serial:
        port.write(chr(int(trig_code)))

def port_reset(port=[]):
    '''
    Function written to "reset" an initalised communication port within
    PsychoPy. This works by first sending all pins "high" (255), waiting a
    brief period, and then sending all pins "low" (0).
    
    Parameter(s)
    ============
    port : object
        The initalised commication port you'd like to reset.
    '''
    if port == []:
        print('No port was reset')
    if port:
        set_data(port, 255)
        core.wait(1)
        set_data(port, 0)
        core.wait(1)

def send_trigger(trig_code=0, port=[], send=False, trig_clock=None):
    '''
    Function written to send a specified trigger to an initalised communication 
    port. These are often used to index points in a time series whereby a 
    participant was stimulated by a particular condition/stimulus, with each
    respective condition/stimulus being denoted by a different 8-bit trigger 
    code (ranging from 0 to 255).
    
    Parameter(s)
    ============
    trig_code : int in range(1, 256)
        The trigger code you'd like to send via the initalised communication 
        port. Avoid having this as zero.
    
    port : object
        Initalised communication port within PsychoPy. See port_init.
    
    send : bool
        The send status of a trigger. This should be used as a conditional
        within your PsychoPy script. If send is True, a trigger greater than 0
        should be sent. Otherwise, zero should be sent (see example below).
    
    trig_clock : core.Clock object
        An already initalised PsychoPy core.Clock object.
    
    Return
    ======
    send : bool
        Changes the status of send to 0.
    
    How to use
    ==========
    ** Code specifying the onset of a particular stimulus next window flip **
    send = True
    trig = trig_code
    
    ** Remainder of routine code **
    
    # refresh the screen
    if continueRoutine:
        win.flip()
        if send:
            send = send_trigger(trig, port, send) # sends specified trig_code
        else:
            send_trigger() # resets pins to zero
    '''
    if port:
        if send:
            set_data(port, trig_code) # sends trigger code of interest
            send = False # change send status to false for next flip
            if trig_clock != None: # for checking when trigger codes are being sent if you wish to do so
                print('{} sent at {}'.format(trig_code, trig_clock.getTime()))
        else:
            set_data(port, trig_code) # sends pins back down to zero (trig_code=0)
    else:
        if send:
            print('trigger code: {}'.format(trig_code))
            send = False
        else:
            print('trigger code: {}'.format(trig_code))
    
    return send

#%% Defining important variables
trig_clock = core.Clock() # initialising a clock to keep track of triggers if you wish to do so
send = False
