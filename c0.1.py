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
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, monitors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
from psychopy.tools.monitorunittools import deg2pix

import pylink
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray, fabs)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding
import copy

from psychopy.hardware import keyboard

# --- Parameters ---
ITI = 3.0
prepare_duration = 3.0
post_question_gap = 0.2
choice_deadline = 3.0
satisfaction_duration  =  3.5
minimal_answer_epoch = 2.2
minimal_fixation_duration = 0.5
minimum_fixation_proportion = 0.75
fixation_distance = 60 # in pixels. change to degrees
instructions_gap = 0.2
waiting_task_duration = 1*60 #40*60
wait_durations = [3, 6, 9, 12]
max_warnings = 5

n_for_ratings_per_category = 8

# Set this variable to True to run the script in eyetracking "Dummy Mode"
dummy_mode = True

# --- Draw questions for rating ---
# Import questios
question_list = data.importConditions('stimuli/questions.csv')

# Order by category
categories = set([q["question_type"] for q in question_list])
n_categories = len(categories)
question_dict = {c:[q for q in question_list if q['question_type'] == c] for c in categories}

# Shuffle within each category
for c in categories:
    shuffle(question_dict[c])

# Split to rating, practice, and main waiting
rating_questions = []
for c in categories:
    rating_questions += question_dict[c][:n_for_ratings_per_category]

practice1_questions = [question_dict[c][n_for_ratings_per_category] for c in categories]
practice2_questions = [question_dict[c][n_for_ratings_per_category+1] for c in categories]

waiting_questions = []
for c in categories:
    waiting_questions += question_dict[c][(n_for_ratings_per_category+2):]

# --- Instructions ---
instr1_text = [
    {"text_page": """Thank you for participating today. 
You will now complete a computer task about curiosity. 
In this task, you will listen to a series of trivia questions about animals, the arts, food, or geography.
Press 'd' to read the instructions for this task."""},
 {"text_page": """For each question, you must decide if you want to know the answer to the question.
If you want to find out the answer, you will have to wait a certain amount of time. The required waiting period for each answer will be read out to you after you hear the question.
If you do not want to wait to see the answer, you can choose to skip the question.
If you are 100% certain that you already know the answer to the question, you may indicate that you already know it.
If you choose to skip or indicate that you know the answer, you will NOT see the answer to the question.
Press 'd' to continue."""},
{"text_page":["""To wait for answer, you will press the 'd' key.
To skip the answer, press the 'g' key.
If you 100% know the answer, press the 'j' key.
Refer to this diagram below to make sure you understand which key to press.
                     Wait                          Skip                        Know""",
"""
          ┏━━━┓           ┏━━━┓           ┏━━━┓
          ┃ D ┃           ┃ G ┃           ┃ J ┃
          ┗━━━┛           ┗━━━┛           ┗━━━┛
""",
"""Press 'd' to continue."""],
"fonts": ['Arial', 'Menlo', 'Arial'],
"poss": [(0.0, 0.2), (0.0, 0.0), (0.0, -0.15)]},
{"text_page": """If you choose to wait for a question, you will be asked to rate if the answer was worth waiting for on as scale of 1 to 5. 
If the answer was not worth the wait, it should be rated as 1. If it was extremely worth it, rate it as 5. Use numbers 2-4 for annything in between.
Press 'd' to continue."""},
{"text_page": """To rate the answer, please speak the number you choose ("one", "two", "three", "four", or "five") into the microphone.
Please only use whole numbers, no fractions.
Press 'd' to continue."""},
{"text_page": f"""The task will continue for {int(waiting_task_duration / 60)} minutes. The task takes the same amount of time regardless of how many questions you choose to skip or wait for, so please base your decisions on how interested you are in learning the answers.
Press 'd' to continue."""},
{"text_page": """You will now complete a short practice to get comfortable with the task. Please use this time to get used to pressing the different buttons, to rating the answers out loud, and to the amount of time you have to respond to the different prompts.
Press 'd' to start the practice."""}
]

instr2_text = [
    {"text_page": """During this task, we will be recording your eyes using the camera in front of you. 
For this purpose, we need you to always be looking at the target displayed at the center of the screen, unless you are taking a break.
Press 'd' to continue."""},
    {"text_page": """When the computer is ready to play a question, the target will appear on the screen.
When you are ready to hear the question, fix your gaze on the target. 
When the computer has correctly registered your gaze, the target will rotate. Shortly after, the question will play.
From there on, each quesitons is played just as before, and you respond just as you practiced.
Press 'd' to continue."""},
    {"text_page": """If your gaze leaves the target after you initiated a question, the game will stop and the computer will beep to indicate it had lost your gaze.
Try to keep your gaze on the target for the entire sequence: question, answer, and satisfaction rating. Use the intervals between questions, to rest, look away, or blink as much as you need.
Press 'd' to continue."""},
    {"text_page": """You will now complete a short practice to get comfortable with directing your gaze and responding. 
You should respond just as before. This time, you will not be presented with a reminder about the location of the keys or the 1-5 rating scale for the whether the answer was worth it.
Please ring the bell now to call the experimenter.""",
    "cont_key": "q"}
]

instr3_text = [
    {"text_page": f"""You will now start work on the curiosity task.
This part will be {int(waiting_task_duration / 60)} minutes long.
    
Press 'd' to begin the task. """}
]

rating_instr_text = [
    {"text_page": f"""In the next part of this experiment, you will be 
presented with {n_categories} qustions. We would like you to rate your curiosity to know the answer to each of these questions.
You will rate your curiosity on a scale of 
1 - "Not curious at all"     to       5 - "Extremely curious",
    
If you are 100% confident that you know the answer to the question press 'Know' instead of rating your curiosity. Only use this option for questions you are absolutely sure you know the answer to.
Press the space key to continue""",
    "cont_key": "space"},
    {"text_page":  """In this study we are interested in your own personal judgment. Therefore it is important that you rely only on your own knowledge and give your best answer "off the top of your head."
Press the space key to begin this part of the experiment.""",
    "cont_key": "space"}
]

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

# Step 1: Connect to the EyeLink Host PC
#
# The Host IP address, by default, is "100.1.1.1".
# the "el_tracker" objected created here can be accessed through the Pylink
# Set the Host PC address to "None" (without quotes) to run the script
# in "Dummy Mode"
if dummy_mode:
    el_tracker = pylink.EyeLink(None)
else:
    try:
        el_tracker = pylink.EyeLink("100.1.1.1")
    except RuntimeError as error:
        print('ERROR:', error)
        core.quit()
        sys.exit()

# Step 2: Open an EDF data file on the Host PC
edf_file = expInfo['participant'] + ".EDF"
try:
    el_tracker.openDataFile(edf_file)
except RuntimeError as err:
    print('ERROR:', err)
    # close the link if we have one open
    if el_tracker.isConnected():
        el_tracker.close()
    core.quit()
    sys.exit()

# Step 3: Configure the tracker
#
# Put the tracker in offline mode before we change tracking parameters
el_tracker.setOfflineMode()

# Get the software version:  1-EyeLink I, 2-EyeLink II, 3/4-EyeLink 1000,
# 5-EyeLink 1000 Plus, 6-Portable DUO
eyelink_ver = 0  # set version to 0, in case running in Dummy mode
if not dummy_mode:
    vstr = el_tracker.getTrackerVersionString()
    eyelink_ver = int(vstr.split()[-1].split('.')[0])
    # print out some version info in the shell
    print('Running experiment on %s, version %d' % (vstr, eyelink_ver))

# File and Link data control
# what eye events to save in the EDF file, include everything by default
file_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT'
# what eye events to make available over the link, include everything by default
link_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,FIXUPDATE,INPUT'
# what sample data to save in the EDF data file and to make available
# over the link, include the 'HTARGET' flag to save head target sticker
# data for supported eye trackers
if eyelink_ver > 3:
    file_sample_flags = 'LEFT,RIGHT,GAZE,HREF,RAW,AREA,HTARGET,GAZERES,BUTTON,STATUS,INPUT'
    link_sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,AREA,HTARGET,STATUS,INPUT'
else:
    file_sample_flags = 'LEFT,RIGHT,GAZE,HREF,RAW,AREA,GAZERES,BUTTON,STATUS,INPUT'
    link_sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,INPUT'
el_tracker.sendCommand("file_event_filter = %s" % file_event_flags)
el_tracker.sendCommand("file_sample_data = %s" % file_sample_flags)
el_tracker.sendCommand("link_event_filter = %s" % link_event_flags)
el_tracker.sendCommand("link_sample_data = %s" % link_sample_flags)

# Optional tracking parameters
# Sample rate, 250, 500, 1000, or 2000, check your tracker specification
if eyelink_ver > 2:
    el_tracker.sendCommand("sample_rate 1000")
# Choose a calibration type, H3, HV3, HV5, HV13 (HV = horizontal/vertical),
el_tracker.sendCommand("calibration_type = HV9")

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
mon = monitors.Monitor('testMonitor')
win = visual.Window(
    fullscr=False, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='deg')
scn_width, scn_height = win.size

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
instr_max_component = max([len(t["text_page"]) for t in instr1_text + instr2_text if type(t["text_page"]) is list])
text_instr = [visual.TextStim(win=win, name=f'text_instr_{t}',
    font='Arial',
    pos=(0, 0), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    alignText='left',
    antialias=True,
    depth=0.0) for t in range(instr_max_component)]

def display_instructions(instr_text, loop_name):
    # set up handler to look after randomisation of conditions etc
    instr_trials = data.TrialHandler(nReps=1.0, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=instr_text,
        seed=None, name=loop_name)
    thisExp.addLoop(instr_trials)  # add the loop to the experiment
    thisInstr_trial = instr_trials.trialList[0]  # so we can initialise stimuli with some values
    
    for thisInstr_trial in instr_trials:
        currentLoop = instr_trials

        # --- Prepare to start Routine "waiting_instructions" ---
        continueRoutine = True
        routineForceEnded = False
        # update component parameters for each repeat
        key_resp.keys = []
        key_resp.rt = []
        _key_resp_allKeys = []
        # keep track of which components have finished
        waiting_instructionsComponents = [key_resp] + text_instr
        for thisComponent in waiting_instructionsComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED

        # Set text
        if type(thisInstr_trial["text_page"]) is str:
            text_instr[0].text = thisInstr_trial["text_page"]
            num_text_components = 1
        else:
            num_text_components = len(thisInstr_trial["text_page"])
            for i in range(num_text_components):
                text_instr[i].text = thisInstr_trial["text_page"][i]
                text_instr[i].font = thisInstr_trial["fonts"][i]
                text_instr[i].pos = thisInstr_trial["poss"][i]

        # Set key for continue to 'd', unless explicitly specified
        if 'cont_key' in thisInstr_trial:
            cont_key = thisInstr_trial['cont_key']
        else:
            cont_key = 'd'
            
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
            for i in range(num_text_components):
                if text_instr[i].status == NOT_STARTED and tThisFlip >= instructions_gap-frameTolerance:
                    # keep track of start time/frame for later
                    text_instr[i].frameNStart = frameN  # exact frame index
                    text_instr[i].tStart = t  # local t and not account for scr refresh
                    text_instr[i].tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(text_instr[i], 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'text_instr.started')
                    text_instr[i].setAutoDraw(True)
            
            # *key_resp* updates
            waitOnFlip = False
            if key_resp.status == NOT_STARTED and tThisFlip >= instructions_gap-frameTolerance:
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
                theseKeys = key_resp.getKeys(keyList=[cont_key], waitRelease=False)
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
    opacity=None, depth=-1.0, interpolate=True)

def check_fixation(t,
                    gaze_start,
                    gaze_stop,
                    in_hit_region,
                    dummy_mode):
    if dummy_mode:
        g_x, g_y = deg2pix(mouse.getPos(), mon)
        
        # for mouse, origin is center
        fix_x, fix_y = (0.0, 0.0)
    else:
        # For ET, origin is corner
        fix_x, fix_y = (scn_width/2.0, scn_height/2.0)

    # return true if the current gaze position is
    # in a 120 x 120 pixels region around the screen centered
    # 
    if fabs(g_x - fix_x) < fixation_distance and fabs(g_y - fix_y) < fixation_distance:
        # record gaze start time
        if not in_hit_region:
            if gaze_start == -1:
                gaze_start = t
                in_hit_region = True
    else:  # gaze outside the hit region, reset variables
        if in_hit_region:
            logging.data("Fixation borken")
            gaze_stop = t
            in_hit_region = False
            gaze_start = -1

    return in_hit_region, gaze_start, gaze_stop



def draw_fixation(ori,
                  when,
                  tThisFlip,
                  frameN,
                  t,
                  tThisFlipGlobal):
    if ori == 0.0:
        shapes = [fixation_circle, fixation_cross_cardinal, fixation_dot]
    else:
        shapes = [fixation_circle, fixation_cross_rotated, fixation_dot]
    for _, x in enumerate(shapes):
        if x.status == NOT_STARTED and tThisFlip >= when-frameTolerance:
            # keep track of start time/frame for later
            x.frameNStart = frameN  # exact frame index
            x.tStart = t  # local t and not account for scr refresh
            x.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(x, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, x.name + '.started')
            x.setAutoDraw(True)           

def rotate_fixation(ori,
                  when,
                  tThisFlip,
                  frameN,
                  t,
                  tThisFlipGlobal):
        if ori == 0.0:
            o = fixation_cross_rotated
            n = fixation_cross_cardinal
        else:
            n = fixation_cross_rotated
            o = fixation_cross_cardinal

        
        if (n.status == NOT_STARTED or n.status == FINISHED) and tThisFlip >= when-frameTolerance:
            
            # keep track of start time/frame for later
            n.frameNStart = frameN  # exact frame index
            n.tStart = t  # local t and not account for scr refresh
            n.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(n, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, n.name+'.started')
            n.setAutoDraw(True)
            
            # Reset timers for circle and dot
            # fixation_circle.tStartRefresh = tThisFlipGlobal # on global time
            # fixation_dot.tStartRefresh = tThisFlipGlobal # on global timev
        if o.status == STARTED:
            # is it time to stop? (based on local clock)
            if tThisFlip >  when-frameTolerance:
                # keep track of stop time/frame for later
                o.tStop = t  # not accounting for scr refresh
                o.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, o.name + '.stopped')
                o.setAutoDraw(False)

# --- Initialize components for Routine "question" ---
static_prepare = clock.StaticPeriod(win=win, screenHz=expInfo['frameRate'], name='static_prepare')
question_voice = sound.Sound('A', secs=-1, stereo=True, hamming=True,
    name='question_voice')
question_voice.setVolume(1.0)
duration_voice = sound.Sound('A', secs=-1, stereo=True, hamming=True,
    name='duration_voice')
duration_voice.setVolume(1.0)
choice = keyboard.Keyboard()

choice_aid = visual.TextStim(win=win, name='choice_aid',
    text = """WAIT              SKIP                KNOW""",
    font='Arial',
    alignText = 'center',
    anchorHoriz = 'center',
    pos=(0.02, -0.1), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    antialias=True,
    depth=0.0)

warning_msg = visual.TextStim(win=win, name='deadline_warning',
    font='Arial',
    alignText = 'center',
    anchorHoriz = 'center',
    pos=(0.02, -0.1), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    antialias=True,
    depth=0.0)

call_experimenter_msg = visual.TextStim(win=win, name='call_experimenter',
    text = """Please ring for the experimenter""",
    font='Arial',
    alignText = 'center',
    anchorHoriz = 'center',
    pos=(0.02, -0.1), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    antialias=True,
    depth=0.0)

# --- Initialize components for Routine "answer" ---
answer_voice = sound.Sound('A', secs=-1, stereo=True, hamming=True,
    name='answer_voice')
answer_voice.setVolume(1.0)
mic = sound.microphone.Microphone(
    device=None, channels=None, 
    sampleRateHz=48000, maxRecordingSize=24000.0
)
static_wait = clock.StaticPeriod(win=win, screenHz=expInfo['frameRate'], name='static_wait')

satisfaction_aid = visual.TextStim(win=win, name='satisfaction_aid',
    text = """Speak:
    1     2       3       4       5
    
Not worth                     Extremely
    it                         worth it
""",
    font='Arial',
    alignText = 'center',
    anchorHoriz = 'center',
    pos=(0.01, -0.2), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    antialias=True,
    depth=0.0)

# --- Functions for calling routines "fixate", "question", "answer" ---
# Start trial, wait for fixation
def run_fixate(block_trials):
    # --- Prepare to start Routine "fixate" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    # keep track of which components have finished
    fixateComponents = [fixation_cross_cardinal, fixation_dot, fixation_circle]
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
    
    gaze_start = -1
    in_hit_region = False
    # --- Run Routine "fixate" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fixation* updates
        draw_fixation(0.0,
                      ITI,
                      tThisFlip,
                      frameN,
                      t,
                      tThisFlipGlobal)
        
        in_hit_region, gaze_start, _ = check_fixation(tThisFlip,
                                                    gaze_start,
                                                    -1,
                                                    in_hit_region,
                                                    dummy_mode)
        
        if in_hit_region:
            if tThisFlip >= gaze_start + minimal_fixation_duration:
                logging.data("Minimal fixation duration achieved")
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
    # the Routine "fixate" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

# Play question, collect choice
def run_question(block_trials,
                 ITI=0.0,
                 display_choice_aid=False):
    # --- Prepare to start Routine "question" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code
    
    question_voice.setSound('stimuli/' + question_file, hamming=True)
    question_voice.setVolume(1.0, log=False)
    duration_voice.setSound('stimuli/' + str(thisTrialDuration) + 's.ogg', hamming=True)
    duration_voice.setVolume(1.0, log=False)
    choice.keys = []
    choice.rt = []
    _choice_allKeys = []
    # keep track of which components have finished
    questionComponents = [static_prepare, question_voice, duration_voice, choice, 
                          fixation_cross_cardinal, fixation_dot, fixation_circle, fixation_cross_rotated, choice_aid] 
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
    
    in_hit_region = True
    sum_in_hit_region = 0
    # --- Run Routine "question" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        in_hit_region, _, _ = check_fixation(tThisFlip, -1, -1, in_hit_region, dummy_mode)
        sum_in_hit_region += in_hit_region
        
        # *fixation_prepare* updates
        draw_fixation(45.0,
                      0.0+ITI,
                      tThisFlip,
                      frameN,
                      t,
                      tThisFlipGlobal)
        
        # *fixation_question* updates
        rotate_fixation(0.0,
                    prepare_duration+ITI,
                    tThisFlip,
                    frameN,
                    t,
                    tThisFlipGlobal)
        # start/stop question_voice
        if question_voice.status == NOT_STARTED and tThisFlip >= prepare_duration+ITI-frameTolerance:
            # keep track of start time/frame for later
            question_voice.frameNStart = frameN  # exact frame index
            question_voice.tStart = t  # local t and not account for scr refresh
            question_voice.tStartRefresh = tThisFlipGlobal  # on global time
            # add timestamp to datafile
            thisExp.addData('question_voice.started', tThisFlipGlobal)
            question_voice.play(when=win)  # sync with win flip
        # start/stop duration_voice
        if duration_voice.status == NOT_STARTED and tThisFlip >= (ITI + prepare_duration + question_voice.duration +
                                                                  post_question_gap -frameTolerance):
            # keep track of start time/frame for later
            duration_voice.frameNStart = frameN  # exact frame index
            duration_voice.tStart = t  # local t and not account for scr refresh
            duration_voice.tStartRefresh = tThisFlipGlobal  # on global time
            # add timestamp to datafile
            thisExp.addData('duration_voice.started', tThisFlipGlobal)
            duration_voice.play(when=win)  # sync with win flip
        
        # Display choice aid if needed
        if display_choice_aid:
            if choice_aid.status == NOT_STARTED and tThisFlip >= (ITI + prepare_duration + question_voice.duration + 
                                                          post_question_gap + duration_voice.duration-frameTolerance):
                # keep track of start time/frame for later
                choice_aid.frameNStart = frameN  # exact frame index
                choice_aid.tStart = t  # local t and not account for scr refresh
                choice_aid.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(choice_aid, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, choice_aid.name + '.started')
                choice_aid.setAutoDraw(True)

        # *choice* updates
        waitOnFlip = False
        if choice.status == NOT_STARTED and tThisFlip >= (ITI + prepare_duration + question_voice.duration + 
                                                          post_question_gap + duration_voice.duration / 2-frameTolerance):
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
            static_prepare.tStop = static_prepare.tStart + prepare_duration  # record stop time
        
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

        # Implement response deadline
        if tThisFlip >= (ITI + prepare_duration + question_voice.duration + 
                            post_question_gap + duration_voice.duration + choice_deadline -frameTolerance):
            logging.exp("Failed to respond on time")
            continueRoutine = False
        
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
    block_trials.addData('choice.keys',choice.keys)
    if choice.keys != None:  # we had a response
        block_trials.addData('choice.rt', choice.rt)

    # Record percentage fixating
    mean_in_hit_region =  sum_in_hit_region / frameN
    block_trials.addData('question.sum_frames_fixating', sum_in_hit_region)
    block_trials.addData('question.total_frames', frameN)
    logging.exp(f"Fixated during this question {mean_in_hit_region * 100}% of the time")

    # the Routine "question" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

    return sum_in_hit_region, frameN

# Play answer, collect satisfaction
def run_answer(block_trials,
               thisTrialDuration,
               display_satisfaction_aid=False):
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
    answerComponents = [answer_voice, mic, static_wait, 
                        fixation_cross_cardinal, fixation_dot, fixation_circle, fixation_cross_rotated]
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

    in_hit_region = True
    sum_in_hit_region = 0

    # --- Run Routine "answer" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)

        # Get fixation status
        in_hit_region, _, _ = check_fixation(tThisFlip, -1, -1, in_hit_region, dummy_mode)
        sum_in_hit_region += in_hit_region
        
        # *fixation_wait* updates
        draw_fixation(45.0, 0.0, 
                      tThisFlip, 
                      frameN,
                      t,
                      tThisFlipGlobal)
        
        # *fixation_answer* updates
        rotate_fixation(0.0, thisTrialDuration, 
                        tThisFlip,
                        frameN,
                        t,
                        tThisFlipGlobal)

        # start/stop answer_voice
        if answer_voice.status == NOT_STARTED and tThisFlip >= thisTrialDuration-frameTolerance:
            # keep track of start time/frame for later
            answer_voice.frameNStart = frameN  # exact frame index
            answer_voice.tStart = t  # local t and not account for scr refresh
            answer_voice.tStartRefresh = tThisFlipGlobal  # on global time
            # add timestamp to datafile
            thisExp.addData('answer_voice.started', tThisFlipGlobal)
            answer_voice.play(when=win)  # sync with win flip

        # Make sure answer epoch is not too short
        answer_epoch = max(answer_voice.duration, minimal_answer_epoch)
        
        # *fixation_satisfaction* updates
        rotate_fixation(45.0, thisTrialDuration + answer_epoch, 
                        tThisFlip,
                        frameN,
                        t,
                        tThisFlipGlobal)

        for x in [fixation_circle, fixation_cross_rotated, fixation_cross_cardinal, fixation_dot, satisfaction_aid]:
            if x.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlip > thisTrialDuration + answer_epoch + satisfaction_duration-frameTolerance:
                    # keep track of stop time/frame for later
                    x.tStop = t  # not accounting for scr refresh
                    x.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, x.name + '.stopped')
                    x.setAutoDraw(False)
                    x.status = PAUSED

        # Display satisfaction aid if needed
        if display_satisfaction_aid:
            if satisfaction_aid.status == NOT_STARTED and tThisFlip >= thisTrialDuration + answer_epoch-frameTolerance:
                # keep track of start time/frame for later
                satisfaction_aid.frameNStart = frameN  # exact frame index
                satisfaction_aid.tStart = t  # local t and not account for scr refresh
                satisfaction_aid.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(satisfaction_aid, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, satisfaction_aid.name + '.started')
                satisfaction_aid.setAutoDraw(True)

        
        # mic updates
        if mic.status == NOT_STARTED and t >= thisTrialDuration + answer_epoch-frameTolerance:
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
            if tThisFlipGlobal > mic.tStartRefresh + satisfaction_duration-frameTolerance:
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
            if hasattr(thisComponent, "status") and thisComponent.status not in [FINISHED, PAUSED]:
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
    block_trials.addData('mic.clip', os.path.join(micRecFolder, 'recording_mic_%s.wav' % tag))

    # Record percentage fixating
    mean_in_hit_region =  sum_in_hit_region / frameN
    block_trials.addData('answer.sum_frames_fixating', sum_in_hit_region)
    block_trials.addData('answer.total_frames', frameN)
    logging.exp(f"Fixated during this answer {mean_in_hit_region * 100}% of the time")

    # the Routine "answer" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    return sum_in_hit_region, frameN

def display_warning():
    continueRoutine = True
    routineForceEnded = False

    key_resp.keys = []
    key_resp.rt = []
    _key_resp_allKeys = []

    # keep track of which components have finished
    deadlineComponents = [warning_msg, key_resp]
    for thisComponent in deadlineComponents:
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
    
    # --- Run Routine "deadline_warning" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        if warning_msg.status == NOT_STARTED and tThisFlip >= instructions_gap-frameTolerance:
            # keep track of start time/frame for later
            warning_msg.frameNStart = frameN  # exact frame index
            warning_msg.tStart = t  # local t and not account for scr refresh
            warning_msg.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(warning_msg, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'deadline_warning.started')
            warning_msg.setAutoDraw(True)

        # *key_resp* updates
        waitOnFlip = False
        if key_resp.status == NOT_STARTED and tThisFlip >= instructions_gap-frameTolerance:
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
            theseKeys = key_resp.getKeys(keyList=['d'], waitRelease=False)
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
        for thisComponent in deadlineComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "deadline_warning" ---
    for thisComponent in deadlineComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

    # the Routine "deadline_warning" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
warning_counter =  0
def display_deadline_warning(warning_counter):
    # --- Prepare to start Routine "deadline warning" ---
    # Check whether warning needs to be given
    if choice.keys != None or warning_counter >= max_warnings:
        return warning_counter
    
    # Update warning counter
    warning_counter += 1
    thisExp.addData("n_warnings", warning_counter)
    logging.data("Choice deadline missed")

    warning_msg.text = """Please respond more quickly.
    
Press the 'd' key to continue."""

    display_warning()

    return warning_counter

def display_fixation_warning(warning_counter):
    # --- Prepare to start Routine "fixation warning" ---
    
    if warning_counter >= max_warnings:
        return warning_counter
    
    # Update warning counter
    warning_counter += 1
    thisExp.addData("n_warnings", warning_counter)
    logging.data("Poor fixation on last trial")

    warning_msg.text = """Please keep your gaze on the target.
    
Press the 'd' key to continue."""

    display_warning()

    return warning_counter


def display_call_experimenter(warning_counter):
    # --- Prepare to start Routine "call experimenter" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    # Run 'Begin Routine' code from conditional_answer
    if warning_counter < max_warnings:
        return warning_counter

    # Update warning counter
    warning_counter += 1
    thisExp.addData("n_warnings", warning_counter)
    logging.data("Choice deadline missed")

    key_resp.keys = []
    key_resp.rt = []
    _key_resp_allKeys = []

    # keep track of which components have finished
    callExperimenterComponents = [call_experimenter_msg, key_resp]
    for thisComponent in callExperimenterComponents:
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
    
    # --- Run Routine "deadline_warning" ---
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        if call_experimenter_msg.status == NOT_STARTED and tThisFlip >= instructions_gap-frameTolerance:
            # keep track of start time/frame for later
            call_experimenter_msg.frameNStart = frameN  # exact frame index
            call_experimenter_msg.tStart = t  # local t and not account for scr refresh
            call_experimenter_msg.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(call_experimenter_msg, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'call_experimenter.started')
            call_experimenter_msg.setAutoDraw(True)

        # *key_resp* updates
        waitOnFlip = False
        if key_resp.status == NOT_STARTED and tThisFlip >= instructions_gap-frameTolerance:
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
            theseKeys = key_resp.getKeys(keyList=['q'], waitRelease=False)
            _key_resp_allKeys.extend(theseKeys)
            if len(_key_resp_allKeys):
                key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                key_resp.rt = _key_resp_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
                
                warning_counter = 0
                logging.data("Warning counter reset")

        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in callExperimenterComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "call experimenter" ---
    for thisComponent in callExperimenterComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

    # the Routine "call experimenter" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

    return warning_counter

# --- Initialize components for Routine "rating" ---
text = visual.TextStim(win=win, name='text',
    text='',
    font='Arial',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
slider = visual.Slider(win=win, name='slider',
    startValue=None, size=(12.0, 1.0), pos=(0, -3.4), units='deg',
    labels=("Know", "1", "2", "3", "4", "5"), ticks=(0, 1, 2, 3, 4, 5), granularity=1.0,
    style='rating', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Blue', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=1.0,
    flip=False, ori=0.0, depth=-1, readOnly=False)


mouse = event.Mouse(win=win)
x, y = [None, None]
mouse.mouseClock = core.Clock()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

# --- First instruction loop ---
# display_instructions(instr1_text, "instr1_trials")

# # First practice loop ----
# # set up handler to look after randomisation of conditions etc
# practice1_trials = data.TrialHandler(nReps=1.0, method='random', 
#     extraInfo=expInfo, originPath=-1,
#     trialList=practice1_questions,
#     seed=None, name='practice1_trials')
# thisExp.addLoop(practice1_trials)  # add the loop to the experiment
# thisWaiting_trial = practice1_trials.trialList[0]  # so we can initialise stimuli with some values
# # abbreviate parameter names if possible (e.g. rgb = thisWaiting_trial.rgb)
# if thisWaiting_trial != None:
#     for paramName in thisWaiting_trial:
#         exec('{} = thisWaiting_trial[paramName]'.format(paramName))

# # Sample durations w/o replacement
# this_block_durations = copy.copy(wait_durations)
# shuffle(this_block_durations)

# for thisWaiting_trial in practice1_trials:
#     currentLoop = practice1_trials
#     # abbreviate parameter names if possible (e.g. rgb = thisWaiting_trial.rgb)
#     if thisWaiting_trial != None:
#         for paramName in thisWaiting_trial:
#             exec('{} = thisWaiting_trial[paramName]'.format(paramName))

#     # Sample durations w/o replacement
#     thisTrialDuration = this_block_durations.pop()
#     thisExp.addData('wait_duration', thisTrialDuration)
    
#     run_question(practice1_trials, ITI=ITI, display_choice_aid=True)

#     warning_counter = display_deadline_warning(warning_counter)

#     warning_counter = display_call_experimenter(warning_counter)
    
#     run_answer(practice1_trials, thisTrialDuration, display_satisfaction_aid=True)

#     thisExp.nextEntry()    
# # completed 1.0 repeats of 'practice1_trials'

# # --- Second instruction loop ---
# display_instructions(instr2_text, "instr2_trials")

# Second practice loop ---
# set up handler to look after randomisation of conditions etc
practice2_trials = data.TrialHandler(nReps=1.0, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=practice2_questions,
    seed=None, name='practice2_trials')
thisExp.addLoop(practice2_trials)  # add the loop to the experiment
thisWaiting_trial = practice2_trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisWaiting_trial.rgb)
if thisWaiting_trial != None:
    for paramName in thisWaiting_trial:
        exec('{} = thisWaiting_trial[paramName]'.format(paramName))

# Sample durations w/o replacement
this_block_durations = copy.copy(wait_durations)
shuffle(this_block_durations)

for thisWaiting_trial in practice2_trials:
    currentLoop = practice2_trials
    # abbreviate parameter names if possible (e.g. rgb = thisWaiting_trial.rgb)
    if thisWaiting_trial != None:
        for paramName in thisWaiting_trial:
            exec('{} = thisWaiting_trial[paramName]'.format(paramName))

    # Sample durations w/o replacement
    thisTrialDuration = this_block_durations.pop()
    thisExp.addData('wait_duration', thisTrialDuration)

    run_fixate(practice2_trials)
    
    q_sum_in_region, q_frameN = run_question(practice2_trials)

    warning_counter = display_deadline_warning(warning_counter)

    warning_counter = display_call_experimenter(warning_counter)
    
    a_sum_in_region, a_frameN = run_answer(practice2_trials, thisTrialDuration)

    print((q_sum_in_region + a_sum_in_region) / (q_frameN + a_frameN))
    if (q_sum_in_region + a_sum_in_region) / (q_frameN + a_frameN) < minimum_fixation_proportion:
        warning_counter = display_fixation_warning(warning_counter)

        warning_counter = display_call_experimenter(warning_counter)

    thisExp.nextEntry()    
# completed 1.0 repeats of 'practice2_trials'


# --- Final message before waiting task ---
display_instructions(instr3_text, "instr3_trials")

# set up handler to look after randomisation of conditions etc
waiting_trials = data.TrialHandler(nReps=1.0, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=waiting_questions,
    seed=None, name='waiting_trials')
thisExp.addLoop(waiting_trials)  # add the loop to the experiment
thisWaiting_trial = waiting_trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisWaiting_trial.rgb)
if thisWaiting_trial != None:
    for paramName in thisWaiting_trial:
        exec('{} = thisWaiting_trial[paramName]'.format(paramName))

waiting_task_start = win.getFutureFlipTime(clock=None)
for thisWaiting_trial in waiting_trials:
    currentLoop = waiting_trials
    # abbreviate parameter names if possible (e.g. rgb = thisWaiting_trial.rgb)
    if thisWaiting_trial != None:
        for paramName in thisWaiting_trial:
            exec('{} = thisWaiting_trial[paramName]'.format(paramName))

    # Check for total time
    if win.getFutureFlipTime(clock=None) > waiting_task_start + waiting_task_duration:
        logging.data("Waiting task over after %0.2f seconds" %(waiting_task_start + waiting_task_duration))
        break

    # Draw wait duration for this trial
    thisTrialDuration = wait_durations[randint(0,4)]
    thisExp.addData('wait_duration', thisTrialDuration)

    run_fixate(waiting_trials)
    
    q_sum_in_region, q_frameN = run_question(practice2_trials)

    warning_counter = display_deadline_warning(warning_counter)

    warning_counter = display_call_experimenter(warning_counter)
    
    a_sum_in_region, a_frameN = run_answer(practice2_trials, thisTrialDuration)

    print((q_sum_in_region + a_sum_in_region) / (q_frameN + a_frameN))
    if (q_sum_in_region + a_sum_in_region) / (q_frameN + a_frameN) < minimum_fixation_proportion:
        warning_counter = display_fixation_warning(warning_counter)

        warning_counter = display_call_experimenter(warning_counter)

    thisExp.nextEntry()    
# completed 1.0 repeats of 'waiting_trials'

# save mic recordings
for tag in mic.clips:
    for i, clip in enumerate(mic.clips[tag]):
        clipFilename = 'recording_mic_%s.wav' % tag
        # if there's more than 1 clip with this tag, append a counter for all beyond the first
        if i > 0:
            clipFilename += '_%s' % i
        clip.save(os.path.join(micRecFolder, clipFilename))

# --- Ration task ---
# Present instructions
display_instructions(rating_instr_text, "rating_instr_trials")

# set up handler to look after randomisation of conditions etc
rating_trials = data.TrialHandler(nReps=1.0, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=rating_questions,
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
    text.setText("How curious are you to know: \n\n" + question_text + "\n\n\n")
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
        if text.status == NOT_STARTED and tThisFlip >= instructions_gap-frameTolerance:
            # keep track of start time/frame for later
            text.frameNStart = frameN  # exact frame index
            text.tStart = t  # local t and not account for scr refresh
            text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text.started')
            text.setAutoDraw(True)
        
        # *slider* updates
        if slider.status == NOT_STARTED and tThisFlip >= instructions_gap-frameTolerance:
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