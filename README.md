# ying_dataAnalysis_tutorials

This repository contains tutorials to process and analyze several physiological signals (e.g. ECG, EEG, eye tracking). The data sets
are Lab Streaming Layer recordings, so I have added a tutorial to load in XDF files using Python. ECG and eye tracking involve 
coding in Python while EEG analysis requires MATLAB. I will try to update this with a comprehensive tutorial on using EEGLAB 
in our lab in the coming future but the [EEGLab Wiki](https://eeglab.org/tutorials/) has a great tutorial on how to use the GUI 
and tips on writing scripts (Section 11).

The code is divided into two directories: __matlab__ and __python__. I would recommend starting with the Python tutorials
as they have tutorials and information on lab streaming layer, as well as the type of data you may encounter in our lab. 
The ECG tutorials will also provide information on how LSL recordings are organized. Then I would move on to the EEG tutorials 
in the matlab directory as it assumes you know about LSL recordings. I am still in the process of writing these EEG tutorials 
(1/5/2023), but I am hoping I can write more soon.

For the Lab Streaming Layer and ECG tutorials, I recommend using a Python virtual environment, so you can keep your 
analysis/projects/classwork separate. That being said, these tutorials are Jupyter Notebooks. I think most people
use Anaconda to access Jupyter Notebooks as it is easy to use. In Anaconda, you can create virtual environments 
easily with a YAML file, allowing the user to pick what version of Python to install and install dependencies without
affecting any of your other work. If you don't want to use Anaconda, let me know and we'll see what we can do. Please refer to 
__virtualEnv_anaconda_installation.pdf__ as you may have to use the terminal or command window (which can be daunting 
for beginners).

Unfortunately, I could not upload the data on this repository, so the data is on a Google Folder which you can find a link 
in the __Data Location.pdf__. These data directories should be moved into each tutorial directory and without them, you 
will not be able to run the code. I have added some interactive (write code) excercises in some of the tutorials, allowing 
you to apply what you learned. The answers can be provided if you shoot me an email, but please try them first or contact me 
for some help. 

Lastly, I have added some cheat sheets for some common Conda commands or terminal commands you might use. Let me know if 
anything goes wrong or if you have suggestions. We could always go through these together. Also let me know if you have 
any suggestions or bugs. 

__Contact Email:__ enc013@ucsd.edu
