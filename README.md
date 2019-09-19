# anesthRecord : a set of python functions to read, display and analyse anesthesia (veterinary) data 
developed essentially for teaching purposes

recordings are .csv files saved by 
the Monitor software (trends or wave files)
the Taphonius software (trends)

to use it:
1- build a configuration .yaml file trough the buildRecordRC.py
to define a paths directory for 
- the data locations (data)
- the folder to save the plots if required (sFig, ...)
(should create 'recordRC.yaml' in the same folder as 'recordMain.py)

2- run the main file (python recordMain.py)
