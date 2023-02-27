#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.2.5),
    on Mon Feb 27 01:19:57 2023
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
prefs.hardware['audioLib'] = 'ptb'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard



# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2022.2.5'
expName = 'ene_pupil_1_0'  # from the Builder filename that created this script
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
}
# --- Show participant info dialog --
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation
# Make folder to store recordings from mic
micRecFolder = filename + '_mic_recorded'
if not os.path.isdir(micRecFolder):
    os.mkdir(micRecFolder)

# --- Setup the Window ---
win = visual.Window(
    size=[1000, 800], fullscr=False, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
win.mouseVisible = True
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess
# --- Setup input devices ---
ioConfig = {}
ioSession = ioServer = eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='ptb')

# --- Initialize components for Routine "waiting_instructions" ---
text_instr = visual.TextStim(win=win, name='text_instr',
    text="This is a template" + " \n on how to use" + "\n the text component" + " \n to present instructions.",
    font='Arial',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
key_resp = keyboard.Keyboard()

# --- Initialize components for Routine "fixate" ---
fixation_circle = visual.ShapeStim(
    win=win, name='fixation_circle',units='deg', 
    size=(1.0, 1.0), vertices='circle',
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=0.0,     colorSpace='rgb',  lineColor='black', fillColor='black',
    opacity=None, depth=0.0, interpolate=True)
fixation_cross_cardinal = visual.ShapeStim(
    win=win, name='fixation_cross_cardinal', vertices='cross',units='deg', 
    size=(1.0, 1.0),
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=0.25,     colorSpace='rgb',  lineColor='grey', fillColor='grey',
    opacity=None, depth=0.0, interpolate=True)
fixation_cross_rotated = visual.ShapeStim(
    win=win, name='fixation_cross_rotated', vertices='cross',units='deg', 
    size=(1.0, 1.0),
    ori=45.0, pos=(0, 0), anchor='center',
    lineWidth=0.25,     colorSpace='rgb',  lineColor='grey', fillColor='grey',
    opacity=None, depth=0.0, interpolate=True)
fixation_dot = visual.ShapeStim(
    win=win, name='fixation_dot',units='deg', 
    size=(0.18, 0.18), vertices='circle',
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=0.0,     colorSpace='rgb',  lineColor='black', fillColor='black',
    opacity=None, depth=0.0, interpolate=True)

fixation_cardinal = [fixation_circle, fixation_cross_cardinal, fixation_dot]
fixation_rotated = [fixation_circle, fixation_cross_rotated, fixation_dot]

def draw_fixation(shapes,
                  tThisFlip,
                  frameN,
                  tThisFlipGlobal,
                  frameTolerance=frameTolerance,
                  win=win):
    for _, x in enumerate(shapes):
        if x.status == NOT_STARTED and tThisFlip >= 0.7-frameTolerance:
            # keep track of start time/frame for later
            x.frameNStart = frameN  # exact frame index
            x.tStart = t  # local t and not account for scr refresh
            x.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(x, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, x.name + '.started')
            x.setAutoDraw(True)

fixation_placeholder = keyboard.Keyboard()

# --- Initialize components for Routine "question" ---
fixation_prepare = visual.ShapeStim(
    win=win, name='fixation_prepare', vertices='cross',units='deg', 
    size=(1.0, 1.0),
    ori=45.0, pos=(0, 0), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor='black', fillColor='black',
    opacity=None, depth=-1.0, interpolate=True)
fixation_question = visual.ShapeStim(
    win=win, name='fixation_question', vertices='cross',units='deg', 
    size=(1.0, 1.0),
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor='black', fillColor='black',
    opacity=None, depth=-2.0, interpolate=True)
static_prepare = clock.StaticPeriod(win=win, screenHz=expInfo['frameRate'], name='static_prepare')
question_voice = sound.Sound('A', secs=-1, stereo=True, hamming=True,
    name='question_voice')
question_voice.setVolume(1.0)
duration_voice = sound.Sound('A', secs=-1, stereo=True, hamming=True,
    name='duration_voice')
duration_voice.setVolume(1.0)
choice = keyboard.Keyboard()

# --- Initialize components for Routine "answer" ---
fixation_wait = visual.ShapeStim(
    win=win, name='fixation_wait', vertices='cross',units='deg', 
    size=(1.0, 1.0),
    ori=45.0, pos=(0, 0), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor='green', fillColor='green',
    opacity=None, depth=-1.0, interpolate=True)
fixation_answer = visual.ShapeStim(
    win=win, name='fixation_answer', vertices='cross',units='deg', 
    size=(1.0, 1.0),
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor='red', fillColor='red',
    opacity=None, depth=-2.0, interpolate=True)
answer_voice = sound.Sound('A', secs=-1, stereo=True, hamming=True,
    name='answer_voice')
answer_voice.setVolume(1.0)
fixation_satisfaction = visual.ShapeStim(
    win=win, name='fixation_satisfaction', vertices='cross',units='deg', 
    size=(1.0, 1.0),
    ori=45.0, pos=(0, 0), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor='blue', fillColor='blue',
    opacity=None, depth=-4.0, interpolate=True)
mic = sound.microphone.Microphone(
    device=None, channels=None, 
    sampleRateHz=48000, maxRecordingSize=24000.0
)
static_wait = clock.StaticPeriod(win=win, screenHz=expInfo['frameRate'], name='static_wait')

# --- Initialize components for Routine "rating" ---
text = visual.TextStim(win=win, name='text',
    text='',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
slider = visual.Slider(win=win, name='slider',
    startValue=None, size=(12.0, 1.0), pos=(0, -3.4), units='deg',
    labels=("Know", "1", "2", "3", "4", "5"), ticks=(0, 1, 2, 3, 4, 5), granularity=1.0,
    style='rating', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=1.0,
    flip=False, ori=0.0, depth=-1, readOnly=False)

# --- Initialize components for Routine "demog" ---
age = visual.TextStim(win=win, name='age',
    text='What age group are you in?',
    font='Arial',
    pos=(-0.5, 0.45), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
respAge = visual.Slider(win=win, name='respAge',
    startValue=None, size=(0.9, 0.015), pos=(-0.1, 0.4), units=None,
    labels=("Under 16", "16-20", "21-25", "26-30", "31-35", "36-40", "Above 40"), ticks=(1, 2, 3, 4, 5, 6, 7), granularity=1.0,
    style='radio', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Arial', labelHeight=0.035,
    flip=False, ori=0.0, depth=-1, readOnly=False)
gender = visual.TextStim(win=win, name='gender',
    text='What gender are you?',
    font='Arial',
    pos=(-0.5, 0.3), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
genderResp1 = visual.Slider(win=win, name='genderResp1',
    startValue=None, size=(0.015, 0.15), pos=(-0.5, 0.15), units=None,
    labels=("Prefer not to say", "In another way", "Non-binary", "Man", "Woman"), ticks=(1, 2, 3, 4, 5), granularity=1.0,
    style='radio', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Arial', labelHeight=0.035,
    flip=True, ori=0.0, depth=-3, readOnly=False)
genderResp2 = visual.TextBox2(
     win, text=None, font='Arial',
     pos=(0.135, 0.11),     letterHeight=0.025,
     size=(0.425, 0.04), borderWidth=2.0,
     color='black', colorSpace='rgb',
     opacity=None,
     bold=False, italic=False,
     lineSpacing=1.0,
     padding=0.0, alignment='center',
     anchor='center-left',
     fillColor='white', borderColor=None,
     flipHoriz=False, flipVert=False, languageStyle='LTR',
     editable=True,
     name='genderResp2',
     autoLog=True,
)
student = visual.TextStim(win=win, name='student',
    text='Are you a student?',
    font='Arial',
    pos=(-0.55, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-5.0);
studentResp = visual.Slider(win=win, name='studentResp',
    startValue=None, size=(1.1, 0.02), pos=(0, -0.05), units=None,
    labels=("Undergraduate", "Taught postgraduate", "Research postgraduate", "No"), ticks=(1, 2, 3, 4), granularity=1.0,
    style='radio', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Arial', labelHeight=0.035,
    flip=False, ori=0.0, depth=-6, readOnly=False)
mood = visual.TextStim(win=win, name='mood',
    text='What is your current mood?',
    font='Arial',
    pos=(-0.45, -0.15), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-7.0);
moodResp = visual.Slider(win=win, name='moodResp',
    startValue=None, size=(1.1, 0.02), pos=(-0.1, -0.2), units=None,
    labels=("Low", "Okay", "Great!"), ticks=(1, 2, 3), granularity=0.0,
    style='rating', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Arial', labelHeight=0.03,
    flip=False, ori=0.0, depth=-8, readOnly=False)
nextButton = visual.ImageStim(
    win=win,
    name='nextButton', 
    image='next.png', mask=None, anchor='center',
    ori=0.0, pos=(0, -0.4), size=(0.15, 0.075),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-9.0)
mouse = event.Mouse(win=win)
x, y = [None, None]
mouse.mouseClock = core.Clock()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

# --- Prepare to start Routine "waiting_instructions" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
key_resp.keys = []
key_resp.rt = []
_key_resp_allKeys = []
# keep track of which components have finished
waiting_instructionsComponents = [text_instr, key_resp]
for thisComponent in waiting_instructionsComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "waiting_instructions" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_instr* updates
    if text_instr.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_instr.frameNStart = frameN  # exact frame index
        text_instr.tStart = t  # local t and not account for scr refresh
        text_instr.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_instr, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'text_instr.started')
        text_instr.setAutoDraw(True)
    
    # *key_resp* updates
    waitOnFlip = False
    if key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        key_resp.frameNStart = frameN  # exact frame index
        key_resp.tStart = t  # local t and not account for scr refresh
        key_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'key_resp.started')
        key_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp.status == STARTED and not waitOnFlip:
        theseKeys = key_resp.getKeys(keyList=['space'], waitRelease=False)
        _key_resp_allKeys.extend(theseKeys)
        if len(_key_resp_allKeys):
            key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
            key_resp.rt = _key_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in waiting_instructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "waiting_instructions" ---
for thisComponent in waiting_instructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp.keys in ['', [], None]:  # No response was made
    key_resp.keys = None
thisExp.addData('key_resp.keys',key_resp.keys)
if key_resp.keys != None:  # we had a response
    thisExp.addData('key_resp.rt', key_resp.rt)
thisExp.nextEntry()
# the Routine "waiting_instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
waiting_trials = data.TrialHandler(nReps=1.0, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('stimuli/questions.csv'),
    seed=None, name='waiting_trials')
thisExp.addLoop(waiting_trials)  # add the loop to the experiment
thisWaiting_trial = waiting_trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisWaiting_trial.rgb)
if thisWaiting_trial != None:
    for paramName in thisWaiting_trial:
        exec('{} = thisWaiting_trial[paramName]'.format(paramName))

for thisWaiting_trial in waiting_trials:
    currentLoop = waiting_trials
    # abbreviate parameter names if possible (e.g. rgb = thisWaiting_trial.rgb)
    if thisWaiting_trial != None:
        for paramName in thisWaiting_trial:
            exec('{} = thisWaiting_trial[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "fixate" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    fixation_placeholder.keys = []
    fixation_placeholder.rt = []
    _fixation_placeholder_allKeys = []
    # keep track of which components have finished
    fixateComponents = [fixation_placeholder] + fixation_cardinal
    for thisComponent in fixateComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "fixate" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fixation* updates
        draw_fixation(fixation_cardinal, 
                      tThisFlip,
                      frameN,
                      tThisFlipGlobal)
                    
        # *fixation_placeholder* updates
        waitOnFlip = False
        if fixation_placeholder.status == NOT_STARTED and tThisFlip >= 0.7 -frameTolerance:
            # keep track of start time/frame for later
            fixation_placeholder.frameNStart = frameN  # exact frame index
            fixation_placeholder.tStart = t  # local t and not account for scr refresh
            fixation_placeholder.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fixation_placeholder, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'fixation_placeholder.started')
            fixation_placeholder.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(fixation_placeholder.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(fixation_placeholder.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if fixation_placeholder.status == STARTED and not waitOnFlip:
            theseKeys = fixation_placeholder.getKeys(keyList=['space'], waitRelease=False)
            _fixation_placeholder_allKeys.extend(theseKeys)
            if len(_fixation_placeholder_allKeys):
                fixation_placeholder.keys = _fixation_placeholder_allKeys[-1].name  # just the last key pressed
                fixation_placeholder.rt = _fixation_placeholder_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in fixateComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "fixate" ---
    for thisComponent in fixateComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if fixation_placeholder.keys in ['', [], None]:  # No response was made
        fixation_placeholder.keys = None
    waiting_trials.addData('fixation_placeholder.keys',fixation_placeholder.keys)
    if fixation_placeholder.keys != None:  # we had a response
        waiting_trials.addData('fixation_placeholder.rt', fixation_placeholder.rt)
    # the Routine "fixate" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "question" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code
    thisTrialDuration = [3, 6, 9, 12][randint(0,4)]
    thisExp.addData('wait_duration', thisTrialDuration)
    
    question_voice.setSound('stimuli/' + question_file, hamming=True)
    question_voice.setVolume(1.0, log=False)
    duration_voice.setSound('stimuli/' + str(thisTrialDuration) + 's.ogg', hamming=True)
    duration_voice.setVolume(1.0, log=False)
    choice.keys = []
    choice.rt = []
    _choice_allKeys = []
    # keep track of which components have finished
    questionComponents = [fixation_prepare, fixation_question, static_prepare, question_voice, duration_voice, choice]
    for thisComponent in questionComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "question" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fixation_prepare* updates
        if fixation_prepare.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            fixation_prepare.frameNStart = frameN  # exact frame index
            fixation_prepare.tStart = t  # local t and not account for scr refresh
            fixation_prepare.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fixation_prepare, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'fixation_prepare.started')
            fixation_prepare.setAutoDraw(True)
        if fixation_prepare.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fixation_prepare.tStartRefresh + 2.0-frameTolerance:
                # keep track of stop time/frame for later
                fixation_prepare.tStop = t  # not accounting for scr refresh
                fixation_prepare.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation_prepare.stopped')
                fixation_prepare.setAutoDraw(False)
        
        # *fixation_question* updates
        if fixation_question.status == NOT_STARTED and tThisFlip >= 2.0-frameTolerance:
            # keep track of start time/frame for later
            fixation_question.frameNStart = frameN  # exact frame index
            fixation_question.tStart = t  # local t and not account for scr refresh
            fixation_question.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fixation_question, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'fixation_question.started')
            fixation_question.setAutoDraw(True)
        # start/stop question_voice
        if question_voice.status == NOT_STARTED and tThisFlip >= 2.0-frameTolerance:
            # keep track of start time/frame for later
            question_voice.frameNStart = frameN  # exact frame index
            question_voice.tStart = t  # local t and not account for scr refresh
            question_voice.tStartRefresh = tThisFlipGlobal  # on global time
            # add timestamp to datafile
            thisExp.addData('question_voice.started', tThisFlipGlobal)
            question_voice.play(when=win)  # sync with win flip
        # start/stop duration_voice
        if duration_voice.status == NOT_STARTED and tThisFlip >= 2.0 + question_voice.duration + 0.2-frameTolerance:
            # keep track of start time/frame for later
            duration_voice.frameNStart = frameN  # exact frame index
            duration_voice.tStart = t  # local t and not account for scr refresh
            duration_voice.tStartRefresh = tThisFlipGlobal  # on global time
            # add timestamp to datafile
            thisExp.addData('duration_voice.started', tThisFlipGlobal)
            duration_voice.play(when=win)  # sync with win flip
        
        # *choice* updates
        waitOnFlip = False
        if choice.status == NOT_STARTED and tThisFlip >= 2.0 + question_voice.duration + duration_voice.duration / 2-frameTolerance:
            # keep track of start time/frame for later
            choice.frameNStart = frameN  # exact frame index
            choice.tStart = t  # local t and not account for scr refresh
            choice.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(choice, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'choice.started')
            choice.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(choice.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(choice.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if choice.status == STARTED and not waitOnFlip:
            theseKeys = choice.getKeys(keyList=['d','g','j'], waitRelease=False)
            _choice_allKeys.extend(theseKeys)
            if len(_choice_allKeys):
                choice.keys = _choice_allKeys[-1].name  # just the last key pressed
                choice.rt = _choice_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        # *static_prepare* period
        if static_prepare.status == NOT_STARTED and t >= 0-frameTolerance:
            # keep track of start time/frame for later
            static_prepare.frameNStart = frameN  # exact frame index
            static_prepare.tStart = t  # local t and not account for scr refresh
            static_prepare.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(static_prepare, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData('static_prepare.started', t)
            static_prepare.start(2)
        elif static_prepare.status == STARTED:  # one frame should pass before updating params and completing
            # Updating other components during *static_prepare*
            question_voice.setSound('stimuli/' + question_file, secs=-1)
            duration_voice.setSound('stimuli/' + str(thisTrialDuration) + 's.ogg', secs=-1)
            # Component updates done
            static_prepare.complete()  # finish the static period
            static_prepare.tStop = static_prepare.tStart + 2  # record stop time
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in questionComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "question" ---
    for thisComponent in questionComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    question_voice.stop()  # ensure sound has stopped at end of routine
    duration_voice.stop()  # ensure sound has stopped at end of routine
    # check responses
    if choice.keys in ['', [], None]:  # No response was made
        choice.keys = None
    waiting_trials.addData('choice.keys',choice.keys)
    if choice.keys != None:  # we had a response
        waiting_trials.addData('choice.rt', choice.rt)
    # the Routine "question" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "answer" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    # Run 'Begin Routine' code from conditional_answer
    if choice.keys != 'd':
        continueRoutine = False
    answer_voice.setSound('./stimuli/' + answer_file, hamming=True)
    answer_voice.setVolume(1.0, log=False)
    # keep track of which components have finished
    answerComponents = [fixation_wait, fixation_answer, answer_voice, fixation_satisfaction, mic, static_wait]
    for thisComponent in answerComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "answer" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fixation_wait* updates
        if fixation_wait.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            fixation_wait.frameNStart = frameN  # exact frame index
            fixation_wait.tStart = t  # local t and not account for scr refresh
            fixation_wait.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fixation_wait, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'fixation_wait.started')
            fixation_wait.setAutoDraw(True)
        if fixation_wait.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fixation_wait.tStartRefresh + thisTrialDuration-frameTolerance:
                # keep track of stop time/frame for later
                fixation_wait.tStop = t  # not accounting for scr refresh
                fixation_wait.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation_wait.stopped')
                fixation_wait.setAutoDraw(False)
        
        # *fixation_answer* updates
        if fixation_answer.status == NOT_STARTED and tThisFlip >= thisTrialDuration-frameTolerance:
            # keep track of start time/frame for later
            fixation_answer.frameNStart = frameN  # exact frame index
            fixation_answer.tStart = t  # local t and not account for scr refresh
            fixation_answer.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fixation_answer, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'fixation_answer.started')
            fixation_answer.setAutoDraw(True)
        if fixation_answer.status == STARTED:
            # is it time to stop? (based on local clock)
            if tThisFlip > thisTrialDuration + answer_voice.duration-frameTolerance:
                # keep track of stop time/frame for later
                fixation_answer.tStop = t  # not accounting for scr refresh
                fixation_answer.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation_answer.stopped')
                fixation_answer.setAutoDraw(False)
        # start/stop answer_voice
        if answer_voice.status == NOT_STARTED and tThisFlip >= thisTrialDuration-frameTolerance:
            # keep track of start time/frame for later
            answer_voice.frameNStart = frameN  # exact frame index
            answer_voice.tStart = t  # local t and not account for scr refresh
            answer_voice.tStartRefresh = tThisFlipGlobal  # on global time
            # add timestamp to datafile
            thisExp.addData('answer_voice.started', tThisFlipGlobal)
            answer_voice.play(when=win)  # sync with win flip
        
        # *fixation_satisfaction* updates
        if fixation_satisfaction.status == NOT_STARTED and tThisFlip >= thisTrialDuration + answer_voice.duration-frameTolerance:
            # keep track of start time/frame for later
            fixation_satisfaction.frameNStart = frameN  # exact frame index
            fixation_satisfaction.tStart = t  # local t and not account for scr refresh
            fixation_satisfaction.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fixation_satisfaction, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'fixation_satisfaction.started')
            fixation_satisfaction.setAutoDraw(True)
        if fixation_satisfaction.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fixation_satisfaction.tStartRefresh + 3.0-frameTolerance:
                # keep track of stop time/frame for later
                fixation_satisfaction.tStop = t  # not accounting for scr refresh
                fixation_satisfaction.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation_satisfaction.stopped')
                fixation_satisfaction.setAutoDraw(False)
        
        # mic updates
        if mic.status == NOT_STARTED and t >= thisTrialDuration + answer_voice.duration-frameTolerance:
            # keep track of start time/frame for later
            mic.frameNStart = frameN  # exact frame index
            mic.tStart = t  # local t and not account for scr refresh
            mic.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mic, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData('mic.started', t)
            # start recording with mic
            mic.start()
            mic.status = STARTED
        if mic.status == STARTED:
            # update recorded clip for mic
            mic.poll()
        if mic.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > mic.tStartRefresh + 3.0-frameTolerance:
                # keep track of stop time/frame for later
                mic.tStop = t  # not accounting for scr refresh
                mic.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.addData('mic.stopped', t)
                # stop recording with mic
                mic.stop()
                mic.status = FINISHED
        # *static_wait* period
        if static_wait.status == NOT_STARTED and t >= 0-frameTolerance:
            # keep track of start time/frame for later
            static_wait.frameNStart = frameN  # exact frame index
            static_wait.tStart = t  # local t and not account for scr refresh
            static_wait.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(static_wait, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData('static_wait.started', t)
            static_wait.start(thisTrialDuration)
        elif static_wait.status == STARTED:  # one frame should pass before updating params and completing
            # Updating other components during *static_wait*
            answer_voice.setSound('./stimuli/' + answer_file, secs=-1)
            # Component updates done
            static_wait.complete()  # finish the static period
            static_wait.tStop = static_wait.tStart + thisTrialDuration  # record stop time
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in answerComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "answer" ---
    for thisComponent in answerComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    answer_voice.stop()  # ensure sound has stopped at end of routine
    # tell mic to keep hold of current recording in mic.clips and transcript (if applicable) in mic.scripts
    # this will also update mic.lastClip and mic.lastScript
    mic.stop()
    tag = data.utils.getDateStr()
    micClip = mic.bank(
        tag=tag, transcribe='None',
        config=None
    )
    waiting_trials.addData('mic.clip', os.path.join(micRecFolder, 'recording_mic_%s.wav' % tag))
    # the Routine "answer" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1.0 repeats of 'waiting_trials'


# set up handler to look after randomisation of conditions etc
rating_trials = data.TrialHandler(nReps=1.0, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('stimuli/questions.csv'),
    seed=None, name='rating_trials')
thisExp.addLoop(rating_trials)  # add the loop to the experiment
thisRating_trial = rating_trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisRating_trial.rgb)
if thisRating_trial != None:
    for paramName in thisRating_trial:
        exec('{} = thisRating_trial[paramName]'.format(paramName))

for thisRating_trial in rating_trials:
    currentLoop = rating_trials
    # abbreviate parameter names if possible (e.g. rgb = thisRating_trial.rgb)
    if thisRating_trial != None:
        for paramName in thisRating_trial:
            exec('{} = thisRating_trial[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "rating" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    text.setText("How curious are you to know: \n" + question_text)
    slider.reset()
    # keep track of which components have finished
    ratingComponents = [text, slider]
    for thisComponent in ratingComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "rating" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text* updates
        if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text.frameNStart = frameN  # exact frame index
            text.tStart = t  # local t and not account for scr refresh
            text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text.started')
            text.setAutoDraw(True)
        
        # *slider* updates
        if slider.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            slider.frameNStart = frameN  # exact frame index
            slider.tStart = t  # local t and not account for scr refresh
            slider.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(slider, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'slider.started')
            slider.setAutoDraw(True)
        
        # Check slider for response to end routine
        if slider.getRating() is not None and slider.status == STARTED:
            continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in ratingComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "rating" ---
    for thisComponent in ratingComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    rating_trials.addData('slider.response', slider.getRating())
    rating_trials.addData('slider.rt', slider.getRT())
    # the Routine "rating" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1.0 repeats of 'rating_trials'


# --- Prepare to start Routine "demog" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
respAge.reset()
genderResp1.reset()
genderResp2.reset()
studentResp.reset()
moodResp.reset()
# setup some python lists for storing info about the mouse
mouse.clicked_name = []
gotValidClick = False  # until a click is received
# keep track of which components have finished
demogComponents = [age, respAge, gender, genderResp1, genderResp2, student, studentResp, mood, moodResp, nextButton, mouse]
for thisComponent in demogComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "demog" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *age* updates
    if age.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        age.frameNStart = frameN  # exact frame index
        age.tStart = t  # local t and not account for scr refresh
        age.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(age, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'age.started')
        age.setAutoDraw(True)
    
    # *respAge* updates
    if respAge.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        respAge.frameNStart = frameN  # exact frame index
        respAge.tStart = t  # local t and not account for scr refresh
        respAge.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(respAge, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'respAge.started')
        respAge.setAutoDraw(True)
    
    # *gender* updates
    if gender.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        gender.frameNStart = frameN  # exact frame index
        gender.tStart = t  # local t and not account for scr refresh
        gender.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(gender, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'gender.started')
        gender.setAutoDraw(True)
    
    # *genderResp1* updates
    if genderResp1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        genderResp1.frameNStart = frameN  # exact frame index
        genderResp1.tStart = t  # local t and not account for scr refresh
        genderResp1.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(genderResp1, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'genderResp1.started')
        genderResp1.setAutoDraw(True)
    
    # *genderResp2* updates
    if genderResp2.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
        # keep track of start time/frame for later
        genderResp2.frameNStart = frameN  # exact frame index
        genderResp2.tStart = t  # local t and not account for scr refresh
        genderResp2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(genderResp2, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'genderResp2.started')
        genderResp2.setAutoDraw(True)
    
    # *student* updates
    if student.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        student.frameNStart = frameN  # exact frame index
        student.tStart = t  # local t and not account for scr refresh
        student.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(student, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'student.started')
        student.setAutoDraw(True)
    
    # *studentResp* updates
    if studentResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        studentResp.frameNStart = frameN  # exact frame index
        studentResp.tStart = t  # local t and not account for scr refresh
        studentResp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(studentResp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'studentResp.started')
        studentResp.setAutoDraw(True)
    
    # *mood* updates
    if mood.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        mood.frameNStart = frameN  # exact frame index
        mood.tStart = t  # local t and not account for scr refresh
        mood.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(mood, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'mood.started')
        mood.setAutoDraw(True)
    
    # *moodResp* updates
    if moodResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        moodResp.frameNStart = frameN  # exact frame index
        moodResp.tStart = t  # local t and not account for scr refresh
        moodResp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(moodResp, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'moodResp.started')
        moodResp.setAutoDraw(True)
    
    # *nextButton* updates
    if nextButton.status == NOT_STARTED and respAge.rating and genderResp1.rating and studentResp.rating and moodResp.rating:
        # keep track of start time/frame for later
        nextButton.frameNStart = frameN  # exact frame index
        nextButton.tStart = t  # local t and not account for scr refresh
        nextButton.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(nextButton, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'nextButton.started')
        nextButton.setAutoDraw(True)
    # *mouse* updates
    if mouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        mouse.frameNStart = frameN  # exact frame index
        mouse.tStart = t  # local t and not account for scr refresh
        mouse.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(mouse, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.addData('mouse.started', t)
        mouse.status = STARTED
        mouse.mouseClock.reset()
        prevButtonState = mouse.getPressed()  # if button is down already this ISN'T a new click
    if mouse.status == STARTED:  # only update if started and not finished!
        buttons = mouse.getPressed()
        if buttons != prevButtonState:  # button state changed?
            prevButtonState = buttons
            if sum(buttons) > 0:  # state changed to a new click
                # check if the mouse was inside our 'clickable' objects
                gotValidClick = False
                try:
                    iter(nextButton)
                    clickableList = nextButton
                except:
                    clickableList = [nextButton]
                for obj in clickableList:
                    if obj.contains(mouse):
                        gotValidClick = True
                        mouse.clicked_name.append(obj.name)
                if gotValidClick:  
                    continueRoutine = False  # abort routine on response
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in demogComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "demog" ---
for thisComponent in demogComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('respAge.response', respAge.getRating())
thisExp.addData('respAge.rt', respAge.getRT())
thisExp.addData('genderResp1.response', genderResp1.getRating())
thisExp.addData('genderResp1.rt', genderResp1.getRT())
thisExp.addData('genderResp2.text',genderResp2.text)
thisExp.addData('studentResp.response', studentResp.getRating())
thisExp.addData('studentResp.rt', studentResp.getRT())
thisExp.addData('moodResp.response', moodResp.getRating())
thisExp.addData('moodResp.rt', moodResp.getRT())
# store data for thisExp (ExperimentHandler)
x, y = mouse.getPos()
buttons = mouse.getPressed()
if sum(buttons):
    # check if the mouse was inside our 'clickable' objects
    gotValidClick = False
    try:
        iter(nextButton)
        clickableList = nextButton
    except:
        clickableList = [nextButton]
    for obj in clickableList:
        if obj.contains(mouse):
            gotValidClick = True
            mouse.clicked_name.append(obj.name)
thisExp.addData('mouse.x', x)
thisExp.addData('mouse.y', y)
thisExp.addData('mouse.leftButton', buttons[0])
thisExp.addData('mouse.midButton', buttons[1])
thisExp.addData('mouse.rightButton', buttons[2])
if len(mouse.clicked_name):
    thisExp.addData('mouse.clicked_name', mouse.clicked_name[0])
thisExp.nextEntry()
# the Routine "demog" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()
# save mic recordings
for tag in mic.clips:
    for i, clip in enumerate(mic.clips[tag]):
        clipFilename = 'recording_mic_%s.wav' % tag
        # if there's more than 1 clip with this tag, append a counter for all beyond the first
        if i > 0:
            clipFilename += '_%s' % i
        clip.save(os.path.join(micRecFolder, clipFilename))

# --- End experiment ---
# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
if eyetracker:
    eyetracker.setConnectionState(False)
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
