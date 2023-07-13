#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2020.2.0),
    on January 27, 2021, at 11:35
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

import psychopy
#psychopy.useVersion('2020.2.0')


from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import pandas as pd
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard

from luminance_control_functions import *
from port_funcs import *

## what imaging method is being used to record brain data?
imaging_methods = ['fMRI', 'EEG', 'MEG']
imaging_method = 'EEG'
assert imaging_method in imaging_methods

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '2020.2.0'
expName = 'contextual_trajectory_paradigm_BL'  # from the Builder filename that created this script
expInfo = {'participant': '', 'session': '001'}
dlg = gui.DlgFromDict(dictionary=expInfo, sort_keys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'{}_behavioural_data/%s_%s_%s'.format(imaging_method) % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='R:\\PhD_studies\\Study2\\repo\\contextual_trajectory_paradigm.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(
    size=[1920, 1080], fullscr=True, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Setting parallel port
if imaging_method == 'EEG':
    port_type = 'parallel'
    port_address = 57084
if imaging_method == 'fMRI':
    port_type = 'test'
    port_address = 0
#port = port_init(port_type, port_address)
port = port_init('test', 0) #########################################################################################################################################

# Initialize components for Routine "welcome"

welcomeClock = core.Clock()
text_welcome = visual.TextStim(win=win, name='text_welcome',
    text='Welcome and thank you for agreeing to participate in the experiment!\n\nPlease press the SPACEBAR on the keyboard in front of you.',
    font='Arial',
    pos=(0, 0), height=0.025, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
key_resp_welcome = keyboard.Keyboard()

# Initialize components for Routine "intro"
introClock = core.Clock()
text_instructions = visual.TextStim(win=win, name='text_instructions',
    text='During this recording session, you will see a series of image trajectories which imply a stimulus changing across three attributes: colour, size, and orientation. It is your job to attend to these stimuli changes as much as possible. \n\nAdditionally, a red dot will periodically appear in the centre of the screen. When you see this, please press the SPACEBAR as quickly as possible.\n\nTo ensure that our recorded brain signals are clean, please keep ALL movement to a minimum where possible.\n\nIf you have any questions, please direct them to the researcher now.\n',
    font='Arial',
    pos=(0, 0), height=0.025, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
key_resp_instructions = keyboard.Keyboard()

if imaging_method == 'fMRI':
    text_welcome.text = 'Welcome and thank you for agreeing to participate in the experiment!\n\nPlease press the any key on the response pad.'
    text_instructions.text = 'During this recording session, you will see a series of image trajectories which imply a stimulus changing across three attributes: colour, size, and orientation. It is your job to attend to these stimuli changes as much as possible. \n\nAdditionally, a red dot will periodically appear in the centre of the screen. When you see this, please press any of the response keys as quickly as possible.\n\nTo ensure that our recorded brain signals are clean, please keep ALL movement to a minimum where possible.\n\nIf you have any questions, please direct them to the researcher now.\n'

# Initialize components for Routine "trial"
trialClock = core.Clock()

# defining some important variables
path = os.getcwd()
if imaging_method != 'fMRI':
    corr_ans = ['space']
    start_exp_TR_count = 1
else:
    corr_ans = ['1', '2', '3', '4']
    TR_times = []
    TR_tracker = keyboard.Keyboard()
    TR_tracker.status = STARTED
    _TR_tracker_allKeys = []
    start_exp_TR_count = 3
sigma = 1
baseline_lumin = 127.5
x, y = win.size
screenshots = False
rest_n = 0

# determining conditions file
cond_files = '{}_conditions.xlsx'.format(imaging_method)

# making screenshots directory
if screenshots and os.path.isdir('screenshots') == False:
    os.mkdir('screenshots')

# setting image durations
if imaging_method == 'fMRI':
    #im_dur = round(expInfo['frameRate']*0.4) # 400 ms
    im_dur = 0.4 # 400 ms
else:
    im_dur = round(expInfo['frameRate']*0.5) # 500 ms

fixation = visual.ShapeStim(
    win=win, name='fixation', vertices='cross',
    size=(0.025, 0.025),
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1, depth=-1.0, interpolate=True)
im_0 = visual.ImageStim(
    win=win,
    name='im_0', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
im_1 = visual.ImageStim(
    win=win,
    name='im_1', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)
im_2 = visual.ImageStim(
    win=win,
    name='im_2', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-4.0)
im_3 = visual.ImageStim(
    win=win,
    name='im_3', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-5.0)
im_4 = visual.ImageStim(
    win=win,
    name='im_4', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-6.0)
polygon = visual.ShapeStim(
    win=win, name='polygon', vertices='star7',
    size=(0.005, 0.005),
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1.000,-1.000,-1.000], lineColorSpace='rgb',
    fillColor=[1.000,-1.000,-1.000], fillColorSpace='rgb',
    opacity=1, depth=-7.0, interpolate=True)
key_resp_trial = keyboard.Keyboard()

# Initialize components for Routine "rest"
restClock = core.Clock()
text_rest = visual.TextStim(win=win, name='text_rest',
    text="You may now take a few moments break from the task. If you need to move, now is the time.\n\nIf you feel you're ready to continue with the experiment, please press SPACEBAR to begin the next block of trials.",
    font='Arial',
    pos=(0, 0), height=0.025, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
key_resp_rest = keyboard.Keyboard()

# Initialize components for Routine "finish"
finishClock = core.Clock()
text_finish = visual.TextStim(win=win, name='text_finish',
    text='Thank you for your participation! \n\nPlease sit back and relax. A researcher will be with you shortly.',
    font='Arial',
    pos=(0, 0), height=0.025, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
key_resp_finish = keyboard.Keyboard()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "welcome"-------
continueRoutine = True
# update component parameters for each repeat
key_resp_welcome.keys = []
key_resp_welcome.rt = []
_key_resp_welcome_allKeys = []
# keep track of which components have finished
welcomeComponents = [text_welcome, key_resp_welcome]
for thisComponent in welcomeComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
welcomeClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "welcome"-------
while continueRoutine:
    # get current time
    t = welcomeClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=welcomeClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_welcome* updates
    if text_welcome.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_welcome.frameNStart = frameN  # exact frame index
        text_welcome.tStart = t  # local t and not account for scr refresh
        text_welcome.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_welcome, 'tStartRefresh')  # time at next scr refresh
        text_welcome.setAutoDraw(True)
    
    # *key_resp_welcome* updates
    waitOnFlip = False
    if key_resp_welcome.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        key_resp_welcome.frameNStart = frameN  # exact frame index
        key_resp_welcome.tStart = t  # local t and not account for scr refresh
        key_resp_welcome.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_welcome, 'tStartRefresh')  # time at next scr refresh
        key_resp_welcome.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_welcome.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_welcome.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_welcome.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_welcome.getKeys(keyList=corr_ans, waitRelease=False)
        _key_resp_welcome_allKeys.extend(theseKeys)
        if len(_key_resp_welcome_allKeys):
            key_resp_welcome.keys = _key_resp_welcome_allKeys[-1].name  # just the last key pressed
            key_resp_welcome.rt = _key_resp_welcome_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
        
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in welcomeComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "welcome"-------
for thisComponent in welcomeComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_welcome.keys in ['', [], None]:  # No response was made
    key_resp_welcome.keys = None
# the Routine "welcome" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

for i in range(start_exp_TR_count):
    # ------Prepare to start Routine "intro"-------
    continueRoutine = True
    # update component parameters for each repeat
    key_resp_instructions.keys = []
    key_resp_instructions.rt = []
    _key_resp_instructions_allKeys = []
    # keep track of which components have finished
    introComponents = [text_instructions, key_resp_instructions]
    for thisComponent in introComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    introClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1

    # -------Run Routine "intro"-------
    while continueRoutine:
        # get current time
        t = introClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=introClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_instructions* updates
        if text_instructions.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_instructions.frameNStart = frameN  # exact frame index
            text_instructions.tStart = t  # local t and not account for scr refresh
            text_instructions.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_instructions, 'tStartRefresh')  # time at next scr refresh
            text_instructions.setAutoDraw(True)
        
        # *key_resp_instructions* updates
        waitOnFlip = False
        if key_resp_instructions.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_instructions.frameNStart = frameN  # exact frame index
            key_resp_instructions.tStart = t  # local t and not account for scr refresh
            key_resp_instructions.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_instructions, 'tStartRefresh')  # time at next scr refresh
            key_resp_instructions.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_instructions.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_instructions.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_instructions.status == STARTED and not waitOnFlip:
            if imaging_method == 'fMRI':
                theseKeys = key_resp_instructions.getKeys(keyList=['5'], waitRelease=False)
                _key_resp_instructions_allKeys.extend(theseKeys)
            else:
                theseKeys = key_resp_instructions.getKeys(keyList=corr_ans, waitRelease=False)
                _key_resp_instructions_allKeys.extend(theseKeys)
            if len(_key_resp_instructions_allKeys):
                key_resp_instructions.keys = _key_resp_instructions_allKeys[-1].name  # just the last key pressed
                key_resp_instructions.rt = _key_resp_instructions_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in introComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "intro"-------
    for thisComponent in introComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp_instructions.keys in ['', [], None]:  # No response was made
        key_resp_instructions.keys = None
    # the Routine "intro" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

# set up handler to look after randomisation of conditions etc
blocks = data.TrialHandler(nReps=1, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(cond_files),
    seed=None, name='blocks')
thisExp.addLoop(blocks)  # add the loop to the experiment
thisBlock = blocks.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
if thisBlock != None:
    for paramName in thisBlock:
        exec('{} = thisBlock[paramName]'.format(paramName))

for thisBlock in blocks:
    currentLoop = blocks
    # abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
    if thisBlock != None:
        for paramName in thisBlock:
            exec('{} = thisBlock[paramName]'.format(paramName))
    
    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=1, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions(block),
        seed=None, name='trials')
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            exec('{} = thisTrial[paramName]'.format(paramName))
    
    for thisTrial in trials:
        currentLoop = trials
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                exec('{} = thisTrial[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "trial"-------
        continueRoutine = True
        # update component parameters for each repeat
        
        # calculating image start time and durations
        if imaging_method == 'fMRI':
            im_0_start = inter_trial_dur
            im_1_start = inter_trial_dur+im_dur
            im_2_start = inter_trial_dur+im_dur*2
            im_3_start = inter_trial_dur+im_dur*3
            im_4_start = inter_trial_dur+im_dur*4
            trial_dur = im_4_start+im_dur
            catch_start = inter_trial_dur+catch_appears
        else:
            inter_trial_frame = round(inter_trial_dur*expInfo['frameRate'])
            im_0_start = int(inter_trial_frame)
            im_1_start = int(inter_trial_frame+im_dur)
            im_2_start = int(inter_trial_frame+im_dur*2)
            im_3_start = int(inter_trial_frame+im_dur*3)
            im_4_start = int(inter_trial_frame+im_dur*4)
            trial_dur = int(im_4_start+im_dur)
            catch_start = int(inter_trial_frame+catch_appears)
        
        # calculating mu for each image
        im_0_mu = finding_mu(im_0_file, x, y, baseline_lumin)
        im_1_mu = finding_mu(im_1_file, x, y, baseline_lumin)
        im_2_mu = finding_mu(im_2_file, x, y, baseline_lumin)
        im_3_mu = finding_mu(im_3_file, x, y, baseline_lumin)
        im_4_mu = finding_mu(im_4_file, x, y, baseline_lumin)
        
        im_0.setImage(im_0_file)
        im_1.setImage(im_1_file)
        im_2.setImage(im_2_file)
        im_3.setImage(im_3_file)
        im_4.setImage(im_4_file)
        key_resp_trial.keys = []
        key_resp_trial.rt = []
        _key_resp_trial_allKeys = []
        # keep track of which components have finished
        trialComponents = [fixation, im_0, im_1, im_2, im_3, im_4, polygon, key_resp_trial]
        for thisComponent in trialComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "trial"-------
        while continueRoutine:
            # get current time
            t = trialClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=trialClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            if imaging_method == 'fMRI':
                theseKeys = TR_tracker.getKeys(keyList=['5'], waitRelease=False) # Keeping track of TR times
                _TR_tracker_allKeys.extend(theseKeys)
                if len(_TR_tracker_allKeys):
                    _TR_tracker_allKeys = []
                    TR_times.append(core.getTime())
            
            # update/draw components on each frame
            # changing window color to maintain luminance
            if im_0.status == STARTED and im_0.status != FINISHED:
                mu = im_0_mu
            elif im_1.status == STARTED and im_1.status != FINISHED:
                mu = im_1_mu
            elif im_2.status == STARTED and im_2.status != FINISHED:
                mu = im_2_mu
            elif im_3.status == STARTED and im_3.status != FINISHED:
                mu = im_3_mu
            elif im_4.status == STARTED and im_4.status != FINISHED:
                mu = im_4_mu
            else:
                mu = baseline_lumin
            win.color = convert_byte_value(np.random.normal(mu, sigma))
            
            # finishing trial routine
            if im_4.status == FINISHED:
                continueRoutine = False
            
            # Taking screenshot of frame
            if screenshots:
                win.getMovieFrame(buffer='front') # taking screenshot of frame
            
            if imaging_method == 'fMRI':
                # *fixation* updates
                if fixation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    fixation.frameNStart = frameN  # exact frame index
                    fixation.tStart = t  # local t and not account for scr refresh
                    fixation.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(fixation, 'tStartRefresh')  # time at next scr refresh
                    fixation.setAutoDraw(True)
                if fixation.status == STARTED:
                    if tThisFlip >= (fixation.tStart + inter_trial_dur):
                        # keep track of stop time/frame for later
                        fixation.tStop = t  # not accounting for scr refresh
                        fixation.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(fixation, 'tStopRefresh')  # time at next scr refresh
                        fixation.setAutoDraw(False)
                
                # *im_0* updates
                if im_0.status == NOT_STARTED and tThisFlip >= im_0_start-frameTolerance:
                    # keep track of start time/frame for later
                    im_0.frameNStart = frameN  # exact frame index
                    im_0.tStart = t  # local t and not account for scr refresh
                    im_0.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(im_0, 'tStartRefresh')  # time at next scr refresh
                    im_0.setAutoDraw(True)
                    send = True
                    trig = int(trig_0)
                if im_0.status == STARTED:
                    if tThisFlip >= (im_0.tStart + im_dur):
                        # keep track of stop time/frame for later
                        im_0.tStop = t  # not accounting for scr refresh
                        im_0.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(im_0, 'tStopRefresh')  # time at next scr refresh
                        im_0.setAutoDraw(False)
                
                # *im_1* updates
                if im_1.status == NOT_STARTED and tThisFlip >= im_1_start-frameTolerance:
                    # keep track of start time/frame for later
                    im_1.frameNStart = frameN  # exact frame index
                    im_1.tStart = t  # local t and not account for scr refresh
                    im_1.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(im_1, 'tStartRefresh')  # time at next scr refresh
                    im_1.setAutoDraw(True)
                    send = True
                    trig = int(trig_1)
                if im_1.status == STARTED:
                    if tThisFlip >= (im_1.tStart + im_dur):
                        # keep track of stop time/frame for later
                        im_1.tStop = t  # not accounting for scr refresh
                        im_1.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(im_1, 'tStopRefresh')  # time at next scr refresh
                        im_1.setAutoDraw(False)
                
                # *im_2* updates
                if im_2.status == NOT_STARTED and tThisFlip >= im_2_start-frameTolerance:
                    # keep track of start time/frame for later
                    im_2.frameNStart = frameN  # exact frame index
                    im_2.tStart = t  # local t and not account for scr refresh
                    im_2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(im_2, 'tStartRefresh')  # time at next scr refresh
                    im_2.setAutoDraw(True)
                    send = True
                    trig = int(trig_2)
                if im_2.status == STARTED:
                    if tThisFlip >= (im_2.tStart + im_dur):
                        # keep track of stop time/frame for later
                        im_2.tStop = t  # not accounting for scr refresh
                        im_2.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(im_2, 'tStopRefresh')  # time at next scr refresh
                        im_2.setAutoDraw(False)
                
                # *im_3* updates
                if im_3.status == NOT_STARTED and tThisFlip >= im_3_start-frameTolerance:
                    # keep track of start time/frame for later
                    im_3.frameNStart = frameN  # exact frame index
                    im_3.tStart = t  # local t and not account for scr refresh
                    im_3.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(im_3, 'tStartRefresh')  # time at next scr refresh
                    im_3.setAutoDraw(True)
                    send = True
                    trig = int(trig_3)
                if im_3.status == STARTED:
                    if tThisFlip >= (im_3.tStart + im_dur):
                        # keep track of stop time/frame for later
                        im_3.tStop = t  # not accounting for scr refresh
                        im_3.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(im_3, 'tStopRefresh')  # time at next scr refresh
                        im_3.setAutoDraw(False)
                
                # *im_4* updates
                if im_4.status == NOT_STARTED and tThisFlip >= im_4_start-frameTolerance:
                    # keep track of start time/frame for later
                    im_4.frameNStart = frameN  # exact frame index
                    im_4.tStart = t  # local t and not account for scr refresh
                    im_4.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(im_4, 'tStartRefresh')  # time at next scr refresh
                    im_4.setAutoDraw(True)
                    send = True
                    trig = int(trig_4)
                if im_4.status == STARTED:
                    if tThisFlip >= (im_4.tStart + im_dur):
                        # keep track of stop time/frame for later
                        im_4.tStop = t  # not accounting for scr refresh
                        im_4.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(im_4, 'tStopRefresh')  # time at next scr refresh
                        im_4.setAutoDraw(False)
                
                # *polygon* updates
                if polygon.status == NOT_STARTED and tThisFlip >= catch_start-frameTolerance:
                    # keep track of start time/frame for later
                    polygon.frameNStart = frameN  # exact frame index
                    polygon.tStart = t  # local t and not account for scr refresh
                    polygon.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(polygon, 'tStartRefresh')  # time at next scr refresh
                    polygon.setAutoDraw(True)
                if polygon.status == STARTED:
                    if tThisFlip >= (polygon.tStart + catch_dur):
                        # keep track of stop time/frame for later
                        polygon.tStop = t  # not accounting for scr refresh
                        polygon.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(polygon, 'tStopRefresh')  # time at next scr refresh
                        polygon.setAutoDraw(False)
                
                # *key_resp_trial* updates
                waitOnFlip = False
                if key_resp_trial.status == NOT_STARTED and tThisFlip >= catch_start-frameTolerance:
                    # keep track of start time/frame for later
                    key_resp_trial.frameNStart = frameN  # exact frame index
                    key_resp_trial.tStart = t  # local t and not account for scr refresh
                    key_resp_trial.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(key_resp_trial, 'tStartRefresh')  # time at next scr refresh
                    key_resp_trial.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(key_resp_trial.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(key_resp_trial.clearEvents, eventType='keyboard')  # clear events on next screen flip
                if key_resp_trial.status == STARTED:
                    if tThisFlip >= (key_resp_trial.tStart + resp_dur):
                        # keep track of stop time/frame for later
                        key_resp_trial.tStop = t  # not accounting for scr refresh
                        key_resp_trial.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(key_resp_trial, 'tStopRefresh')  # time at next scr refresh
                        key_resp_trial.status = FINISHED
                if key_resp_trial.status == STARTED and not waitOnFlip:
                    theseKeys = key_resp_trial.getKeys(keyList=corr_ans, waitRelease=False)
                    _key_resp_trial_allKeys.extend(theseKeys)
                    if len(_key_resp_trial_allKeys):
                        key_resp_trial.keys = _key_resp_trial_allKeys[-1].name  # just the last key pressed
                        key_resp_trial.rt = _key_resp_trial_allKeys[-1].rt
                        # was this correct?
                        if key_resp_trial.keys in corr_ans:
                            key_resp_trial.corr = 1
                        else:
                            key_resp_trial.corr = 0

            elif imaging_method != 'fMRI':
                # *fixation* updates
                if fixation.status == NOT_STARTED and frameN >= 0.0:
                    # keep track of start time/frame for later
                    fixation.frameNStart = frameN  # exact frame index
                    fixation.tStart = t  # local t and not account for scr refresh
                    fixation.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(fixation, 'tStartRefresh')  # time at next scr refresh
                    fixation.setAutoDraw(True)
                if fixation.status == STARTED:
                    if frameN >= (fixation.frameNStart + inter_trial_frame):
                        # keep track of stop time/frame for later
                        fixation.tStop = t  # not accounting for scr refresh
                        fixation.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(fixation, 'tStopRefresh')  # time at next scr refresh
                        fixation.setAutoDraw(False)
                
                # *im_0* updates
                if im_0.status == NOT_STARTED and frameN >= im_0_start:
                    # keep track of start time/frame for later
                    im_0.frameNStart = frameN  # exact frame index
                    im_0.tStart = t  # local t and not account for scr refresh
                    im_0.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(im_0, 'tStartRefresh')  # time at next scr refresh
                    im_0.setAutoDraw(True)
                    send = True
                    trig = int(trig_0)
                if im_0.status == STARTED:
                    if frameN >= (im_0.frameNStart + im_dur):
                        # keep track of stop time/frame for later
                        im_0.tStop = t  # not accounting for scr refresh
                        im_0.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(im_0, 'tStopRefresh')  # time at next scr refresh
                        im_0.setAutoDraw(False)
                
                # *im_1* updates
                if im_1.status == NOT_STARTED and frameN >= im_1_start:
                    # keep track of start time/frame for later
                    im_1.frameNStart = frameN  # exact frame index
                    im_1.tStart = t  # local t and not account for scr refresh
                    im_1.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(im_1, 'tStartRefresh')  # time at next scr refresh
                    im_1.setAutoDraw(True)
                    send = True
                    trig = int(trig_1)
                if im_1.status == STARTED:
                    if frameN >= (im_1.frameNStart + im_dur):
                        # keep track of stop time/frame for later
                        im_1.tStop = t  # not accounting for scr refresh
                        im_1.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(im_1, 'tStopRefresh')  # time at next scr refresh
                        im_1.setAutoDraw(False)
                
                # *im_2* updates
                if im_2.status == NOT_STARTED and frameN >= im_2_start:
                    # keep track of start time/frame for later
                    im_2.frameNStart = frameN  # exact frame index
                    im_2.tStart = t  # local t and not account for scr refresh
                    im_2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(im_2, 'tStartRefresh')  # time at next scr refresh
                    im_2.setAutoDraw(True)
                    send = True
                    trig = int(trig_2)
                if im_2.status == STARTED:
                    if frameN >= (im_2.frameNStart + im_dur):
                        # keep track of stop time/frame for later
                        im_2.tStop = t  # not accounting for scr refresh
                        im_2.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(im_2, 'tStopRefresh')  # time at next scr refresh
                        im_2.setAutoDraw(False)
                
                # *im_3* updates
                if im_3.status == NOT_STARTED and frameN >= im_3_start:
                    # keep track of start time/frame for later
                    im_3.frameNStart = frameN  # exact frame index
                    im_3.tStart = t  # local t and not account for scr refresh
                    im_3.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(im_3, 'tStartRefresh')  # time at next scr refresh
                    im_3.setAutoDraw(True)
                    send = True
                    trig = int(trig_3)
                if im_3.status == STARTED:
                    if frameN >= (im_3.frameNStart + im_dur):
                        # keep track of stop time/frame for later
                        im_3.tStop = t  # not accounting for scr refresh
                        im_3.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(im_3, 'tStopRefresh')  # time at next scr refresh
                        im_3.setAutoDraw(False)
                
                # *im_4* updates
                if im_4.status == NOT_STARTED and frameN >= im_4_start:
                    # keep track of start time/frame for later
                    im_4.frameNStart = frameN  # exact frame index
                    im_4.tStart = t  # local t and not account for scr refresh
                    im_4.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(im_4, 'tStartRefresh')  # time at next scr refresh
                    im_4.setAutoDraw(True)
                    send = True
                    trig = int(trig_4)
                if im_4.status == STARTED:
                    if frameN >= (im_4.frameNStart + im_dur):
                        # keep track of stop time/frame for later
                        im_4.tStop = t  # not accounting for scr refresh
                        im_4.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(im_4, 'tStopRefresh')  # time at next scr refresh
                        im_4.setAutoDraw(False)
                
                # *polygon* updates
                if polygon.status == NOT_STARTED and frameN >= catch_start:
                    # keep track of start time/frame for later
                    polygon.frameNStart = frameN  # exact frame index
                    polygon.tStart = t  # local t and not account for scr refresh
                    polygon.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(polygon, 'tStartRefresh')  # time at next scr refresh
                    polygon.setAutoDraw(True)
                if polygon.status == STARTED:
                    if frameN >= (polygon.frameNStart + catch_dur):
                        # keep track of stop time/frame for later
                        polygon.tStop = t  # not accounting for scr refresh
                        polygon.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(polygon, 'tStopRefresh')  # time at next scr refresh
                        polygon.setAutoDraw(False)
                
                # *key_resp_trial* updates
                waitOnFlip = False
                if key_resp_trial.status == NOT_STARTED and frameN >= catch_start:
                    # keep track of start time/frame for later
                    key_resp_trial.frameNStart = frameN  # exact frame index
                    key_resp_trial.tStart = t  # local t and not account for scr refresh
                    key_resp_trial.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(key_resp_trial, 'tStartRefresh')  # time at next scr refresh
                    key_resp_trial.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(key_resp_trial.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(key_resp_trial.clearEvents, eventType='keyboard')  # clear events on next screen flip
                if key_resp_trial.status == STARTED:
                    if frameN >= (key_resp_trial.frameNStart + resp_dur):
                        # keep track of stop time/frame for later
                        key_resp_trial.tStop = t  # not accounting for scr refresh
                        key_resp_trial.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(key_resp_trial, 'tStopRefresh')  # time at next scr refresh
                        key_resp_trial.status = FINISHED
                if key_resp_trial.status == STARTED and not waitOnFlip:
                    theseKeys = key_resp_trial.getKeys(keyList=corr_ans, waitRelease=False)
                    _key_resp_trial_allKeys.extend(theseKeys)
                    if len(_key_resp_trial_allKeys):
                        key_resp_trial.keys = _key_resp_trial_allKeys[-1].name  # just the last key pressed
                        key_resp_trial.rt = _key_resp_trial_allKeys[-1].rt
                        # was this correct?
                        if key_resp_trial.keys in corr_ans:
                            key_resp_trial.corr = 1
                        else:
                            key_resp_trial.corr = 0
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
                if imaging_method != 'fMRI':
                    if send:
                        send = send_trigger(trig, port, send)
                        if trig == trig_4:
                            trig_4_time = core.getTime() # keeps track of when the trigger was sent
                    else:
                        send_trigger(port=port) # resets pins to zero
        
        # -------Ending Routine "trial"-------
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
        # saving screenshots
        if screenshots:
            win.saveMovieFrames('screenshots//frame.tif')
        
        trials.addData('fixation.started', fixation.tStartRefresh)
        trials.addData('fixation.stopped', fixation.tStopRefresh)
        trials.addData('im_0.started', im_0.tStartRefresh)
        trials.addData('im_0.stopped', im_0.tStopRefresh)
        trials.addData('im_1.started', im_1.tStartRefresh)
        trials.addData('im_1.stopped', im_1.tStopRefresh)
        trials.addData('im_2.started', im_2.tStartRefresh)
        trials.addData('im_2.stopped', im_2.tStopRefresh)
        trials.addData('im_3.started', im_3.tStartRefresh)
        trials.addData('im_3.stopped', im_3.tStopRefresh)
        trials.addData('im_4.started', im_4.tStartRefresh)
        if imaging_method != 'fMRI':
            trials.addData('trig_4_time', trig_4_time)
        trials.addData('polygon.started', polygon.tStartRefresh)
        trials.addData('polygon.stopped', polygon.tStopRefresh)
        
        # check responses
        if key_resp_trial.keys in ['', [], None]:  # No response was made
            key_resp_trial.keys = None
            if catch_dur == 0:
                key_resp_trial.corr = 1;  # correct non-response
            else:
                key_resp_trial.corr = 0;
        else:
            if catch_dur == 0:
                key_resp_trial.corr = 0;  # failed to respond (incorrectly)
            else:
                key_resp_trial.corr = 1;
        
        # store data for trials (TrialHandler)
        trials.addData('key_resp_trial.keys',key_resp_trial.keys)
        trials.addData('key_resp_trial.corr', key_resp_trial.corr)
        if key_resp_trial.keys != None:  # we had a response
            trials.addData('key_resp_trial.rt', key_resp_trial.rt)
        trials.addData('key_resp_trial.started', key_resp_trial.tStartRefresh)
        trials.addData('key_resp_trial.stopped', key_resp_trial.tStopRefresh)
        # the Routine "trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 1 repeats of 'trials'
    
    
    # ------Prepare to start Routine "rest"-------
    continueRoutine = True
    # update component parameters for each repeat
    
    if imaging_method == 'fMRI':
        continueRoutine = False
        
    if rest_n > 3:
        continueRoutine = False
        rest_n += 1
    
    key_resp_rest.keys = []
    key_resp_rest.rt = []
    _key_resp_rest_allKeys = []
    # keep track of which components have finished
    restComponents = [text_rest, key_resp_rest]
    for thisComponent in restComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    restClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "rest"-------
    while continueRoutine:
        # get current time
        t = restClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=restClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_rest* updates
        if text_rest.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_rest.frameNStart = frameN  # exact frame index
            text_rest.tStart = t  # local t and not account for scr refresh
            text_rest.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_rest, 'tStartRefresh')  # time at next scr refresh
            text_rest.setAutoDraw(True)
        
        # *key_resp_rest* updates
        waitOnFlip = False
        if key_resp_rest.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_rest.frameNStart = frameN  # exact frame index
            key_resp_rest.tStart = t  # local t and not account for scr refresh
            key_resp_rest.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_rest, 'tStartRefresh')  # time at next scr refresh
            key_resp_rest.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_rest.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_rest.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_rest.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_rest.getKeys(keyList=corr_ans, waitRelease=False)
            _key_resp_rest_allKeys.extend(theseKeys)
            if len(_key_resp_rest_allKeys):
                key_resp_rest.keys = _key_resp_rest_allKeys[-1].name  # just the last key pressed
                key_resp_rest.rt = _key_resp_rest_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in restComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "rest"-------
    for thisComponent in restComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp_rest.keys in ['', [], None]:  # No response was made
        key_resp_rest.keys = None
    # the Routine "rest" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1 repeats of 'blocks'


# ------Prepare to start Routine "finish"-------
continueRoutine = True
# update component parameters for each repeat
key_resp_finish.keys = []
key_resp_finish.rt = []
_key_resp_finish_allKeys = []
# keep track of which components have finished
finishComponents = [text_finish, key_resp_finish]
for thisComponent in finishComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
finishClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "finish"-------
while continueRoutine:
    # get current time
    t = finishClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=finishClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_finish* updates
    if text_finish.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_finish.frameNStart = frameN  # exact frame index
        text_finish.tStart = t  # local t and not account for scr refresh
        text_finish.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_finish, 'tStartRefresh')  # time at next scr refresh
        text_finish.setAutoDraw(True)
    
    # *key_resp_finish* updates
    waitOnFlip = False
    if key_resp_finish.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        key_resp_finish.frameNStart = frameN  # exact frame index
        key_resp_finish.tStart = t  # local t and not account for scr refresh
        key_resp_finish.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_finish, 'tStartRefresh')  # time at next scr refresh
        key_resp_finish.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_finish.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_finish.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_finish.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_finish.getKeys(keyList=corr_ans, waitRelease=False)
        _key_resp_finish_allKeys.extend(theseKeys)
        if len(_key_resp_finish_allKeys):
            key_resp_finish.keys = _key_resp_finish_allKeys[-1].name  # just the last key pressed
            key_resp_finish.rt = _key_resp_finish_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in finishComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "finish"-------
for thisComponent in finishComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_finish.keys in ['', [], None]:  # No response was made
    key_resp_finish.keys = None
thisExp.nextEntry()
# the Routine "finish" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
# outputting TR times
if imaging_method == 'fMRI':
    TR_times = pd.DataFrame(data=np.array(TR_times), columns=['Time'])
    if os.path.isdir('TR_times') == False:
        os.mkdir('TR_times')
    TR_times.to_csv('TR_times//{}_{}_TR_times_{}.csv'.format(expInfo['participant'], expInfo['session'], expInfo['date']))
core.quit()