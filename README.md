# energizing_pupil1
Code for energizing pupillometry experiment

## Enviornment set up
Psychopy is installed via a conda environment. PyLink is then installed via pip:
```
conda env create -n psychopy -f psychopy-env.yml
/PATH/TO/CONDA/ENVIRONMENTS/FOLDER/psychopy/bin/pip install --index-url=https://pypi.sr-support.com sr-research-pylink
```

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