# energizing_pupil1
Code for energizing pupillometry experiment

## Enviornment set up
Psychopy is installed via a conda environment. PyLink is then installed via pip:
```
conda env create -n psychopy -f psychopy-env.yml
/PATH/TO/CONDA/ENVIRONMENTS/FOLDER/psychopy/bin/pip install --index-url=https://pypi.sr-support.com sr-research-pylink
```
## 03/12/2023
Order of actions for ET in trial:
- Get eyelink object within function
- Enter recalibration if needed
- Put ET in offline mode
- Draw central area on host pc
- Send trial ID and other data to EDF
- Put ET in offline mode
- Start recording
- Pump 100 ms
- Get which eye
- Fixation onset - send message
- Get sample, compare to region and to max time. Abort if max time reached (and recalibrate). End routine if in region for more than needed  time.
- Trigger each next stage
- Get sample, compare to region, abort if out of region for minial time and not blink.
- Abort trial if tracker disconnected
- Register choice
- ET clear screen
- ET pump delay
- ET stop recording
- ET send trial vars to edf
- Calibrate before first trial
- Clean shut off of ET

To do:
- [x] Allocate items to rating, waiting 
- [x] Instructions
- [x] Demographics
- [x] Timing
- [x] Max time
- [ ] ET
- [ ] Sound
- [X] Rating task formattting and ITI
- [X] Rating task instructions
- [ ] Mouse visibility
- [x] Function for trial. Argumets: police, aids
- [x] Function for fixate portion of trial