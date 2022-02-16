# OnCue
Auditory cuing software to remind you of whatever

Overview of Files:
  1. on_cue.py python script with all the code
  2. on_cue.spec pyinstaller file for compiling 
  3. requirements.txt enviroment requirements
  4. OnCueIcon.png icon for program because everyone needs an icon
  5. dist folder contains built executables for different operating systems
    
How-To-Run excutables:
  1. Find, and download your desired operating system folder in the dist folder
  2. Put the downloaded folder somewhere like home directory
  3. Within the folder find the OnCue excutable it should be called OnCue and be in the main folder
  4. Right click on the excutable and make a shortcut to that file and put that short cut in an easy
     to find place like Desktop 
  5. Click the shortcut and have fun with cue's!
  Note: If your excutable does not have an icon you can always right click on the excutable and set an
  icon the OnCueIcon.png is in the same folder if you would like to use that
 
 How-To-Build excutables:
  1. First clone the repo
  2. Install all the enviroment requirements: kivy, pysinewave
  3. Make sure you have pyinstaller installed might need version 3.6 and above
  4. Edit the on_cue.spec file to have the correct directory paths for icon file
  5. In Terminal run: pyinstaller on_cue.spec
  6. Once the command completes you can delete the build folder and then look into the dist folder for your new build
 
